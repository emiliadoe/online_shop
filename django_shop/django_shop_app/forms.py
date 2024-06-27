from django import forms
from .models import Product, Rating


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = ['title', 'category', 'price']

        widgets = {
            'type': forms.Select(choices=Product.TYPE),
            'user': forms.HiddenInput(),
        }


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating

        fields = ['text']

        widgets = {
            'user': forms.HiddenInput(),
            'product': forms.HiddenInput(),
        }

