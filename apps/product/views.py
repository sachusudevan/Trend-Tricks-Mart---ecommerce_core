import logging
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Q
from django.contrib import messages
from apps.product.models import Manufactures, Products
from apps.groups.models import Groups



logger = logging.getLogger(__name__)



#shop products view
@method_decorator(login_required, name='dispatch')
class ShopProductsIndexView(View):
    def __init__(self):
        self.context = {"breadcrumbs" : []}
        self.generateBreadcrumbs();
        self.context['title'] = 'Products'
        self.template = 'shop/products/product.html'

    def get(self, request, *args, **kwargs):
        self.context['shop_slug'] = kwargs.pop('shop_slug', None) 
        return render(request, self.template, self.context)


    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Shops", "route" : reverse('shops:shops.index'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Products", "route" : '','active' : True});









































#============================== start shop products view ======================================================


@method_decorator(login_required, name='dispatch')
class ShopManufacturesIndexView(View):
    def __init__(self):
        self.context = {"breadcrumbs" : []}
        self.generateBreadcrumbs();
        self.context['title'] = 'Manufactureres'
        self.template = 'shop/manufactureres/manufacture.html'

    def get(self, request, *args, **kwargs):
        self.context['shop_slug'] = kwargs.pop('shop_slug', None) 
        return render(request, self.template, self.context)


    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Shops", "route" : reverse('shops:shops.index'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Manufactureres", "route" : '','active' : True});







class LoadShopManufacturesDatatable(BaseDatatableView):
    model = Manufactures
    
    order_columns = ['id','name']
    
    def get_initial_queryset(self):

        filter_value = self.request.POST.get('columns[4][search][value]', None)
        
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
                'website' : escape(item.website),
                'product' : escape(Products.objects.filter(manufacture__exact=item.id).count()),
                'logo' : escape(item.logo.url),
                'group' : escape(item.group),
                'is_active' : escape(item.is_active),
                'created_date' : item.created_date.strftime("%Y-%m-%d %H:%M:%S"),
                'modified_date' : item.modified_date.strftime("%Y-%m-%d %H:%M:%S"),
                
            })
        return json_data







@method_decorator(login_required, name='dispatch')
class ShopManufacturesCreateOrUpdatetView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = 'Created'
        self.context = {'breadcrumbs': []}
        self.context['title'] = 'Manufacture'
        self.context['action_title'] = 'Create'
        self.template = 'shop/manufactureres/create-or-update-manufacture.html'
        
        
    def get(self, request, *args, **kwargs):
        self.context['shop_slug'] = kwargs.pop('shop_slug', None) 
        self.context['groups'] = Groups.objects.all()
        id = kwargs.pop('id', None)
        if id:
            self.context['manufacture'] = get_object_or_404(Manufactures, id=id)
        self.generateBreadcrumbs()
        return render(request,self.template, self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Shops", "route" : reverse('shops:shops.index'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Manufactures", "route" : reverse('shops:shops.shop.manufacture.index', args=(self.context['shop_slug'],)),'active' : False});
        self.context['breadcrumbs'].append({"name" : self.context['action_title']+" Manufacture", "route" : '','active' : True});

    def post(self, request, *args, **kwargs):

        manufacture_id = request.POST.get('manufacture_id', None)
        
        self.context['shop_slug'] = kwargs.pop('shop_slug', None) 
        try:
            
            if manufacture_id:
                self.action = 'Updated'
                manufacture = get_object_or_404(Manufactures, id=manufacture_id)
                if request.FILES.__len__() != 0:
                    if request.POST.get('manufacture_image', None) is None:
                        manufacture.logo = request.FILES.get('manufacture_image')
                    if request.POST.get('manufacture_cover_image', None) is None:
                        manufacture.cover_image = request.FILES.get('manufacture_cover_image')
            else:
                manufacture = Manufactures()
                if request.FILES.__len__() != 0:
                    if request.POST.get('manufacture_image', None) is None:
                        manufacture.logo = request.FILES.get('manufacture_image')
                    if request.POST.get('manufacture_cover_image', None) is None:
                        manufacture.cover_image = request.FILES.get('manufacture_cover_image')
            

            #general
            manufacture.name         = request.POST.get('manufacture_name').strip()
            manufacture.description  = request.POST.get('manufacture_description','').strip() #optional
            manufacture.website      = request.POST.get('website','').strip()
            manufacture.group_id     = request.POST.get('group_id')
            manufacture.is_active    = 0 if request.POST.get('manufacture_status',0) == ''  else  int(request.POST.get('manufacture_status',0))
            manufacture.owner_id = request.user.id
            manufacture.save()

            messages.success(request, f"Data Successfully "+ self.action)

        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if manufacture_id is not None:
                return HttpResponse("fgdfg"+str(e))
                return redirect('shops:shops.update', id=manufacture_id)   
            return redirect('shops:shops.shop.manufacture.create', shop_slug=self.context['shop_slug'])

        return redirect('shops:shops.shop.manufacture.index', shop_slug=self.context['shop_slug'])




@method_decorator(login_required, name='dispatch')
class ShopManufacturesDestroyRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            shop_ids = request.POST.getlist('ids[]')
            if shop_ids:
                Manufactures.objects.filter(id__in=shop_ids).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)



#============================== end shop products view ======================================================
