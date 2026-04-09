from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('chart-data/', views.chart_data, name='chart_data'),
    path('export/<str:report_type>/', views.export_csv, name='export_csv'),
]
