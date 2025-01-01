from django.db import models

from django.contrib.auth.models import AbstractUser 

from django.db.models.signals import post_save

from django.utils.timezone import now


class User(AbstractUser):

    phone=models.CharField(max_length=15,unique=True)

    is_verified=models.BooleanField(default=False)

class Company(models.Model):

    company_obj=models.OneToOneField(User,on_delete=models.CASCADE,related_name="company")

    company_logo=models.ImageField(upload_to="company_logo",null=True,blank=True)

    company_name=models.CharField(max_length=100)

    registration_number = models.CharField(max_length=50,null=True,blank=True)

    company_address=models.TextField()

    city = models.CharField(max_length=100)
    
    state = models.CharField(max_length=100)
    
    country = models.CharField(max_length=100,null=True,blank=True)
    
    postal_code = models.CharField(max_length=20)

    company_mobile=models.CharField(max_length=12)

    company_email=models.EmailField()

    website = models.URLField(blank=True, null=True)

    company_GSTIN=models.CharField(max_length=20,null=True,blank=True)

    established_date = models.DateField(null=True,blank=True)

    active = models.BooleanField(default=True,null=True,blank=True)

    def __str__(self):

        return self.company_name
    
class Item(models.Model):
   
    items_obj = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='items')  # Linking to Company
   
    si_no = models.PositiveIntegerField(null=True)  # Serial Number
   
    items = models.CharField(max_length=255)  # Item Name
   
    description = models.TextField(blank=True, null=True)  # Item Description
   
    quantity = models.PositiveIntegerField()  # Quantity of Items
   
    unit = models.CharField(max_length=50, choices=[
        ('pcs', 'Pieces'),
        ('kg', 'Kilograms'),
        ('ltr', 'Liters'),
        ('box', 'Box'),
        ('doz', 'Dozen'),
    ], default='pcs')  # Unit of Measurement
   
    rate = models.DecimalField(max_digits=10, decimal_places=2)  # Unit Rate
   
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Discount in %")  # Discount Percentage
   
    tax_option = [
        ('18', 'GST'),
        ('0', 'No Tax'),
    ]
   
    tax = models.CharField(max_length=50, choices=tax_option, default='None')  # Tax Type
   
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Tax rate in %")  # Tax Rate
   
    stock = models.PositiveIntegerField(default=0, help_text="Current stock available")  # Stock Tracking
   
    amount = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)  # Total Amount
   
    created_at = models.DateTimeField(default=now, editable=False)  # Timestamp for creation
   
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for last update

    def __str__(self):
        return f"{self.items} - {self.items_obj.name}"

    def calculate_amount(self):
        """
        Calculate total amount based on quantity, rate, discount, and tax.
        """
        base_amount = self.quantity * float(self.rate)
        discount_amount = base_amount * (float(self.discount) / 100)
        taxable_amount = base_amount - discount_amount
        tax_amount = taxable_amount * (float(self.tax) / 100)
        total_amount = taxable_amount + tax_amount
        return round(total_amount, 2)

    def save(self, *args, **kwargs):
        """
        Override save method to calculate and update the amount field before saving.
        """
        self.amount = self.calculate_amount()
        super().save(*args, **kwargs)

class Receiver(models.Model):

    receiver_obj = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='receivers')  # Linking to Company

    receiver_name = models.CharField(max_length=100)  # Receiver Name

    receiver_address = models.TextField()  # Receiver Address

    receiver_city = models.CharField(max_length=100,null=True,blank=True)  # City

    receiver_state = models.CharField(max_length=100)  # State

    receiver_country = models.CharField(max_length=100, default="India",null=True,blank=True)  # Country (default to India)

    receiver_postal_code = models.CharField(max_length=10, blank=True, null=True)  # Postal Code

    receiver_mobile = models.CharField(max_length=15,null=True,blank=True)  # Mobile Number

    receiver_alternate_phone = models.CharField(max_length=15, blank=True, null=True)  # Alternate Phone Number

    receiver_email = models.EmailField()  # Email Address

    receiver_GSTIN = models.CharField(max_length=20, blank=True, null=True, help_text="GST Identification Number")

    receiver_pan = models.CharField(max_length=10, blank=True, null=True, help_text="PAN Number")

    is_active = models.BooleanField(default=True,null=True,blank=True)  # Status: Active/Inactive

    created_at = models.DateTimeField(default=now, editable=False,null=True,blank=True)  # Timestamp for creation

    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)  # Timestamp for last update

    def __str__(self):
        return f"{self.receiver_name} - {self.receiver_obj.name}"

    class Meta:
        verbose_name = "Receiver"
        verbose_name_plural = "Receivers"
        ordering = ['receiver_name']

