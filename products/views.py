from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category
from cart.forms import CartAddProductForm

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        qs = Product.objects.filter(available=True).select_related('category')
        category = self.kwargs.get('category_slug')
        if category:
            qs = qs.filter(category__slug=category)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        if self.kwargs.get('category_slug'):
            context['current_category'] = get_object_or_404(
                Category, slug=self.kwargs['category_slug']
            )
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Product.objects.filter(available=True).select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm(
            sizes=self.object.available_sizes
        )
        return context