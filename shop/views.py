from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from .cart import Cart
from .forms import CheckoutForm
from django.urls import reverse

def product_list(request):
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'shop/product_detail.html', {'product': product})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('shop:product_list')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total = cart.get_total_price()
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return redirect(reverse('shop:order_success', args=[order.id]))
    else:
        form = CheckoutForm()
    return render(request, 'shop/checkout.html', {'cart': cart, 'form': form})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})

# Create your views here.
