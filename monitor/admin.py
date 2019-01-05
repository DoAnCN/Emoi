from django.contrib import admin
from .models import Hardware, Network

# Register your models here.

class HardwareModelAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('id_agent','total','usage','free')

class NetworkModelAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('id_agent','tx_bytes','rx_bytes','n_scan_time')

admin.site.register(Hardware, HardwareModelAdmin)
admin.site.register(Network, NetworkModelAdmin)
