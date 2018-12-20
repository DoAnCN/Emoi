#from django import forms
#from .models import Instance, Version

#class InstanceForm(forms.ModelForm):
#	class Meta:
#		model = Instance
#		fields = ["project_ver", "project"]
#
#	def __init__(self, *args, **kwargs):
#		super(InstanceForm, self).__init__(*args, **kwargs)
#		instance = kwargs.get('instance')
#		if instance:
#			self.fields['project_ver'].queryset = Version.objects.filter(
#					project=instance.project)
