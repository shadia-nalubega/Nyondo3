from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# supplier models here
class Supplier(models.Model):
    company_name = models.TextField(blank=False)
    email = models.EmailField(blank=True)
    location = models.CharField(blank=False, max_length=100)
    TRN = models.TextField(blank=False)
    phone = models.TextField(blank=False)
    product_description = models.TextField(blank=False)
    payment_option = models.CharField(max_length=50, blank=False)
    
    def __str__(self):
        return self.company_name
    # the supplier credit model
 

class Scredit(models.Model):
    company_name = models.ForeignKey(Supplier ,on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    amount_owed = models.IntegerField(blank=False)
    status = models.TextField(blank=False)
    notes = models.TextField(blank=True)

class Payment(models.Model):
    supplier_name = models.CharField(blank=False, max_length=255, unique=True)
    product_description = models.CharField(blank=False, max_length=255)
    amount_paid = models.IntegerField(blank=False)
    payment_date = models.DateField(auto_now_add=True)
    balance_remaining = models.IntegerField(blank=False)
    comments = models.TextField()

class Stock(models.Model):
    product_id = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    units = models.CharField(max_length=20)
    cost_price = models.IntegerField()
    selling_price = models.IntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='stocks')
    date = models.DateField(auto_now_add=True)
    buyer_type = models.CharField(max_length=50)


    

class Product(models.Model):
    product_id = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=100)
    buying_price = models.IntegerField()
    current_stock = models.IntegerField(default=0)
    threshold = models.IntegerField(default=10)
    last_updated = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.product_name







# this class is going to be a child of the supplier class
# models.py - Keep it simple, no ForeignKeys!

class Sale(models.Model):
    cashier = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)  # Store the name directly
    quantity = models.IntegerField()
    selling_price = models.IntegerField()  # Store the price at time of sale
    distance = models.IntegerField(default=0)
    total_amount = models.IntegerField()
    transport_fee = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    payment = models.CharField(max_length=50)  # Cash, Mobile Money, etc.
    customer_name = models.CharField(max_length=50)
    customer_phone = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.product_name} - {self.date}"



    
class Customer(models.Model):
    customer_name = models.CharField(max_length=30, blank=False)
    phone=models.TextField()
    product_name = models.CharField(max_length=100 ,blank=False)
    nin = models.TextField()
    location = models.CharField(max_length=100)
    total_price = models.IntegerField()


class Deposit(models.Model):
    STATUS = [
        ("Active","Active"),
        ("Pending","Pending"),
        ("Finished","Finished")
    ]   
    
    Customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    deposit_date = models.DateField()
    deposit_amount = models.IntegerField()
    expected_completion = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS)


class Staff(models.Model):
    ROLES =[
        ("admin","admin"),
        ("sales_attendant","sales_attendant"),
        ("store_manager","store_manager")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50)
    role = models.CharField(max_length=50, choices=ROLES)