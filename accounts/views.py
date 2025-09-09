from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm, EmailAuthenticationForm, SalesRepCreationForm
from .models import CustomUser


def customer_register(request):
    #=======================================
    #Allow customers to register themselves
    #=======================================
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_role = 3  # Force customer role
            user.save()
            
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-set the role to customer and make it readonly
        form = CustomUserCreationForm(initial={'user_role': 3})
    context =  {'form': form}
    return render(request, 'accounts/customer_register.html', context)


@login_required
def sales_rep_register(request):
    #=======================================================
    # Allow only SystAdmin to register Sales Representatives
    #=======================================================
    # Check if the logged-in user is a SystAdmin
    if request.user.user_role != 1:
        messages.error(request, 'Only System Administrators can register Sales Representatives.')
        return HttpResponseForbidden('Access denied. Only System Administrators can register Sales Representatives.')
    
    if request.method == 'POST':
        form = SalesRepCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_role = 2  # Force sales rep role
            user.save()
            
            messages.success(request, f'Sales Representative {user.email} has been successfully registered.')
            return redirect('sales_rep_list')  # Redirect to a list view or dashboard
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SalesRepCreationForm()
    context = {'form': form}
    return render(request, 'accounts/sales_rep_register.html', context)


def user_login(request):
    #===========================================
    #User login view using email authentication
    #===========================================
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect if already logged in
    
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # 'username' field contains email
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.email}!')
                
                # Redirect based on user role
                if user.user_role == 1:  # SystAdmin
                    return redirect('admin_dashboard')
                elif user.user_role == 2:  # SalesRep
                    return redirect('sales_dashboard')
                else:  # Customer
                    return redirect('customer_dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmailAuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')


@login_required
def dashboard(request):
    if request.user.user_role == 1:  # SystAdmin
        return redirect('admin_dashboard')
    elif request.user.user_role == 2:  # SalesRep
        return redirect('sales_dashboard')
    else:  # Customer
        return redirect('customer_dashboard')
