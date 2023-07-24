from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Images
from django.forms import ModelForm
from django import forms

class CreateCustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['seller']

class ImageForm(ModelForm):
    images = forms.ImageField(label='')    
    class Meta:
        model = Images
        fields = ('images', )

    