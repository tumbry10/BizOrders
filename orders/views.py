from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .cart import Cart
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required

# Create your views here.
def sales_required(view_func):
    """Decorator to allow only sales reps"""
    def wrapper(request, *args, **kwargs):
        if request.user.user_role != 2:
            return redirect("customer_dashboard")  # or a 403 page
        return view_func(request, *args, **kwargs)
    return wrapper


def cart_detail(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'orders/cart_detail.html', context)

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect('customer_dashboard')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect("cart_detail")  # no checkout with empty cart

    if request.method == "POST":
        # 1. Create the Order
        order = Order.objects.create(
            customer=request.user,
            status="PENDING"
        )

        # 2. Create OrderItems
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["price"]
            )

        # 3. Save total_amount
        order.total_amount = cart.get_total_price()
        order.save()

        # 4. Clear cart
        cart.clear()

        return redirect("order_confirmation", order_id=order.id)

    return render(request, "orders/checkout.html", {"cart": cart})

@login_required
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id, customer=request.user)
    return render(request, "orders/order_confirmation.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    context = {"orders": orders}
    return render(request, "orders/my_orders.html", context)


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, customer=request.user)
    context = {"order": order}
    return render(request, "orders/order_detail.html", context)


@login_required
@sales_required
def sales_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ["PENDING", "PROCESSING", "READY", "CANCELLED"]:
            order.status = new_status
            order.sales_rep = request.user
            order.save()
        return redirect("sales_order_detail", order_id=order.id)

    return render(request, "orders/sales_order_detail.html", {"order": order})