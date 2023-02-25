from django import forms
from .models import Category, Subcategory, OrderItem


class SearchForm(forms.Form):

    CATEGORY = (
        (category['slug'], category['name']) for category in Category.objects.all().values('slug', 'name')
    )

    SUBCATEGORY = (
        (subcategory['slug'], subcategory['name']) for subcategory in Subcategory.objects.all().values('slug', 'name')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AddQuantityForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']
