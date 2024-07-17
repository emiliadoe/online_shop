from django import forms
from .models import Product, Rating, Report


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

        fields = ['text', 'rating']

        widgets = {
            'user': forms.HiddenInput(),
            'product': forms.HiddenInput(),
        }

class SearchForm(forms.ModelForm):

    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
    rating = forms.IntegerField(required=False)

    class Meta:
        model = Product
        fields = ['title', 'description', 'rating']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'description']

        widgets = {
            'reason': forms.Select(choices=Report.REASON_CHOICES),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional: Add any additional information'}),
        }

class EditRatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['text', 'rating']

        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Sterne') for i in range(1, 6)]),
            'text': forms.Textarea(attrs={'rows': 3}),
        }