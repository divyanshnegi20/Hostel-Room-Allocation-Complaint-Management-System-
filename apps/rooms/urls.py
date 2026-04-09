from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('my-room/', views.my_room, name='my_room'),
    path('create/', views.room_create, name='room_create'),
    path('<int:pk>/', views.room_detail, name='room_detail'),
    path('<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('<int:pk>/delete/', views.room_delete, name='room_delete'),
    path('allocate/<int:bed_id>/', views.allocate_bed, name='allocate_bed'),
    path('deallocate/<int:allocation_id>/', views.deallocate_bed, name='deallocate_bed'),
]
