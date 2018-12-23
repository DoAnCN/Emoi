from django.urls import path

from .views import InstanceAPIView, HostAPIView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


app_name = 'api'

urlpatterns = [
    path('auth/token/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('instances/<slug:name>', InstanceAPIView.as_view(),
         name='inst_detail'),
    path('hosts/<slug:name>', HostAPIView.as_view(), name='host_detail_name'),
]
