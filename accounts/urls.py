from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Registration URLs
    path('register/customer/', views.customer_register, name='customer_register'),
    path('register/sales-rep/', views.sales_rep_register, name='sales_rep_register'),
    
    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('sales/dashboard/', views.sales_dashboard, name='sales_dashboard'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    
    # Admin-specific URLs
    path('admin/sales-reps/', views.sales_rep_list, name='sales_rep_list'),
]