"""
URL configuration for nyondoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from nyondoapp import views

urlpatterns = [
    path('admin/', admin.site.urls),   
    path('dash', views.dash, name='dash'),
    path('supplier/registration/', views.supplier_registration, name='supplier_registration'),
    path('supplier/list/', views.supplier_list, name='supplier_list'),
    path('supplier/credit/register/', views.supplier_credit_register, name='supplier_credit_register'),
    path('supplier/credit/table/', views.supplier_credit_table, name='supplier_credit_table'),
    path('supplier/payment/register/', views.payment_register, name='payment_register'),
    path('supplier/payment/table/', views.payment_table, name='payment_table'),
    path('stock_dash/',views.stock_dash, name='stock_dash' ),
    path('stock_page/', views.stock_page, name='stock_page'),
    path('stock_register/', views.stock_register, name='stock_reg'),
    path('sales_dash/', views.sales_dash, name='sales_dash'),
    path('sales/', views.sales_page, name='sales_page'),
    path('sales/register/', views.sales_reg, name='sales_reg'),
    path('', views.land, name="land"),
    path('login/', views.login_view, name="login"),   
    path('customer_deposit/', views.customer_deposit, name="customer_deposit"),  
    path('customer_page/', views.customer_page, name="customer_page"),
    path('deposit_page/', views.deposit_page, name="deposit_page"),       
    path('edit_deposit/<int:deposit_id>/', views.edit_deposit, name="edit_deposit"),
    path('delete_deposit/<int:deposit_id>/', views.delete_deposit, name="delete_deposit"),
    path('track/', views.track, name='track'),
    path('sales/report/', views.sales_report, name='sales_report'),
    path('stock/report/', views.stock_report, name='stock_report'),
    path('logout/', views.logout_page, name='logout'),
    path('stock/view/<int:pk>/', views.view_stock, name='view_stock'),
    path('stock/update/<int:pk>/', views.update_stock, name='update_stock'),
    path('stock/delete/<int:pk>/', views.delete_stock, name='delete_stock'),
    path('receipt/', views.receipt, name='receipt'),
    path('receipt/temp/', views.temp_receipt, name='temp_receipt'),
    path('supplier/view/<int:id>/', views.view_supplier, name='view_supplier'),
    path('supplier/delete/<int:id>/', views.delete_supplier, name='delete_supplier'),
    path('supplier/update/<int:id>/', views.update_supplier, name='update_supplier'),
    path('employee_table/', views.employee_table, name='employee_table'),
    path('view_employee/<int:id>/', views.view_employee, name='view_employee'),
    path('update_employee/<int:id>/', views.update_employee, name='update_employee'),
    path('delete_employee/<int:id>/', views.delete_employee, name='delete_employee'),
    path('users/', views.create_staff, name='users'),

]
