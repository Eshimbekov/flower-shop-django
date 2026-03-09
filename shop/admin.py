from django.contrib import admin
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("order", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "price", "size", "status", "is_popular", "created_at")
    list_filter = ("category", "size", "status", "is_popular")
    search_fields = ("title", "article", "description")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("price", "status", "is_popular")
    autocomplete_fields = ("category",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "delivery_date", "delivery_time", "total_amount", "status", "created_at")
    list_filter = ("status", "payment_method", "delivery_date")
    search_fields = ("full_name", "phone", "email", "address")
    list_editable = ("status",)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price")
    search_fields = ("product__title", "order__full_name")