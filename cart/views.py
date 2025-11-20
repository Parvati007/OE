from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST, sizes=product.available_sizes)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            size=cd['size'],
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
    return redirect('cart:detail')


def cart_remove(request, product_id, size):
    cart = Cart(request)
    cart.remove(product_id, size)
    return redirect('cart:detail')


def cart_detail(request):
    cart = Cart(request)
    
    # Update cart items with forms for quantity update
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True},
            sizes=[item['size']]
        )
    
    return render(request, 'cart/detail.html', {'cart': cart})