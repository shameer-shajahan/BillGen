from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from django.views.generic.edit import FormView
from .forms import ItemForm, SignUpForm, SignInForm, CompanyDetailForm, ReceiverForm, ShipToForm, BillForm
from django.contrib.auth import authenticate,login,logout
from .models import Item,Company,ExistingBills,ExBill
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
from django.utils.decorators import method_decorator
from billapp.decorators import signin_requried
from django.views.decorators.cache import never_cache
decs=[signin_requried,never_cache]


    
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

        return redirect("landingpage")

class LandingpageView(View):

    template_name="landingpage.html"

    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)

@method_decorator(decs, name='dispatch')
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

@method_decorator(decs, name='dispatch')
class ReceiverView(View):

    template_name = 'receiver.html'

    form_class = ReceiverForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            receiver_object=form_instance.save(commit=False)

            receiver_object.receiver_obj=request.user.company

            form_instance.save()

            return redirect("shipto")
        
        return render(request,self.template_name,{"form":form_instance})

@method_decorator(decs, name='dispatch')
class Shipto(View):

    template_name = 'shipto.html'

    form_class = ShipToForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            shipto_object=form_instance.save(commit=False)

            shipto_object.ship_obj=request.user.company

            form_instance.save()

            return redirect("generate-bill",pk=shipto_object.id)
        
        return render(request,self.template_name,{"form":form_instance})

@method_decorator(decs, name='dispatch')
class index(View):

    template_name="index.html"

    def get(self,request,*args,**kwargs):

        company = request.user.company
        context = {
        'company_id': company.id,
        }
        return render(request, self.template_name, context)
    
@method_decorator(decs, name='dispatch')
class Invoice(View):
    template_name = "invoice.html"

    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')  # Retrieve the id from the URL parameters
        comp_dtl = Company.objects.get(company_obj=request.user)
        items = Item.objects.filter(items_obj=request.user.company)
        receiver = Receiver.objects.filter(receiver_obj=request.user.company).get(id=id)
        shipto = ShipTo.objects.filter(ship_obj=request.user.company).get(id=id)

        # Calculate the sum of the total amounts
        total_amount = sum(item.amount for item in items)

        return render(request, self.template_name, {
            "data": items,
            "receiver_data": receiver,
            "shipto_data": shipto,
            "comp_dtl": comp_dtl,
            "total_amount": total_amount  # Pass the total amount to the template context
        })
    
@method_decorator(decs, name='dispatch')
class GenerateBillReceiptView(View):

    template_name = 'generate_bill.html'

    item_form_class = ItemForm

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        item_form_instance = self.item_form_class()
        
        qs = Item.objects.filter(items_obj=request.user.company)
        
        comp_dtl=Company.objects.get(company_obj=(request.user))
        
        receiver = Receiver.objects.filter(receiver_obj=request.user.company).get(id=id)

        shipto = ShipTo.objects.filter(ship_obj=request.user.company).get(id=id)
        
        return render(request, self.template_name, {
            "data": qs,
            "item_form": item_form_instance,
            "receiver_data": receiver,
            "shipto_data": shipto,
            "comp_dtl":comp_dtl,
             "id": id ,
            })

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        form_data = request.POST
        form_instance = self.item_form_class(form_data)  # Use item_form_class here

        if form_instance.is_valid():
            item_object = form_instance.save(commit=False)
            item_object.items_obj = request.user.company  # Link item to the user's company
            item_object.save()

            return redirect('generate-bill', pk=id)  # Redirect to the generate-bill page with the correct id

        qs = Item.objects.filter(items_obj=request.user.company)  # Get items for the user's company
        company_obj = Company.objects.get(company_obj=request.user)  # Get the user's company

        # Return the template with errors in the form
        return render(
            request,
            self.template_name,
            {
                "data": qs,
                "item_form": form_instance,
                "company": company_obj,
                "id": id  # Pass the id to the template context
            },
        )
    
@method_decorator(decs, name='dispatch')
class ItemDeleteView(View):

    def get(self, request, *args, **kwargs):
        item_id = kwargs.get("pk")
        bill_id = kwargs.get("bill_id")  # Assuming you pass the bill_id to redirect back to the generate-bill page

        Item.objects.get(id=item_id).delete()

        return redirect('generate-bill', pk=bill_id)

def render_to_pdf(template_src, context_dict={}):
    """
    Utility function to render a template into a PDF file.
    """
    from django.template.loader import get_template
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pisa_status = pisa.CreatePDF(
        html, dest=result
    )
    if pisa_status.err:
        return None
    return result.getvalue()  # Return raw PDF bytes

def generate_items_pdf(request, *args, **kwargs):
    """
    View to generate and return the PDF for items.
    """
    id = kwargs.get('pk')
    
    items = Item.objects.filter(items_obj=request.user.company)
    comp_dtl = Company.objects.get(company_obj=request.user)
    receiver = Receiver.objects.filter(receiver_obj=request.user.company).get(id=id)

    shipto = ShipTo.objects.filter(ship_obj=request.user.company).get(id=id)


    pdf = render_to_pdf('items_pdf_template.html', {"items": items,"receiver_data": receiver,"shipto_data": shipto,"company_dlt":comp_dtl})

    
    if pdf:
        # Wrap the raw PDF bytes in a BytesIO object
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="items.pdf"'
        return response

    return HttpResponse('Failed to generate PDF.')
    
