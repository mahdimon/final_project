from django.contrib import admin
from .models import Product, Category, Discount
from django.contrib import admin
from .models import Product, Feature

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1 

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock")
    inlines = [FeatureInline]  

admin.site.register(Product, ProductAdmin)
admin.site.register(Feature)
admin.site.register(Category)
admin.site.register(Discount)

# Register your models here.
