from django.urls import path
from . import views

app_name = 'visitors'

urlpatterns = [
    path('', views.visitor_list, name='visitor_list'),
    path('new/', views.visitor_create, name='visitor_create'),
    path('<int:pk>/checkout/', views.visitor_checkout, name='visitor_checkout'),
]
