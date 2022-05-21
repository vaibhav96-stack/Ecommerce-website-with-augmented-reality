from .models import ProductForm,SUPERCATEGORY_CHOICES,Category,Cart,Purchase
from instamojo_wrapper import Instamojo
from django.conf import settings
import os


# this file is generating errors take care to close it

def my_scheduled_job():
    # print("cron is running")
    # f = open('/home/harshit/testfile.txt', 'w+')
    # f.write("Working\n")
    cart_obj = Cart.objects.filter(is_paid__exact='no').exclude(transaction_id='')
    for cart in cart_obj:
        response = settings.INSTAMOJO_API.payment_request_status(cart.transaction_id)
        if response['payment_request']['status'] == 'Completed' and response['payment_request']['payments'][0]['status'] == 'Credit':
            cart.transaction_id = response['payment_request']['payments'][0]['payment_id']
            cart.is_paid = 'yes'
            cart.save()
        else:
            cart.transaction_id = ''
            cart.save()
            purchases = Purchase.objects.filter(cart=cart)

            for item in purchases:
                product = ProductForm.objects.filter(id=item.name.id).first()
                product.stock = product.stock + item.quantity
                product.save()

