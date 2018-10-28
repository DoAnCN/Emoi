# -*- codding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Instance, Host, Project, Version
from .forms import InstanceForm

from inline_actions.admin import InlineActionsModelAdminMixin,\
	InlineActionsMixin

class InstanceInline(InlineActionsMixin,
                    admin.TabularInline):
	model = Instance
	inline_actions = ['deploy']
	list_display = ('name', 'db_name' , 'usr_deployed', 'status',)

	def has_add_permission(self, request, obj):
		return False

	def deploy(self, request, obj, parent_obj=None):
		print("============================")
		# url = reverse(
        #     'admin:{}_{}_change'.format(
        #         obj._meta.app_label,
        #         obj._meta.model_name,
        #     ),
        #     args=(obj.pk,)
        # )
		# return redirect(url)
	deploy.short_description = _("Deploy")

# Register your models here.
class InstanceModelAdmin(admin.ModelAdmin):
	form = InstanceForm
	list_per_page = 10
	list_display = ('name', 'db_name', 'domain', 'project', 'host'
    	, 'usr_deployed', 'status', 'latest_deploy',)
	list_filter = ('status', 'project__name', 'host__name', 'usr_deployed',)
	readonly_fields = ('usr_deployed', 'status', 'latest_deploy', )
	actions = ['deploy',]
	fieldsets = [
		(None, 					{'fields': ['name', 'db_name', 'domain',
											  'host']}),
		('Project Information', {'fields': ['project', 'project_ver']}),
		('Status',				{'fields': ['usr_deployed', 'status',
											  'latest_deploy']}),
	]

	def deploy(self, request, queryset):
		print('========{}======='.format(request.user))


	deploy.short_description = "Deploy instances"

class HostModelAdmin(admin.ModelAdmin):
	list_per_page = 10
	list_display = ('name', 'ip', 'port', 'os', )
	list_filter = ('os', )
	readonly_fields = ('num_of_inst', )

class ProjectModelAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
	list_per_page = 10
	list_display = ('name', 'url')
	inlines = [InstanceInline]

class VersionModelAdmin(admin.ModelAdmin):
	list_per_page = 10
	list_display = ('name', 'project',)
	list_filter = ('project__name',)

admin.site.site_header =  'EmOi'
admin.site.site_title = 'Emoi Admin Site'
admin.site.register(Instance, InstanceModelAdmin)
admin.site.register(Host, HostModelAdmin)
admin.site.register(Project, ProjectModelAdmin)
admin.site.register(Version, VersionModelAdmin)
