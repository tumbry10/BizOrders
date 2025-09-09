from django import forms
from .models import Category, Product

class ProductCategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Product Name' 
    }))
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Product Description' 
    }))


    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Product Name' 
    }))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
            'class': 'form-control text-center',
        }),
        empty_label="-- -Select Product's Category- --"
    )
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Product Description' 
    }))
    selling_price = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.0,
        widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Product Selling Price' 
    }))
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'selling_price']