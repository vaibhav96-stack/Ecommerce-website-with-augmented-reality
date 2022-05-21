from django.contrib.auth.hashers import make_password
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms

class UserProfileForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','username','email','password1','password2']
        labels = {'first_name': '', 'last_name': '', 'username': '', 'email': '', 'password1': '', 'password2': ''}
        help_texts = {'username': '', 'password1': '', 'password2':''}

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True


class UserLoginForm(AuthenticationForm):
    pass


class AddressForm(forms.Form):
    address = forms.CharField(max_length=250,required=True)
    mobno = forms.RegexField(regex=r'^\+?1?\d{10,10}$',required=True)

    class Meta:
        fields = ['address','mobno']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'placeholder': 'Shipping Address'})
        self.fields['mobno'].widget.attrs.update({'placeholder': 'Mobile Number'})
        self.fields['address'].label = ''
        self.fields['mobno'].label = ''