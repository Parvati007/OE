from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product

def home(request):
    featured_products = Product.objects.filter(available=True)[:6]
    return render(request, 'core/home.html', {
        'featured_products': featured_products
    })

def about(request):
    return render(request, 'core/about.html')

@login_required
def chatbot(request):
    """Dedicated chatbot page"""
    return render(request, 'core/chatbot.html')