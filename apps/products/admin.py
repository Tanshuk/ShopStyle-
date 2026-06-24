from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'original_price', 'gender', 'stock', 'is_featured', 'is_on_sale']
    list_filter = ['category', 'gender', 'is_featured', 'is_on_sale', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price')
        }),
        ('Product Details', {
            'fields': ('gender', 'stock', 'image')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_on_sale')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
