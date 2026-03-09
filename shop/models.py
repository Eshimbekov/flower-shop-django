from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("Slug", unique=True, blank=True)
    image = models.ImageField("Фото категории", upload_to="categories/", blank=True, null=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    SIZE_CHOICES = [
        ("small", "Малый"),
        ("medium", "Средний"),
        ("large", "Большой"),
    ]

    STATUS_CHOICES = [
        ("in_stock", "В наличии"),
        ("pre_order", "Под заказ"),
    ]

    OCCASION_CHOICES = [
        ("birthday", "День рождения"),
        ("wedding", "Свадьба"),
        ("march8", "8 марта"),
        ("anniversary", "Годовщина"),
        ("love", "Любовь"),
        ("other", "Другое"),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
    )
    title = models.CharField("Название", max_length=200)
    slug = models.SlugField("Slug", unique=True, blank=True)
    image = models.ImageField("Фото", upload_to="products/")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    description = models.TextField("Описание", blank=True)
    composition = models.TextField("Состав букета", blank=True)
    size = models.CharField("Размер", max_length=20, choices=SIZE_CHOICES, default="medium")
    occasion = models.CharField("Повод", max_length=30, choices=OCCASION_CHOICES, default="other")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="in_stock")
    article = models.CharField("Артикул", max_length=50, unique=True)
    is_popular = models.BooleanField("Популярный", default=False)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("assembling", "В сборке"),
        ("delivering", "Доставляется"),
        ("completed", "Выполнен"),
        ("cancelled", "Отменен"),
    ]

    PAYMENT_CHOICES = [
        ("cash", "Наличными"),
        ("card", "Картой"),
        ("transfer", "Переводом"),
    ]

    full_name = models.CharField("ФИО заказчика", max_length=255)
    phone = models.CharField("Телефон", max_length=30)
    email = models.EmailField("Email", blank=True)
    address = models.TextField("Адрес доставки")
    delivery_date = models.DateField("Дата доставки")
    delivery_time = models.TimeField("Время доставки")
    card_text = models.TextField("Текст открытки", blank=True)
    payment_method = models.CharField("Способ оплаты", max_length=20, choices=PAYMENT_CHOICES, default="cash")
    total_amount = models.DecimalField("Итоговая сумма", max_digits=10, decimal_places=2, default=0)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField("Количество", default=1)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"