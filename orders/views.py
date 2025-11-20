from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm

@login_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('products:list')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    size=item['size'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            cart.clear()
            return render(request, 'orders/created.html', {'order': order})
    else:
        # Pre-fill form with user data if available
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'orders/create.html', {
        'cart': cart,
        'form': form
    })


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})