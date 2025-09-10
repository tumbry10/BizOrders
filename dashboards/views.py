from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import CustomUser
from products.models import Product
from orders.cart import Cart

# Create your views here.
@login_required
def dashboard(request):
    if request.user.user_role == 1:  # SystAdmin
        return redirect('admin_dashboard')
    elif request.user.user_role == 2:  # SalesRep
        return redirect('sales_dashboard')
    else:  # Customer
        return redirect('customer_dashboard')


@login_required
def admin_dashboard(request):
    if request.user.user_role != 1:
        messages.error(request, 'Access denied.')
        return HttpResponseForbidden('Access denied.')
    
    # Get some statistics for the admin
    total_customers = CustomUser.objects.filter(user_role=3).count()
    total_sales_reps = CustomUser.objects.filter(user_role=2).count()
    recent_customers = CustomUser.objects.filter(user_role=3).order_by('-created_at')[:5]
    
    context = {
        'total_customers': total_customers,
        'total_sales_reps': total_sales_reps,
        'recent_customers': recent_customers,
    }
    
    return render(request, 'dashboards/admin_dashboard.html', context)


@login_required
def sales_dashboard(request):
    if request.user.user_role != 2:
        messages.error(request, 'Access denied.')
        return HttpResponseForbidden('Access denied.')
    
    context = {
        'user': request.user,
    }
    
    return render(request, 'dashboards/sales_dashboard.html', context)


@login_required
def customer_dashboard(request):
    if request.user.user_role != 3:
        messages.error(request, 'Access denied.')
        return HttpResponseForbidden('Access denied.')
    
    products = Product.objects.filter(is_active=True)
    context = {
        'user': request.user,
        'products': products,
    }
    
    return render(request, 'dashboards/customer_dashboard.html', context)


@login_required
def sales_rep_list(request):
    if request.user.user_role != 1:
        messages.error(request, 'Access denied.')
        return HttpResponseForbidden('Access denied.')
    
    sales_reps = CustomUser.objects.filter(user_role=2).order_by('-created_at')
    
    context = {
        'sales_reps': sales_reps,
    }
    
    return render(request, 'dashboards/sales_rep_list.html', context)