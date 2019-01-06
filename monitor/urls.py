from django.urls import path
from monitor import views


app_name='monitor'

urlpatterns = [
    path('dashboard/', views.dashboard),
    path('network/<slug:host_name>', views.network)
]