def send_items_email(request, *args, **kwargs):
    """
    View to generate a PDF of items and send it via email.
    """
    id = kwargs.get('pk')
    
    items = Item.objects.filter(items_obj=request.user.company)
    comp_dtl = Company.objects.get(company_obj=request.user)
    receiver_dlt = Receiver.objects.filter(receiver_obj=request.user.company).get(id=id)
    shipto_dlt = ShipTo.objects.filter(ship_obj=request.user.company).get(id=id)

    context = {
        'items': items,
        'company_dlt': comp_dtl,
        'receiver_dlt': receiver_dlt,
        'shipto_dlt': shipto_dlt
    }
    pdf = render_to_pdf('items_pdf_template.html', context)  # Generate the PDF
    if pdf:
        # Email settings
        subject = 'Delivery Receipt'
        message = 'Please find attached the delivery receipt.'
        recipient_list = ['recipient@example.com']  # Replace with actual recipient email
        sender_email = 'your_email@example.com'  # Replace with your sender email

        # Create the email
        email = EmailMessage(subject, message, sender_email, recipient_list)

        # Attach the PDF
        email.attach('delivery_receipt.pdf', pdf, 'application/pdf')

        # Send the email
        email.send()
        return HttpResponse('Email sent successfully!')
    
    return HttpResponse('Failed to generate PDF for email.')

@method_decorator(decs, name='dispatch')
class ManageItemsView(View):
    template_name = 'manage_items.html'

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request. Displays the list of items and the form to add a new item.
        """
        form = ItemForm()
        
        id = kwargs.get('pk')

        item_form_instance = self.item_form_class()
        
        qs = Item.objects.filter(items_obj=request.user.company)
        
        comp_dtl=Company.objects.get(company_obj=(request.user))
        
        receiver = Receiver.objects.filter(receiver_obj=request.user.company).get(id=id)

        shipto = ShipTo.objects.filter(ship_obj=request.user.company).get(id=id)
        
        return render(request, self.template_name, {
            "data": qs,
            "item_form": item_form_instance,
            "receiver_data": receiver,
            "shipto_data": shipto,
            "comp_dtl":comp_dtl,
             "id": id ,
            })
    

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request. Adds a new item to the database if the form is valid.
        """
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_items')  # Redirect to the same page after adding the item
        
        id = kwargs.get('pk')

        item_form_instance = self.item_form_class()
        
        qs = Item.objects.filter(items_obj=request.user.company)
        
        comp_dtl=Company.objects.get(company_obj=(request.user))
        
        receiver = Receiver.objects.filter(receiver_obj=request.user.company).get(id=id)

        shipto = ShipTo.objects.filter(ship_obj=request.user.company).get(id=id)
        
        return render(request, self.template_name, {
            "data": qs,
            "item_form": item_form_instance,
            "receiver_data": receiver,
            "shipto_data": shipto,
            "comp_dtl":comp_dtl,
             "id": id ,
            })

# if user enter shipt data then go to generate-bill with user last enter data

@method_decorator(decs, name='dispatch')
class SaveBillView(View):

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')  # Retrieve the id from the URL parameters

        comp_dtl = Company.objects.get(company_obj=request.user)
        items = Item.objects.filter(items_obj=request.user.company)  # Filter items by the user's company
        receiver = Receiver.objects.filter(receiver_obj=request.user.company).get(id=id)
        shipto = ShipTo.objects.filter(ship_obj=request.user.company).get(id=id)
         # Calculate the sum of the total amounts
        total_amount = sum(item.amount for item in items)
        
        # Correctly reference the `owner` field instead of `user`
        exbill_obj = ExBill.objects.get(owner=request.user)
        
        # Create a new ExistingBills instance
        bill = ExistingBills.objects.create(
            receiver_obj=receiver,
            comp_dtl=comp_dtl,
            ship_obj=shipto,
            exbill_obj=exbill_obj,
            # total_amount=total_amount,
        )

        # Add the items to the bill
        bill.items_obj.set(items)

        print("Bill has been added to saved Bills")

        return redirect("save_bill")

@method_decorator(decs, name='dispatch')
class SavedBillSummaryView(View):

    template_name="saved_items.html"

    def get(self,request,*args,**kwargs):
        
        qs=ExistingBills.objects.filter(exbill_obj=request.user.ex_bill) 

        return render(request,self.template_name,{"data":qs})
    
@method_decorator(decs, name='dispatch')
class SavedBillDetailView(View):

    template_name="saved_bill_detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        bill_obj=ExistingBills.objects.get(id=id)

        items_obj=Item.objects.filter(items_obj=request.user.company)

        return render(request,self.template_name,{"data":bill_obj,"items":items_obj})