class ShipTo(models.Model):
    
    ship_obj = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='shipments')  # Linking to Company
    
    shipping_name = models.CharField(max_length=100)  # Recipient Name
    
    shipping_address = models.TextField()  # Full Shipping Address
    
    shipping_city = models.CharField(max_length=100,null=True,blank=True)  # City
    
    shipping_state = models.CharField(max_length=100,null=True,blank=True)  # State
    
    shipping_country = models.CharField(max_length=100, default="India",null=True,blank=True)  # Country
    
    shipping_postal_code = models.CharField(max_length=10, blank=True, null=True)  # Postal Code
    
    shipping_mobile = models.CharField(max_length=15,null=True,blank=True)  # Primary Mobile Number
    
    shipping_alternate_phone = models.CharField(max_length=15, blank=True, null=True)  # Alternate Phone Number
    
    shipping_email = models.EmailField()  # Email Address
    
    shipping_instructions = models.TextField(blank=True, null=True, help_text="Special instructions for delivery")
    
    is_active = models.BooleanField(default=True,null=True,blank=True)  # Status: Active/Inactive
    
    created_at = models.DateTimeField(default=now, editable=False,null=True,blank=True)  # Timestamp for creation
    
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)  # Timestamp for last update

    def __str__(self):
        return f"{self.shipping_name} - {self.ship_obj.name}"

    class Meta:
        verbose_name = "Ship To"
        verbose_name_plural = "Ship To"
        ordering = ['shipping_name']

class Bill(models.Model):
    
    bill_obj = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='bills')  # Linked to Company
    
    invoice_no = models.PositiveIntegerField(unique=True)  # Unique Invoice Number
    
    invoice_date = models.DateField(default=now)  # Invoice Date (Default to current date)
    
    due_date = models.DateField(null=True, blank=True)  # Due Date for Payment
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Total Amount
    
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Total Tax
    
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Total Discount
    
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Net Payable Amount
    
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Amount Paid
    
    balance_due = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Remaining Balance
    
    payment_status = models.CharField(max_length=20, choices=[
    
        ('Pending', 'Pending'),
    
        ('Paid', 'Paid'),
    
        ('Partially Paid', 'Partially Paid'),
    
        ('Overdue', 'Overdue'),
    
    ], default='Pending')  # Payment Status
    
    remarks = models.TextField(blank=True, null=True, help_text="Any additional notes or remarks")
    
    created_at = models.DateTimeField(default=now, editable=False)  # Timestamp for creation
    
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for last update

    def __str__(self):
    
        return f"Invoice {self.invoice_no} - {self.bill_obj.name}"

    def save(self, *args, **kwargs):
        """
        Override save method to calculate net amount and balance due before saving.
        """
        self.net_amount = (self.total_amount + self.tax_amount) - self.discount_amount
    
        self.balance_due = self.net_amount - self.paid_amount
    
        if self.balance_due <= 0:
    
            self.payment_status = 'Paid'
    
        elif self.paid_amount > 0:
    
            self.payment_status = 'Partially Paid'
    
        elif self.due_date and self.due_date < now().date():
            self.payment_status = 'Overdue'
        else:
            self.payment_status = 'Pending'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Bills"
        ordering = ['-invoice_date']

class ExBill(models.Model):

    exbill_obj=models.OneToOneField(User,on_delete=models.CASCADE,related_name="ex_bill")

class ExistingBills(models.Model):

    items_obj = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='Bill_item')  # Linking to Company

    receiver_obj = models.ForeignKey(Receiver, on_delete=models.CASCADE, related_name='Bill_receivers')  # Linking to Company

    ship_obj = models.ForeignKey(ShipTo, on_delete=models.CASCADE, related_name='Bill_shipments')  # Linking to Company

    bill_obj = models.ForeignKey(Bill, on_delete=models.CASCADE,null=True,blank=True, related_name='Bill_bills') 

    existing_bill_obj = models.ForeignKey(ExBill, on_delete=models.CASCADE, related_name='ex_bill_items') 




def create_bill(sender,instance,created,**kwargs):

    if created:

        ExBill.objects.create(exbill_obj=instance)

post_save.connect(create_bill,User)



