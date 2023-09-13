from django import forms
from django.contrib.auth.models import User
from .models import Category, Dish
 
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
        def clean_username(self):
            username = self.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('Username already exists')
            return username

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'

class DishForm(forms.ModelForm):

    class Meta:
        model = Dish
        fields = '__all__'