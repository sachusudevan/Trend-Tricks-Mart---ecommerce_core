import logging
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q
from apps.categories.models import Categories
from apps.groups.models import Groups

logger = logging.getLogger(__name__)



@method_decorator(login_required, name='dispatch')
class CategoryIndexView(View):
    def __init__(self):
        self.context = {"breadcrumbs" : []}
        self.template = 'categories/category.html'
        self.context['title'] = 'Category'
        self.generateBreadcrumbs();

    def get(self, request, *args, **kwargs):
        
        return render(request, self.template, self.context)


    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Category", "route" : '','active' : True});




class LoadShopsDatatable(BaseDatatableView):
    model = Categories
    
    order_columns = ['id','name','','is_active','','','id']
    
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
                'icon' : escape(item.icon.url),
                'image' : escape(item.image.url),
                'type' : escape(item.type),
                'slug' : escape(item.slug),
                'is_active' : escape(item.is_active),
                'created_date' : item.created_date.strftime("%Y-%m-%d %H:%M:%S"),
                'modified_date' : item.modified_date.strftime("%Y-%m-%d %H:%M:%S"),
            })
        return json_data




@method_decorator(login_required, name='dispatch')
class CategoryCreateOrUpdatetView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = 'Created'
        self.context = {'breadcrumbs': []}
        self.context['title'] = 'Category'
        self.context['action_title'] = 'Create'
        self.template = 'categories/create-or-update-category.html'
        
        
    def get(self, request, *args, **kwargs):
        id = kwargs.pop('id', None)
        self.context['types'] = Groups.objects.filter(is_active__exact=1)
        parent_category = Categories.objects.filter(is_active__exact=1)
        if id:
            self.context['action_title'] = 'Update'
            self.context['category'] = get_object_or_404(Categories, id=id)
            parent_category = parent_category.exclude(id__exact = id)
            
        self.context['parent_categories'] = parent_category
        self.generateBreadcrumbs()
        return render(request,self.template, self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Category", "route" : reverse('categories:category.index'),'active' : False});
        self.context['breadcrumbs'].append({"name" : self.context['action_title']+" Category", "route" : '','active' : True});


    def post(self, request, *args, **kwargs):

        category_id = request.POST.get('category_id', None)
        
        try:
            if category_id:
                self.action = 'Updated'
                category = get_object_or_404(Categories, id=category_id)
                if request.FILES.__len__() != 0:
                    if request.POST.get('category_icon', None) is None:
                        category.icon = request.FILES.get('category_icon')
                    if request.POST.get('image', None) is None:
                        category.image = request.FILES.get('category_image')
            else:
                category = Categories()
                if request.FILES.__len__() != 0:
                    if request.POST.get('category_icon', None) is None:
                        category.icon = request.FILES.get('category_icon')
                    if request.POST.get('image', None) is None:
                        category.image = request.FILES.get('category_image')

            

            category.name                   = request.POST.get('category_name').strip()
            category.description            = request.POST.get('description','').strip()

            category.parent_category_id     = None if request.POST.get('parent_category', None) == ''  else  int(request.POST.get('parent_category', None)) 
            category.type_id                = request.POST.get('group_type', None)
            category.is_active              = 0 if request.POST.get('category_status',0) == ''  else  int(request.POST.get('category_status',0)) 
            category.owner_id              = request.user.id

            category.save()
            
            messages.success(request, f"Data Successfully "+ self.action)

        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if category_id is not None:
                return redirect('categories:category.update', id = category_id )   
            return redirect('categories:category.create')

        return redirect('categories:category.index')





@method_decorator(login_required, name='dispatch')
class DestroyCategoryRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            category_ids = request.POST.getlist('ids[]')
            if category_ids:
                Categories.objects.filter(id__in=category_ids).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
        








