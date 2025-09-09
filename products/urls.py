from django.urls import path
from . import views

urlpatterns = [
    # Category CRUD URLs
    path('category/create/', views.create_category, name='create_category'),
    path('category/list/', views.list_category, name='list_category'),
    path('category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # Product CRUD URLs
    path('create/', views.create_product, name='create_product'),
    path('list/', views.list_product, name='list_product'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
]