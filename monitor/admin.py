from django.contrib import admin
from .models import BasicInfo
from .models import Hardware
from .models import Network

# Register your models here.
class BasicInfoModelAdmin(admin.ModelAdmin):
    list_per_page = 10
    # readonly_fields = ('id_agent', 'version', 'arch', 'os_version', )
    list_display = ('id_agent','sys_name', 'arch','os_name')
# 	list_filter = ('project__name',)
#   sys_name=models.TextField(max_length=255)
#     version = models.TextField(max_length=255)
#     arch = models.TextField(max_length=255)
#     os_name =models.TextField(max_length=255)
#     os_version

class HardwareModelAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('id_agent','total','usage','free')

class NetworkModelAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('id_agent','tx_bytes','rx_bytes','n_scan_time')

admin.site.site_header =  'EmOi'
admin.site.site_title = 'Emoi Admin Site'
admin.site.register(BasicInfo, BasicInfoModelAdmin)
admin.site.register(Hardware, HardwareModelAdmin)
admin.site.register(Network, NetworkModelAdmin)