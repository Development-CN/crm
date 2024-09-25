from django import forms


class OrderForm(forms.Form):
    order_n = forms.CharField(label="Your name", max_length=20)
