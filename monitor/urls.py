from django.urls import path
from monitor import views


app_name='monitor'

urlpatterns = [
    path('dashboard/', views.dashboard),
    # path('test1/', views.test1)
    # path('agent/<slug:id_agent>', views.agent),
    # path('token-refresh/', refresh_jwt_token),
    # path('instances/<slug:name>', InstanceAPIView.as_view(),
    #      name='inst_detail'),
    # path('hosts/<slug:name>', HostAPIView.as_view(), name='host_detail_name'),
]