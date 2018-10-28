from django.urls import path

from .views import InstanceAPIView, HostAPIView

app_name = 'api'

urlpatterns = [
    path('instances/<slug:name>', InstanceAPIView.as_view(), name='inst_detail'),
    path('hosts/<slug:name>', HostAPIView.as_view(), name='host_detail_name'),
    # path('hosts/<int:pk>', HostAPIView.as_view(), name='host_detail_pk')
]
