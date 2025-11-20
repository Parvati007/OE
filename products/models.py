from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('tshirt', 'T-Shirt'),
        ('jacket', 'Jacket'),
        ('shirt', 'Shirt'),
    ]
    
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_name_display())
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('products:category', args=[self.slug])


class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', '2XL'),
    ]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # CHANGED: Removed 'media/' prefix since MEDIA_ROOT already points to static/media/
    # Old: image = models.ImageField(upload_to='media/products/%Y/%m/%d/', blank=True)
    # New: Just use the relative path from MEDIA_ROOT
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    
    available_sizes = models.JSONField(default=list)  # ['S', 'M', 'L']
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['available', '-created']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)