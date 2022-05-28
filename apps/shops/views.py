from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Q
from apps.shops.models import Shops, Metadata
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from apps.locations.models import Country, State
from django.core import serializers


@method_decorator(login_required, name='dispatch')
class ShopsIndexView(View):
    def __init__(self):
        self.context = {"breadcrumbs" : []}
        self.generateBreadcrumbs();
        self.context['title'] = 'Shops'
        self.template = 'shop/shops.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, self.context)


    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Shops", "route" : '','active' : True});



class LoadShopsDatatable(BaseDatatableView):
    model = Shops
    
    order_columns = ['','name']
    
    def get_initial_queryset(self):

        filter_value = self.request.POST.get('columns[3][search][value]', None)
        
        if filter_value == '1':
            return self.model.objects.filter(is_active__contains=1)
        elif filter_value == '2':
            return self.model.objects.filter(is_active__contains=0)
        else:
            return self.model.objects.all()

        


    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        
        
        
        if search:
            qs = qs.filter(name__istartswith=search)

        # more advanced example using extra parameters
        filter_name = self.request.POST.get('name', None)

        if filter_name is not None:
            brands_datas = filter_name.split(' ')
            qs_params = None
            for part in brands_datas:
                q = Q(name__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id' : escape(item.id), 
                'name' : escape(item.name),
                'owner' : escape(item.owner),
                'logo' : escape(item.logo.url),
                'is_active' : escape(item.is_active),
                'created_date' : item.created_date.strftime("%Y-%m-%d %H:%M:%S"),
                'modified_date' : item.modified_date.strftime("%Y-%m-%d %H:%M:%S"),
            })
        return json_data




@method_decorator(login_required, name='dispatch')
class ShopsCreateOrUpdatetView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = 'Created'
        self.context = {'breadcrumbs': []}
        self.context['title'] = 'Shop'
        self.context['action_title'] = 'Create'
        self.template = 'shop/create-or-update-shop.html'
        
        
    def get(self, request, *args, **kwargs):
        id = kwargs.pop('id', None)
        self.getCountryAndState()
        if id:
            self.edit(id)
        self.generateBreadcrumbs()
        return render(request,self.template, self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Shops", "route" : reverse('shops:shops.index'),'active' : False});
        self.context['breadcrumbs'].append({"name" : self.context['action_title']+" Shops", "route" : '','active' : True});

    def post(self, request, *args, **kwargs):
        
        try:
            shop_id = request.POST.get('shop_id', None)
            
            if shop_id:
                self.action = 'Updated'
                shop = get_object_or_404(Shops, id=shop_id)
                if request.FILES.__len__() != 0:
                    if request.POST.get('shop_image', None) is None:
                        shop.logo = request.FILES.get('shop_image')
                    if request.POST.get('shop_cover_image', None) is None:
                        shop.cover_image = request.FILES.get('shop_cover_image')
            else:
                shop = Shops()
                if request.FILES.__len__() != 0:
                    if request.POST.get('shop_image', None) is None:
                        shop.logo = request.FILES.get('shop_image')
                    if request.POST.get('shop_cover_image', None) is None:
                        shop.cover_image = request.FILES.get('shop_cover_image')


            #general
            shop.name         = request.POST.get('shop_name').strip()
            shop.description  = request.POST.get('shop_description','').strip() #optional
            shop.country_id           = request.POST.get('country').strip()
            shop.state_id             = request.POST.get('state').strip()
            shop.city              = request.POST.get('city').strip().capitalize()
            shop.zip_code          = request.POST.get('zip_code').strip()
            shop.street_address    = request.POST.get('street_address').strip().capitalize()

            #advanced  #optional
            shop.account_holder_name   = request.POST.get('account_holder_name','').strip()
            shop.account_holder_email  = request.POST.get('account_holder_email','').strip()
            shop.bank_name             = request.POST.get('bank_name','').strip()
            shop.account_number        = request.POST.get('account_number','').strip()
            shop.latitude              = request.POST.get('latitude','').strip()
            shop.longitude             = request.POST.get('longitude','').strip()
            shop.contact_number        = request.POST.get('contact_number','').strip()
            shop.website               = request.POST.get('website','').strip()

            self.meta_title            = request.POST.get('meta_title','').strip()
            self.shop_meta_description = request.POST.get('shop_meta_description','').strip()
            self.meta_keywords         = request.POST.get('meta_keywords','').strip()

            shop.is_active               = int(request.POST.get('shop_status',''))
            

            shop.owner_id = request.user.id
            shop.save()

            if shop.id:
                self.insertMetadata(shop.id)
            messages.success(request, f"Data Successfully "+ self.action)

        except Exception as e:
            messages.error(request, f"Something went wrong.")
            return redirect('shops:shops.create')

        return redirect('shops:shops.index')




    def getCountryAndState(self):
        self.context['countries'] = Country.objects.all()
        self.context['states'] = State.objects.all()


    def edit(self,id):
        self.context['shop'] = get_object_or_404(Shops, id=id)
        meta_data = list(Metadata.objects.filter(shop=id))
        self.context['title'] = 'Shop'
        self.context['action_title'] = 'Update'
        if len(meta_data) > 0:
            self.context['meta_data'] = {"meta_title" : meta_data[0].meta_title, "meta_description" : meta_data[0].meta_description, "meta_tag" : ','.join([str(shop_meta.meta_tag) for shop_meta in meta_data])}




    def insertMetadata(self,shop_id):
        if len(self.meta_keywords) > 0 :
            Metadata.objects.filter(shop_id=shop_id).delete()
            for meta_keyword in self.meta_keywords.split(","):
                meta_data = Metadata()
                meta_data.meta_title = self.meta_title  
                meta_data.meta_description = self.shop_meta_description  
                meta_data.meta_tag = meta_keyword
                meta_data.shop_id  = shop_id

                meta_data.save()


@method_decorator(login_required, name='dispatch')
class DestroyStaffRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            shop_ids = request.POST.getlist('ids[]')
            if shop_ids:
                Shops.objects.filter(id__in=shop_ids).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
        








