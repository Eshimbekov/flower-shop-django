from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),

    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:product_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),

    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.order_success, name="order_success"),

    
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
]