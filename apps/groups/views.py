from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Q
from apps.groups.models import Groups
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages


@method_decorator(login_required, name='dispatch')
class GroupsIndexView(View):
    def __init__(self):
        self.context = {"breadcrumbs" : []}
        self.template = 'group/groups.html'
        self.context['title'] = 'Groups'
        self.generateBreadcrumbs();

    def get(self, request, *args, **kwargs):
        
        return render(request, self.template, self.context)


    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Groups", "route" : '','active' : True});




class LoadShopsDatatable(BaseDatatableView):
    model = Groups
    
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
                'icon' : escape(item.icon.url),
                'is_active' : escape(item.is_active),
                'created_date' : item.created_date.strftime("%Y-%m-%d %H:%M:%S"),
                'modified_date' : item.modified_date.strftime("%Y-%m-%d %H:%M:%S"),
            })
        return json_data




@method_decorator(login_required, name='dispatch')
class GroupsCreateOrUpdatetView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = 'Created'
        self.context = {'breadcrumbs': []}
        self.context['title'] = 'Group'
        self.context['action_title'] = 'Create'
        self.template = 'group/create-or-update-groups.html'
        
        
    def get(self, request, *args, **kwargs):
        id = kwargs.pop('id', None)
        if id:
            self.context['group'] = get_object_or_404(Groups, id=id)
        self.generateBreadcrumbs()
        return render(request,self.template, self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Groups", "route" : reverse('groups:groups.index'),'active' : False});
        self.context['breadcrumbs'].append({"name" : self.context['action_title']+" Groups", "route" : '','active' : True});

    def post(self, request, *args, **kwargs):
        
        try:
            group_id = request.POST.get('group_id', None)
            
            if group_id:
                self.action = 'Updated'
                group = get_object_or_404(Groups, id=group_id)
                if request.FILES.__len__() != 0:
                    if request.POST.get('group_icon', None) is None:
                        group.icon = request.FILES.get('group_icon')
                    if request.POST.get('group_banner_image', None) is None:
                        group.banner = request.FILES.get('group_banner_image')
            else:
                group = Groups()
                if request.FILES.__len__() != 0:
                    if request.POST.get('group_icon', None) is None:
                        group.icon = request.FILES.get('group_icon')
                    if request.POST.get('group_banner_image', None) is None:
                        group.banner = request.FILES.get('group_banner_image')

            group.name         = request.POST.get('group_name').strip()
            
            group.is_main_homepage = True if request.POST.get('is_main_homepage',0) == 'on' else  request.POST.get('is_main_homepage',0) 

            group.layout           = int(request.POST.get('layout-builder', 0))
            
            group.is_active        = 0 if request.POST.get('group_status',0) == ''  else  int(request.POST.get('group_status',0)) 

            group.owner_id  = request.user.id
            group.save()
            
            messages.success(request, f"Data Successfully "+ self.action)

        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            return redirect('groups:groups.create')

        return redirect('groups:groups.index')





@method_decorator(login_required, name='dispatch')
class DestroyGroupRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            group_ids = request.POST.getlist('ids[]')
            if group_ids:
                Groups.objects.filter(id__in=group_ids).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
        








