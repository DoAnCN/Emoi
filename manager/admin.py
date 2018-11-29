# -*- codding: utf-8 -*-
from __future__ import unicode_literals

import logging
import subprocess

from django.contrib import admin, messages

from .models import Instance, Host, Project, Version
from .forms import InstanceForm


# Register your models here.
class InstanceModelAdmin(admin.ModelAdmin):
	form = InstanceForm
	list_per_page = 10
	list_display = ('name', 'db_name', 'domain', 'project', 'host'
					, 'usr_deployed', 'status', 'latest_deploy',)
	list_filter = ('status', 'project__name', 'host__name', 'usr_deployed',
				   'type',)
	readonly_fields = ('usr_deployed', 'status', 'latest_deploy', )
	actions = ('deployInstance',)
	fieldsets = (
		(None, {'fields': [('name', 'host'), ('db_name', 'type'), 'domain',]}),
		('Project Information', {'fields': [('project', 'project_ver'),]}),
		('Status', {'fields': ['usr_deployed', 'status', 'latest_deploy',]}),
	)

	def deployInstance(self, request, queryset):
		logger = logging.getLogger(__name__)
		selected_list = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
		for selected in selected_list:
			instance_info = Instance.objects.get(id=selected)
			try:
				# user = request.user.get_username()
				output = subprocess.run([
					'/home/datlh/.local/share/virtualenvs/webkhoaluan/bin/webautotool',
					'remote', 'deploy', instance_info.name,],
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
				elif 'has been completed' in output:
					messages.info(request,
								  'The deployment process has been completed')

			except Exception as e:
				if str(e).startswith('[Errno '):
					messages.error(
						request,'Deployment process uncompleted -'
								' Please contact your system administrator')
				logger.error(e)

	deployInstance.short_description = 'Deploy selected instances'


class HostModelAdmin(admin.ModelAdmin):
	list_per_page = 10
	list_display = ('name', 'ip', 'num_of_inst', 'date_add','last_alive',
					'monitor',)
	list_filter = ('os', 'date_add',)
	readonly_fields = ('os', 'date_add', 'last_alive', 'num_of_inst',
					   'monitor',)
	fieldsets = (
		(None, {'fields': ['name', 'port', 'ip', 'os', 'num_of_inst',]}),
		('Monitoring Information', {'fields': ['date_add', 'last_alive',
											   'monitor',]}),
	)
	actions = ('registerAgent',)

	def registerAgent(self, request, queryset):
		logger = logging.getLogger(__name__)
		selected_list = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
		for selected in selected_list:
			host_info = Host.objects.get(id=selected)
			try:
				output = subprocess.run([
					'/home/datlh/.local/share/virtualenvs/webkhoaluan/bin/webautotool',
					'remote', 'register', host_info.name, ],
					stderr=subprocess.PIPE)
				output = output.stderr.decode('utf-8')
				if 'Error' in output:
					output = output[output.find('STDERR') + 7:]
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
				elif 'has been completed' in output:
					messages.info(request,
							'The register agent process has been completed')

			except Exception as e:
				if str(e).startswith('[Errno '):
					messages.error(
						request, 'Registration process uncompleted -'
								 ' Please contact your system administrator')
				logger.error(e)

	registerAgent.short_description = 'Register selected hosts as agent'

class ProjectModelAdmin(admin.ModelAdmin):
	list_per_page = 10
	list_display = ('name', 'url',)

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
