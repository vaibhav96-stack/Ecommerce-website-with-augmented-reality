from django.contrib import admin
from .models import Category,ProductForm,Cart,Purchase

admin.site.register(Category)
admin.site.register(ProductForm)
admin.site.register(Cart)
admin.site.register(Purchase)
