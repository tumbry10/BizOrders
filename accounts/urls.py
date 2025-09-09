from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Registration URLs
    path('register/customer/', views.customer_register, name='customer_register'),
    path('register/sales-rep/', views.sales_rep_register, name='sales_rep_register'),
]