from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .cart import Cart
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required

# Create your views here.
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