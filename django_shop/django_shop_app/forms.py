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

class SearchForm(forms.ModelForm):

    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
    # ratings = forms.IntegerField(required=False)

    class Meta:
        model = Product
        fields = ['title', 'description']   #, 'ratings']

