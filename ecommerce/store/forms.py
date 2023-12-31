from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product
from django.forms import ModelForm

class CreateCustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['seller']
