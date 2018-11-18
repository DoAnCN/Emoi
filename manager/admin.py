# -*- codding: utf-8 -*-
from __future__ import unicode_literals

import logging
import subprocess

from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _

from .models import Instance, Host, Project, Version
from .forms import InstanceForm

from inline_actions.admin import InlineActionsModelAdminMixin,\
	InlineActionsMixin


class InstanceInline(InlineActionsMixin, admin.TabularInline):
	model = Instance
	inline_actions = ['deploy']
	list_display = ('name', 'db_name' , 'usr_deployed', 'status',)
	readonly_fields = ('usr_deployed', 'status', 'latest_deploy',)

	def has_add_permission(self, request, obj):
		return False

	def deploy(self, request, obj, parent_obj=None):
		print('============================')
		# url = reverse(
        #     'admin:{}_{}_change'.format(
        #         obj._meta.app_label,
        #         obj._meta.model_name,
        #     ),
        #     args=(obj.pk,)
        # )
		# return redirect(url)
	deploy.short_description = _('Deploy')

# Register your models here.
class InstanceModelAdmin(admin.ModelAdmin):
	form = InstanceForm
	list_per_page = 10
	list_display = ('name', 'db_name', 'domain', 'project', 'host'
					, 'usr_deployed', 'status', 'latest_deploy',)
	list_filter = ('status', 'project__name', 'host__name', 'usr_deployed',
				   'type')
	readonly_fields = ('usr_deployed', 'status', 'latest_deploy', )
	actions = ('deployInstance',)
	fieldsets = (
		(None, {'fields': ['name', 'db_name', 'domain', 'host', 'type']}),
		('Project Information', {'fields': ['project', 'project_ver']}),
		('Status', {'fields': ['usr_deployed', 'status', 'latest_deploy']}),
	)

	def deployInstance(self, request, queryset):
		logger = logging.getLogger(__name__)
		selected_list = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
		for selected in selected_list:
			instance = Instance.objects.get(id=selected)
			try:
				# user = request.user.get_username()
				output = subprocess.run(['/home/datlh/.local/share/virtualenvs/webkhoaluan/bin/webautotool',
								'remote', 'deploy', instance.name,],
										stderr=subprocess.PIPE)
				output = output.stderr.decode('utf-8')
				if 'Error' in output:
					output = output[output.find('STDERR')+7:]
					logger.error(output.strip())
					if 'No route to host' in output:
						messages.error(
							request, 'No route to host -'
									 ' Please check ip address of host '
									 'or Host does not exist ')
					elif 'Permission denied' in output:
						messages.error(
							request, 'Permission denied - '
									 'Please check permission with system admin'
						)

			except Exception as e:
				if str(e).startswith('[Errno '):
					messages.error(
						request,'Deployment process uncompleted -'
								' Please contact your system administrator')
				logger.error(e)

	deployInstance.short_description = 'Deploy selected instances'


class HostModelAdmin(admin.ModelAdmin):
	list_per_page = 10
	list_display = ('name', 'ip', 'port', 'os', 'is_agent',)
	list_filter = ('os', 'is_agent',)
	readonly_fields = ('num_of_inst', 'is_agent', 'os')
	actions = ('buildHost','registerAgent')

	def buildHost(self, request, queryset):
		pass

	def registerAgent(self, request, queryset):
		pass

	buildHost.short_description = 'Build selected hosts'
	registerAgent.short_description = 'Register selected hosts as agent'

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
