from django import forms
from django_shop_app.models import Product, Rating


class RatingEditForm(forms.ModelForm):

    class Meta:

        model = Rating
        fields = ['text']

        widgets = {
            'comment_id': forms.HiddenInput(),
        }



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'price', 'description', 'image']
