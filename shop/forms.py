from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    delivery_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )
    delivery_time = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"})
    )

    class Meta:
        model = Order
        fields = [
            "full_name",
            "phone",
            "email",
            "address",
            "delivery_date",
            "delivery_time",
            "card_text",
            "payment_method",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Введите ФИО"}),
            "phone": forms.TextInput(attrs={"placeholder": "Введите телефон"}),
            "email": forms.EmailInput(attrs={"placeholder": "Введите email"}),
            "address": forms.Textarea(attrs={"placeholder": "Введите адрес доставки", "rows": 3}),
            "card_text": forms.Textarea(attrs={"placeholder": "Текст для открытки", "rows": 3}),
        }