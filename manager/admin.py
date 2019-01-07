# -*- codding: utf-8 -*-
from __future__ import unicode_literals

import logging, os, subprocess

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
	actions = ('deployInstance', 'createDatabase', 'restoreDatabase')
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
				user = request.user.get_username()
				virtualenv_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
				output = subprocess.run([
					'{0}/bin/webautotool'.format(virtualenv_path),
					'remote', 'deploy', instance_info.name, user],
					stderr=subprocess.PIPE)
				output = output.stderr.decode('utf-8')

				if 'ERROR' or 'Error' in output:
					print(output)
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
					elif 'Remote branch' in output and 'not found' in output:
						messages.error(
							request, 'Version not exist'
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

	def createDatabase(self, request, queryset):
		logger = logging.getLogger(__name__)
		selected_list = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
		for selected in selected_list:
			instance_info = Instance.objects.get(id=selected)
			try:
				user = request.user.get_username()
				virtualenv_path = os.path.dirname(os.path.dirname(
					os.path.dirname(os.path.realpath(__file__))))
				output = subprocess.run([
					'{0}/bin/webautotool'.format(virtualenv_path),
					'remote', 'createdb', instance_info.name, user],
					stderr=subprocess.PIPE)
				output = output.stderr.decode('utf-8')
				if 'ERROR' or 'Error' in output:
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
					elif 'database exists' in output:
						messages.error(
							request, 'Database {0} has been exist '.format(instance_info.db_name)
						)
					else:
						messages.info(request,
									  'The database has been successfully created')
				elif 'has been completed' in output:
					messages.info(request,
								  'The database has been successfully created')

			except Exception as e:
				if str(e).startswith('[Errno '):
					messages.error(
						request, 'Create new database process uncompleted -'
								 ' Please contact your system administrator')
				logger.error(e)

	def restoreDatabase(self, request, queryset):
		logger = logging.getLogger(__name__)
		selected_list = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
		for selected in selected_list:
			instance_info = Instance.objects.get(id=selected)
			try:
				user = request.user.get_username()
				virtualenv_path = os.path.dirname(os.path.dirname(
				 	os.path.dirname(os.path.realpath(__file__))))
				#virtualenv_path = '/home/datlh/.local/share/virtualenvs/webkhoaluan/'
				output = subprocess.run([
					'{0}/bin/webautotool'.format(virtualenv_path),
					'remote', 'importdb', instance_info.name, user],
					stderr=subprocess.PIPE)
				output = output.stderr.decode('utf-8')
				if 'ERROR' or 'Error' in output:
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
					elif ' Unknown database' in output:
						messages.error(
							request, 'Database {0} has not been exist '
									 '- Please create first'.format(
								instance_info.db_name)
						)
					elif 'already exists' in output:
						messages.error(
							request, 'Database already restore before'.format(
								instance_info.db_name)
						)
					else:
						messages.info(request,
									  'The database has been successfully imported')
				elif 'has been completed' in output:
					messages.info(request,
								  'The database has been successfully imported')

			except Exception as e:
				if str(e).startswith('[Errno '):
					messages.error(
						request, 'Import database process uncompleted -'
								 ' Please contact your system administrator')
				logger.error(e)

	deployInstance.short_description = 'Deploy selected instances'
	createDatabase.short_description = 'Create empty database for selected instances'
	restoreDatabase.short_description = 'Restore exist database for selected instances'


class HostModelAdmin(admin.ModelAdmin):
	list_per_page = 10
	list_display = ('name', 'ip', 'num_of_inst', 'date_add','last_alive',
					'monitor',)
	list_filter = ('os', 'date_add',)
	readonly_fields = ('os', 'date_add', 'last_alive', 'num_of_inst',
					   'monitor', 'id_agent',)
	fieldsets = (
		(None, {'fields': ['name', ('ip', 'port',), 'os', 'num_of_inst',]}),
		('Monitoring Information', {'fields': ['id_agent', 'date_add', 'last_alive', 'monitor',]}),
	)
	actions = ('registerAgent',)

	def registerAgent(self, request, queryset):
		logger = logging.getLogger(__name__)
		selected_list = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
		for selected in selected_list:
			host_info = Host.objects.get(id=selected)
			try:
				user = request.user.get_username()
				virtualenv_path = os.path.dirname(os.path.dirname(
					os.path.dirname(os.path.realpath(__file__))))
				output = subprocess.run([
					'{0}/bin/webautotool'.format(virtualenv_path),
					'remote', 'register', host_info.name, user],
					stderr=subprocess.PIPE)
				output = output.stderr.decode('utf-8')
				if 'ERROR' or 'Error' in output:
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
        readonly_fields = ('name', )
        list_filter = ('project__name',)

admin.site.register(Instance, InstanceModelAdmin)
admin.site.register(Host, HostModelAdmin)
admin.site.register(Project, ProjectModelAdmin)
admin.site.register(Version, VersionModelAdmin)
