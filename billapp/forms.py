from django import forms

from .models import Item,Company,User,Item,Receiver,ShipTo,Bill

from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):

    class Meta:

        model=User

        fields=["username","email","phone","password1","password2"]

        widgets={
            
            "username":forms.TextInput(attrs={"class":"form-control"}),
            
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            
            "password1":forms.TextInput(attrs={"class":"form-control"}),
            
            "password2":forms.TextInput(attrs={"class":"form-control"}),
            
            "phone":forms.NumberInput(attrs={"class":"form-control"}),
            
                 } 
        
class SignInForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    password=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

class CompanyDetailForm(forms.ModelForm):

    class Meta:

        model=Company

        fields=["company_logo","company_name","company_address","city","state","company_email","company_mobile","postal_code"]

        widgets={

            "company_logo":forms.FileInput(attrs={'class': 'form-control-file'}),

            "company_name":forms.TextInput(attrs={"class":"form-control"}),

            "company_address":forms.TextInput(attrs={"class":"form-control"}),

            "city":forms.TextInput(attrs={"class":"form-control"}),
            
            "state":forms.TextInput(attrs={"class":"form-control"}),
            
            "company_email":forms.EmailInput(attrs={"class":"form-control"}),
            
            # "company_GSTIN":forms.TextInput(attrs={"class":"form-control"}),
            
            "company_mobile":forms.NumberInput(attrs={"class":"form-control"}),

            "postal_code":forms.TextInput(attrs={"class":"form-control"}),
            
                 }
        
class ItemForm(forms.ModelForm):

    class Meta:

        model=Item

        fields=["items","quantity","rate","tax","amount"]

class ReceiverForm(forms.ModelForm):

    class Meta:

        model=Receiver

        fields=["receiver_name","receiver_address","receiver_email","receiver_mobile"]

        widgets={

            "receiver_name":forms.TextInput(attrs={"class":"form-control"}),

            "receiver_address":forms.TextInput(attrs={"class":"form-control"}),
                        
            "receiver_email":forms.EmailInput(attrs={"class":"form-control"}),
            
            # "company_GSTIN":forms.TextInput(attrs={"class":"form-control"}),
            
            "receiver_mobile":forms.NumberInput(attrs={"class":"form-control"}),
            
                 }
        
class ShipToForm(forms.ModelForm):

    class Meta:

        model=ShipTo

        fields=["shipping_name","shipping_address","shipping_email","shipping_mobile"]

        widgets={

            "shipping_name":forms.TextInput(attrs={"class":"form-control"}),

            "shipping_address":forms.TextInput(attrs={"class":"form-control"}),
                        
            "shipping_email":forms.EmailInput(attrs={"class":"form-control"}),
            
            # "company_GSTIN":forms.TextInput(attrs={"class":"form-control"}),
            
            "shipping_mobile":forms.NumberInput(attrs={"class":"form-control"}),
            
                 }

