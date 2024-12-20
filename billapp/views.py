from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from django.views.generic.edit import FormView
from .forms import ItemForm, SignUpForm, SignInForm, CompanyDetailForm, ReceiverForm, ShipToForm
from django.contrib.auth import authenticate,login,logout
from .models import Item,Company
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas 
from django.core.mail import EmailMessage
from django.http import FileResponse
from reportlab.lib.units import inch
import io
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Item, Receiver, ShipTo
from io import BytesIO


    
class SignUpView(View):

    template_name="signup.html"

    form_class=SignUpForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_data=request.POST 

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("signin")

        print("account creation failed")

        return render(request,self.template_name,{"form":form_instance})

class SignInView(View):

    template_name="signin.html"

    form_class=SignInForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_data=request.POST 

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_obj=authenticate(request,username=uname,password=pwd)

            if user_obj:

                login(request,user_obj)

                try:

                    if request.user.company:

                        return redirect("index")

                except:

                    return redirect("company-detail")

        return render(request,self.template_name,{"form":form_instance})

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    
class CompanyDetailView(View):

    template_name="company_detail.html"

    form_class=CompanyDetailForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data,files=request.FILES)

        if form_instance.is_valid():

            company_object=form_instance.save(commit=False)

            company_object.company_obj=request.user

            form_instance.save()

            return redirect("index")
        
        print("company detail creation failed")
        
        return render(request,self.template_name,{"form":form_instance})
    
class index(View):

    template_name="index.html"

    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)
    
# class GenerateBillReceiptView(View):

#     template_name = 'generate_bill.html'

#     item_form_class=ItemForm

#     receiver_form_class=ReceiverForm

#     shipto_form_class=ShipToForm

#     def get(self,request,*args,**kwargs):

#         item_form_instance=self.item_form_class()

#         receiver_form_instance=self.receiver_form_class()

#         shipto_form_instance=self.shipto_form_class()

#         qs=Item.objects.filter(items_obj=request.user.company) 

#         company_obj=Company.objects.get(company_obj=(request.user))

#         return render(request,self.template_name,{"data":qs,"item_form":item_form_instance,"company":company_obj,"receiver_form":receiver_form_instance, "shipto_form":shipto_form_instance })
    
#     def post(self,request,*args,**kwargs):

#         form_data=request.POST

#         item_form_instance=self.item_form_class(form_data)

#         # receiver_form_instance=self.receiver_form_class(form_data)

#         # shipto_form_instance=self.shipto_form_class(form_data)

#         # form_instance=self.form_class(form_data)

#         # if item_form_instance.is_valid():

#         #     item_object=item_form_instance.save(commit=False)

#         #     item_object.items_obj=request.user.company  

#         #     item_form_instance.save()

#             # Item.objects.create(**data,items_obj=request.user.company)


#         #     print (item_form_instance)

#         #     return redirect("generate-bill")
        
#         # if receiver_form_instance.is_valid():

#         if 'submit_item_form' in form_data:
#             item_form_instance = self.item_form_class(form_data)
#             if item_form_instance.is_valid():
#                 item_object = item_form_instance.save(commit=False)
#                 item_object.items_obj = request.user.company
#                 item_object.save()
#                 return redirect("generate-bill")
            
#             return render(request,self.template_name,{"form":item_form_instance})
#         return redirect("generate-bill")
        

class GenerateBillReceiptView(View):
    template_name = 'generate_bill.html'

    item_form_class = ItemForm
    receiver_form_class = ReceiverForm
    shipto_form_class = ShipToForm

    def get(self,request,*args,**kwargs):

        item_form_instance=self.item_form_class()

        receiver_form_instance=self.receiver_form_class()

        shipto_form_instance=self.shipto_form_class()

        qs=Item.objects.filter(items_obj=request.user.company) 

        company_obj=Company.objects.get(company_obj=(request.user))

        return render(request,self.template_name,{"data":qs,"item_form":item_form_instance,"company":company_obj,"receiver_form":receiver_form_instance, "shipto_form":shipto_form_instance })

    def post(self, request, *args, **kwargs):
        form_data = request.POST

        # Handle ItemForm submission
        if 'submit_item_form' in form_data:
            item_form_instance = self.item_form_class(form_data)
            if item_form_instance.is_valid():
                item_object = item_form_instance.save(commit=False)
                item_object.items_obj = request.user.company  # Link item to the user's company
                item_object.save()
                return redirect("generate-bill")  # Redirect after successful submission
            else:
                print("Item Form Errors:", item_form_instance.errors)  # Log errors for debugging

        # Handle ReceiverForm and ShipToForm submission together
        elif 'submit_receiver_shipto_forms' in form_data:
            receiver_form_instance = self.receiver_form_class(form_data)
            shipto_form_instance = self.shipto_form_class(form_data)
            
            if receiver_form_instance.is_valid() and shipto_form_instance.is_valid():
                receiver_object = receiver_form_instance.save(commit=False)
                receiver_object.receiver_obj = request.user.company  # Link receiver to the user's company
                receiver_object.save()
                
                shipto_object = shipto_form_instance.save(commit=False)
                shipto_object.ship_obj = request.user.company  # Link shipping to the user's company
                shipto_object.save()
                return redirect("generate-bill")  # Redirect after successful submission
            else:
                print("Receiver Form Errors:", receiver_form_instance.errors)  # Log errors for debugging
                print("ShipTo Form Errors:", shipto_form_instance.errors)  # Log errors for debugging

        # Reload the page with errors if forms are invalid
        qs = Item.objects.filter(items_obj=request.user.company)  # Get items for the user's company
        company_obj = Company.objects.get(company_obj=request.user)  # Get the user's company

        return render(
            request, 
            self.template_name, 
            {
                "data": qs,
                "item_form": self.item_form_class(form_data) if 'submit_item_form' in form_data else self.item_form_class(),
                "company": company_obj,
                "receiver_form": self.receiver_form_class(form_data),
                "shipto_form": self.shipto_form_class(form_data),
            }
        )

class SignOutView(View): 

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("")
    
class ItemDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Item.objects.get(id=id).delete()

        return redirect("generate-bill")
