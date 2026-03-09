from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderForm
from .models import Category, OrderItem, Product


def home(request):
    categories = Category.objects.all()[:6]
    popular_products = Product.objects.filter(is_popular=True)[:8]

    context = {
        "categories": categories,
        "popular_products": popular_products,
    }
    return render(request, "shop/home.html", context)


def catalog(request):
    products = Product.objects.select_related("category").all()
    categories = Category.objects.all()

    category_slug = request.GET.get("category")
    size = request.GET.get("size")
    sort = request.GET.get("sort")

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if size:
        products = products.filter(size=size)

    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-created_at")

    context = {
        "products": products,
        "categories": categories,
        "selected_category": category_slug,
        "selected_size": size,
        "selected_sort": sort,
    }
    return render(request, "shop/catalog.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "shop/product_detail.html", {"product": product})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    product_id_str = str(product.id)

    if product_id_str in cart:
        cart[product_id_str]["quantity"] += 1
    else:
        cart[product_id_str] = {
            "title": product.title,
            "price": str(product.price),
            "quantity": 1,
            "image": product.image.url if product.image else "",
            "slug": product.slug,
        }

    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart")


def cart_view(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total_price = Decimal("0.00")

    for product_id, item in cart.items():
        price = Decimal(item["price"])
        quantity = item["quantity"]
        subtotal = price * quantity
        total_price += subtotal

        cart_items.append({
            "id": product_id,
            "title": item["title"],
            "price": price,
            "quantity": quantity,
            "subtotal": subtotal,
            "image": item["image"],
            "slug": item["slug"],
        })

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, "shop/cart.html", context)


def update_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)
    action = request.POST.get("action")

    if product_id_str in cart:
        if action == "increase":
            cart[product_id_str]["quantity"] += 1
        elif action == "decrease":
            cart[product_id_str]["quantity"] -= 1

            if cart[product_id_str]["quantity"] <= 0:
                del cart[product_id_str]

    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart")


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart")


def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("catalog")

    cart_items = []
    total_price = Decimal("0.00")

    for product_id, item in cart.items():
        price = Decimal(item["price"])
        quantity = item["quantity"]
        subtotal = price * quantity
        total_price += subtotal

        cart_items.append({
            "id": product_id,
            "title": item["title"],
            "price": price,
            "quantity": quantity,
            "subtotal": subtotal,
            "image": item["image"],
        })

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_amount = total_price
            order.save()

            for product_id, item in cart.items():
                product = get_object_or_404(Product, id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item["quantity"],
                    price=Decimal(item["price"]),
                )

            request.session["cart"] = {}
            request.session.modified = True

            return redirect("order_success")
    else:
        form = OrderForm()

    context = {
        "form": form,
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, "shop/checkout.html", context)


def order_success(request):
    return render(request, "shop/order_success.html")

def about(request):
    return render(request, "shop/about.html")


def contacts(request):
    return render(request, "shop/contacts.html")