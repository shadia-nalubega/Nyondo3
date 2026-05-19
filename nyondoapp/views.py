from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date
from nyondoapp.models import Supplier, Payment, Scredit, Stock, Sale, Product, Customer, Deposit

# ==================== SUPPLIER SECTION ====================

def supplier_registration(request):
    if request.method == 'POST':
        supplier = Supplier.objects.create(
            company_name=request.POST['company_name'],
            location=request.POST['location'],
            product_description=request.POST['product_description'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            TRN=request.POST['TRN'],
            payment_option=request.POST['payment_option']
        )
        return redirect('supplier_list')
    return render(request, 'account/supplier_registration.html')

def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('-id')
    return render(request, 'account/supplier_list.html', {'suppliers': suppliers})

def supplier_credit_register(request):
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_name')
        supplier = Supplier.objects.get(id=supplier_id)
        Scredit.objects.create(
            company_name=supplier,
            quantity=request.POST.get('quantity', 0),
            amount_owed=request.POST.get('amount_owed', 0),
            status=request.POST.get('status', 'Pending'),
            notes=request.POST.get('notes', '')
        )
        return redirect('supplier_credit_table')
    suppliers = Supplier.objects.all()
    return render(request, 'account/supplier_credit.html', {'suppliers': suppliers})

def supplier_credit_table(request):
    supplier = Scredit.objects.all().order_by('-id')
    return render(request, 'account/supplier_credit_table.html', {'supplier': supplier})

# ==================== PAYMENT SECTION ====================

def payment_register(request):
    if request.method == 'POST':
        Payment.objects.create(
            supplier_name=request.POST['supplier_name'],
            product_description=request.POST['product_description'],
            payment_date=request.POST['payment_date'],
            amount_paid=request.POST['amount_paid'],
            balance_remaining=request.POST['balance_remaining'],
            comments=request.POST['comments']
        )
        return redirect('payment_table')
    return render(request, 'account/payment.html')

def payment_table(request):
    payment = Payment.objects.all().order_by('-id')
    return render(request, 'account/payment_table.html', {'payment': payment})

# ==================== STOCK SECTION ====================

def stock_register(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        description = request.POST.get('description')
        supplier_id = request.POST.get('supplier')
        units = request.POST.get('units', 'pieces')
        quantity = request.POST.get('quantity', 0)
        cost_price = request.POST.get('cost_price', 0)
        
        # Convert to numbers
        try:
            quantity = int(quantity) if quantity else 0
        except:
            quantity = 0
        try:
            cost_price = int(cost_price) if cost_price else 0
        except:
            cost_price = 0
        
        # Validate supplier
        if not supplier_id:
            suppliers = Supplier.objects.all()
            return render(request, 'stock/stock_reg.html', {'suppliers': suppliers, 'error': 'Please select a supplier'})
        
        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            suppliers = Supplier.objects.all()
            return render(request, 'stock/stock_reg.html', {'suppliers': suppliers, 'error': 'Selected supplier does not exist'})
        
        # Update or create product
        existing_products = Product.objects.filter(product_id=product_id)
        if existing_products:
            product = existing_products[0]
            product.current_stock = product.current_stock + quantity
            product.buying_price = cost_price
            product.save()
        else:
            product = Product.objects.create(
                product_id=product_id,
                product_name=description,
                buying_price=cost_price,
                current_stock=quantity,
                threshold=10
            )
        
        # Save to stock history
        Stock.objects.create(
            product_id=product_id,
            description=description,
            quantity=quantity,
            units=units,
            cost_price=cost_price,
            supplier=supplier,
            buyer_type=request.POST.get('buyer_type', 'Retail'),
            selling_price=0
        )
        
        messages.success(request, 'Stock added successfully!')
        return redirect('stock_dash')
    
    suppliers = Supplier.objects.all()
    return render(request, 'stock/stock_reg.html', {'suppliers': suppliers})

# MAIN STOCK DASHBOARD (with cards)
def stock_dash(request):
    # Get all stock items
    all_stock = Stock.objects.select_related().order_by('-id')
    
    # Card calculations
    total_stock_count = Stock.objects.count()
    today = date.today()
    todays_stock_count = Stock.objects.filter(date=today).count()
    low_stock_count = Stock.objects.filter(quantity__lt=10).count()
    
    total_value = 0
    for item in all_stock:
        total_value += item.quantity * item.cost_price
    
    return render(request, 'stock/stock_dash.html', {
        'stock_items': all_stock,
        'total_stock': total_stock_count,
        'todays_stock': todays_stock_count,
        'low_stock': low_stock_count,
        'total_value': total_value,
    })

# STOCK PAGE (just table view)
def stock_page(request):
    all_stock = Stock.objects.select_related().order_by('-id')
    return render(request, 'stock/stock_page.html', {
        'stock_items': all_stock,
    })

# TRACK STOCK (for checking stock levels)
def track(request):
    products = Product.objects.all()
    
    total_products = products.count()
    total_units = 0
    low_stock_count = 0
    
    for product in products:
        total_units += product.current_stock
        if product.current_stock < product.threshold and product.current_stock > 0:
            low_stock_count += 1
    
    context = {
        'products': products,
        'total_products': total_products,
        'total_units': total_units,
        'low_stock_count': low_stock_count,
    }
    return render(request, 'stock/track.html', context)

# VIEW, UPDATE, DELETE for Stock
def view_stock(request, pk):
    single_stock = get_object_or_404(Stock, id=pk)
    return render(request, 'stock/view_stock.html', {'item': single_stock})

def update_stock(request, pk):
    stock_item = get_object_or_404(Stock, id=pk)
    
    if request.method == 'POST':
        stock_item.product_id = request.POST.get('product_id')
        stock_item.description = request.POST.get('description')
        stock_item.quantity = request.POST.get('quantity')
        stock_item.cost_price = request.POST.get('cost_price')
        stock_item.supplier_id = request.POST.get('supplier')
        stock_item.buyer_type = request.POST.get('buyer_type')
        stock_item.save()
        messages.success(request, 'Stock updated successfully!')
        return redirect('stock_dash')
    
    suppliers = Supplier.objects.all()
    return render(request, 'stock/update_stock.html', {
        'item': stock_item,
        'suppliers': suppliers
    })

def delete_stock(request, pk):
    stock_item = get_object_or_404(Stock, id=pk)
    
    if request.method == 'POST':
        stock_item.delete()
        messages.success(request, 'Stock deleted successfully!')
        return redirect('stock_dash')
    
    return render(request, 'stock/delete_stock.html', {'stock': stock_item})

# ==================== SALES SECTION ====================

def sales_dash(request):
    from datetime import date
    today = date.today()
    
    # Get all sales for the table
    all_sales = Sale.objects.all().order_by('-id')
    
    # Card calculations
    today_sales_total= Sale.objects.filter(date=today).count()
    today_deposits_total = Deposit.objects.filter(deposit_date=today).count()
    complete_receipts = Sale.objects.count()
    pending_receipts = Deposit.objects.filter(status='Pending').count()
    
    return render(request, 'sales/sales_dash.html', {
        'new_sale': all_sales,
        'today_sales_total': today_sales_total,
        'today_deposits_total': today_deposits_total,
        'complete_receipts': complete_receipts,
        'pending_receipts': pending_receipts,
    })




def sales_reg(request):
    if request.method == "POST":
        cashier = request.POST['cashier']
        customer_name = request.POST['customer_name']
        customer_phone = request.POST.get('phone')
        payment = request.POST['payment']
        
        product_names = request.POST.getlist('product_name')
        quantities = request.POST.getlist('quantity')
        selling_prices = request.POST.getlist('selling_price')
        distances = request.POST.getlist('distance')
        
        subtotal = 0
        max_distance = 0
        
        for i in range(len(product_names)):
            qty = int(quantities[i])
            price = int(selling_prices[i])
            item_total = qty * price
            subtotal += item_total
            distance = int(distances[i])
            if distance > max_distance:
                max_distance = distance
        
        if max_distance <= 10 and subtotal <= 500000:
            transport_fee = 0
        elif max_distance < 10 and subtotal >= 5000000:
            transport_fee = 0  
        else:
            transport_fee = 30000
        grand_total = subtotal + transport_fee
        
        # ========== FIRST: SAVE SALES ==========
        for i in range(len(product_names)):
            Sale.objects.create(
                cashier=cashier,
                product_name=product_names[i],
                quantity=int(quantities[i]),
                selling_price=int(selling_prices[i]),
                distance=int(distances[i]),
                total_amount=int(quantities[i]) * int(selling_prices[i]),
                payment=payment,
                customer_name=customer_name,
                customer_phone=customer_phone,
                transport_fee=transport_fee
            )
        
        # ========== SECOND: REDUCE STOCK ==========
        for i in range(len(product_names)):
            try:
                product = Product.objects.get(product_name=product_names[i])
                product.current_stock -= int(quantities[i])
                product.save()
            except Product.DoesNotExist:
                pass  # Product not found, but sale is already saved

            
        
        return redirect('sales_page')
    
    products = Product.objects.all()
    return render(request, 'sales/sales_reg.html', {'products': products})
def sales_page(request):
    today = date.today()
    all_sales = Sale.objects.all().order_by('-date')
    today_sales = Sale.objects.filter(date=today)
    today_total = sum(sale.total_amount for sale in today_sales)
    
    return render(request, 'sales/sales_page.html', {
        'new_sale': all_sales,
        'today_total': today_total
    })

def sales_report(request):
    sales = Sale.objects.all().order_by('-date')
    grand_total = sum(sale.total_amount for sale in sales)
    
    return render(request, 'sales/sales_report.html', {
        'sales': sales,
        'grand_total': grand_total,
    })

# ==================== CUSTOMER DEPOSIT SECTION ====================
def customer_deposit(request):
    if request.method == 'POST':
        # Create customer
        customer = Customer.objects.create(
            customer_name=request.POST.get('customer_name'),
            phone=request.POST.get('phone'),
            product_name=request.POST.get('product_name'),
            nin=request.POST.get('nin'),
            location=request.POST.get('location'),
            total_price=request.POST.get('total_price')
        )
        
        # Create deposit
        deposit = Deposit.objects.create(
            Customer_name=customer,
            deposit_date=request.POST.get('deposit_date'),
            expected_completion=request.POST.get('expected_completion'),
            status=request.POST.get('status'),
            deposit_amount=request.POST.get('deposit_amount')
        )
        
        # Calculate remaining balance correctly
        total_price = int(customer.total_price)
        deposit_amount = int(deposit.deposit_amount)
        remaining_balance = total_price - deposit_amount
        
        # Store in session for receipt
        request.session['deposit_receipt'] = {
            'receipt_no': deposit.id,
            'date': request.POST.get('deposit_date'),
            'customer_name': customer.customer_name,
            'phone': customer.phone,
            'product_name': customer.product_name,
            'total_price': total_price,
            'deposit_amount': deposit_amount,
            'remaining_balance': remaining_balance, 
            'received_by': request.POST.get('received_by', 'Admin'),
            'status': deposit.status,
            'expected_completion': request.POST.get('expected_completion'),
        }
        
        return redirect('temp_receipt')
    
    return render(request, 'account/customer_deposit.html')
def customer_page(request):
    customers = Customer.objects.all().order_by('-id')
    return render(request, 'account/customer_page.html', {'customers': customers})

def deposit_page(request):
    deposits = Deposit.objects.all().order_by('-deposit_date')
    customers = Customer.objects.all().order_by('-id')
    
    # Calculate remaining balance for each deposit (SAFE VERSION)
    for deposit in deposits:
        # Convert to integers to avoid type errors
        total_price = int(deposit.Customer_name.total_price) if deposit.Customer_name.total_price else 0
        deposit_amount = int(deposit.deposit_amount) if deposit.deposit_amount else 0
        deposit.remaining_balance = total_price - deposit_amount
    
    context = {
        'deposits': deposits,
        'customers': customers,
    }
    return render(request, 'account/deposit_page.html', context)


def edit_deposit(request, deposit_id):
    deposit = get_object_or_404(Deposit, id=deposit_id)
    customer = deposit.Customer_name
    
    if request.method == 'POST':
        customer.customer_name = request.POST.get('customer_name')
        customer.phone = request.POST.get('phone')
        customer.product_name = request.POST.get('product_name')
        customer.nin = request.POST.get('nin')
        customer.location = request.POST.get('location')
        customer.total_price = request.POST.get('total_price')
        customer.save()
        
        deposit.deposit_amount = request.POST.get('deposit_amount')
        deposit.deposit_date = request.POST.get('deposit_date')
        deposit.expected_completion = request.POST.get('expected_completion')
        deposit.status = request.POST.get('status')
        deposit.save()
        
        return redirect('deposit_page')
    
    context = {
        'deposit': deposit,
        'customer': customer,
    }
    return render(request, 'account/edit_deposit.html', context)

def delete_deposit(request, deposit_id):
    deposit = get_object_or_404(Deposit, id=deposit_id)
    deposit.delete()
    return redirect('deposit_page')

# ==================== REPORTS ====================

def stock_report(request):
    products = Product.objects.all()
    
    total_products = products.count()
    total_units = 0
    low_stock_count = 0
    out_of_stock = 0
    
    for product in products:
        total_units += product.current_stock
        if product.current_stock <= 0:
            out_of_stock += 1
        elif product.current_stock < product.threshold:
            low_stock_count += 1
    
    context = {
        'products': products,
        'total_products': total_products,
        'total_units': total_units,
        'low_stock_count': low_stock_count,
        'out_of_stock': out_of_stock,
    }
    return render(request, 'stock/stock_report.html', context)

# ==================== OTHER PAGES ====================

def dash(request):
    suppliers = Supplier.objects.all().order_by('-id')
    total_stock_count = Stock.objects.count()
    total_suppliers = Supplier.objects.count()
    total_sales = Sale.objects.count()
    
    # Calculate total revenue (sum of all sale totals + transport fees)
    all_sales = Sale.objects.all()
    total_revenue = 0
    for sale in all_sales:
        total_revenue += sale.total_amount + sale.transport_fee
    
    context = {
        'suppliers': suppliers,
        'total_stock_count': total_stock_count,
        'total_suppliers': total_suppliers,
        'total_sales': total_sales,
        'total_revenue': total_revenue,  }




    return render(request, 'account/dash.html', context)

def land(request):
    return render(request, "land.html")

def login(request):
    return render(request, "login.html")

def logout_page(request):
    return render(request, 'logout.html')

def stock_track(request):
    return render(request, "stock/track.html")


def receipt(request):
    # Get the most recent sale
    latest_sale = Sale.objects.all().order_by('-id').first()
    
    if not latest_sale:
        messages.error(request, 'No sale found')
        return redirect('receipt')
    
    # Calculate grand total
    grand_total = latest_sale.total_amount + latest_sale.transport_fee
    
    return render(request, 'sales/receipt.html', {
        'sale': latest_sale,
        'grand_total': grand_total
    })
def temp_receipt(request):
    # Get deposit info from session
    deposit_data = request.session.get('deposit_receipt')
    
    if not deposit_data:
        return redirect('deposit_page')
    
    return render(request, 'account/temp_receipt.html', {'deposit': deposit_data})