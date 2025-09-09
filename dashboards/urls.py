from django.urls import path
from . import views

urlpatterns = [ # Dashboard URLs
    path('', views.dashboard, name='dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('sales/', views.sales_dashboard, name='sales_dashboard'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    
    # Admin-specific URLs
    path('admin/sales-reps/', views.sales_rep_list, name='sales_rep_list'),
]