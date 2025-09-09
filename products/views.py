from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from .forms import ProductCategoryForm, ProductForm
from django.contrib import messages

# Create your views here.
#==================
#CATEGORY VIEWS 
#==================
def list_category(request):
    categories =  Category.objects.all()

    context =  {'categories': categories}
    return render(request, 'products/category_list.html', context)

def create_category(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.created_by = request.user
            cat.save()
            messages.success(request, 'Category created successfully!')
            return redirect('list_category')
    else:
        form = ProductCategoryForm()
    context = {'form': form}
    return render(request, 'products/category_form.html', context)

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category details updated successfully')
            return redirect('list_category')
    else:
        form = ProductCategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'products/category_form.html', context)

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, f"Category '{category.name}' deleted successfully.")
        return redirect("list_category")
    
    # if user hits this URL directly without POST
    messages.warning(request, "Delete action not allowed directly.")
    return redirect("list_category")


#==================
#PRODUCTS VIEWS 
#==================
def list_product(request):
    products =  Product.objects.all()

    context =  {'products': products}
    return render(request, 'products/products_list.html', context)

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, 'Product created successfully!')
            return redirect('list_product')
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'products/product_form.html', context)

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product details updated successfully')
            return redirect('list_product')
    else:
        form = ProductForm(instance=product)
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/product_form.html', context)

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, f"Product '{product.name}' deleted successfully.")
        return redirect("list_product")
    
    # if user hits this URL directly without POST
    messages.warning(request, "Delete action not allowed directly.")
    return redirect("list_product")
