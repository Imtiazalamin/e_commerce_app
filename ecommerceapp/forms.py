from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Product, User  # Custom user import

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image', 'available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UserRegisterForm(UserCreationForm):
    user_type_choices = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    user_type = forms.ChoiceField(choices=user_type_choices, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password1', 'password2']

        
