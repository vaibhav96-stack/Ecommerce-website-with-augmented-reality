import os.path

from django.shortcuts import render, redirect
from .models import ProductForm,SUPERCATEGORY_CHOICES,Category,Cart,Purchase
from django.http import JsonResponse, HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from users.forms import AddressForm
from instamojo_wrapper import Instamojo
from django.conf import settings
from django.urls import reverse
from datetime import datetime
import cv2
import numpy as np



def mainpage(request):
    products = {}
    for category in SUPERCATEGORY_CHOICES:
        all_subcategory = Category.objects.filter(superCategory=category[0])
        for subcategory in all_subcategory:
            products.update({subcategory: ProductForm.objects.filter(category=subcategory).order_by('-uploadedDate')})

    return render(request, 'product/mainpage.html', {'products': products})


# def home(request):
#     return render(request, 'users/home.html', {})

def subproduct(request,subcat):
    myproduct={}
    context={
    'myproduct':ProductForm.objects.filter(category=subcat).order_by('-uploadedDate') ,}
    return render(request,'product/subproduct.html',context=context)
def contact(request):
    return render(request,'product/contact.html')

def about(request):
    return render(request,'product/about.html')

def productpage(request,product_id):
    cart_obj = Cart.objects.filter(user=request.user.id, is_paid__exact='no').first()
    if cart_obj:
        product_obj = ProductForm.objects.filter(id=product_id).first()
        purchase_obj = Purchase.objects.filter(cart=cart_obj, name=product_obj).first()
        if purchase_obj:
            product_exist = 'Yes'
        else:
            product_exist = 'No'
    else:
        product_exist= 'No'
    return render(request, 'product/productpage.html', {'product_detail': ProductForm.objects.filter(id=product_id)[0], 'product_exist': product_exist})   #because filter returns an array

def temp(request,product_id):
    my_product = ProductForm.objects.get(pk=product_id)
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    imgTarget = cv2.imread(r'C:\Users\vaibhav\Pictures\Camera Roll/WIN_20210521_13_10_44_Pro.jpg')
    pt=os.path.join(str(settings.MEDIA_ROOT),str(my_product.image))
    #print(str(settings.MEDIA_ROOT) + "/" + str(my_product.image), "This line")
    myVid = cv2.VideoCapture(pt)
    success, imgVideo = myVid.read()
    cv2.imshow('Img', imgVideo)
    #print('my str :')
    #print("r'" + str(settings.MEDIA_ROOT) + '/' + str(my_product.image)+"'")
    cv2.waitKey(0)  # make waitkey as 1 for live video




def arr_real(request,product_id):
    my_product=ProductForm.objects.get(pk=product_id)
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    #imgTarget=cv2.imread(r'C:\Users\vaibhav\Pictures\Camera Roll/WIN_20210613_17_43_54_Pro.jpg')
    while(1):
        
        temp1,temp2=cap.read()
        imgTarget=temp2
        print(str(settings.MEDIA_ROOT)+"/" +str(my_product.image), "This line")
        pt = os.path.join(str(settings.MEDIA_ROOT), str(my_product.image))
        myVid = cv2.VideoCapture(pt)


        detection = False
        frameCounter = 0

        success, imgVideo = myVid.read()
        #cv2.imshow('Img', imgVideo)
        hT, wT, cT = imgTarget.shape
        imgVideo = cv2.resize(imgVideo, (wT, hT))


        orb = cv2.ORB_create(nfeatures=1000)
        kp1, des1 = orb.detectAndCompute(imgTarget, None)
        imgTarget=cv2.drawKeypoints(imgTarget,kp1,None)

        while True:

            sucess, imgWebcam = cap.read()
            # imgWebcam=cv2.flip(imgWebcam,1)
            imgAug = imgWebcam.copy()

            kp2, des2 = orb.detectAndCompute(imgWebcam, None)
            # imgWebcam=cv2.drawKeypoints(imgWebcam,kp2,None) #Draw features

            '''
            if detection==False:
                myVid.set(cv2.CAP_PROP_POS_FRAMES,0)
                frameCounter=0
            else:
                if frameCounter==myVid.get(cv2.CAP_PROP_FRAME_COUNT):
                    myVid.set(cv2.CAP_PROP_POS_FRAMES,0)
                    frameCounter=0

                success,imgVideo=myVid.read()
                imgVideo=cv2.resize(imgVideo,(wT,hT))
            '''

            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            good = []

            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append(m)
            # print(len(good))

            imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)
            if len(good) > 20:
                detection = True
                srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

                matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)

                # print(matrix)

                pts = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)
                img2 = cv2.polylines(imgWebcam, [np.int32(dst)], True, (255, 0, 255), 3)

                imgWarp = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))

                maskNew = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)

                cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))

                maskInv = cv2.bitwise_not(maskNew)
                imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskInv)
                imgAug = cv2.bitwise_or(imgWarp, imgAug)

                # imgStacked= stackImages(([imgWebcam,imgWarp],[imgWebcam,imgWarp]),0.5)

            cv2.imshow('stacked', imgAug)

            '''
            try:

                cv2.imshow('imgwrap',imgWarp)#prints Vedio on surface
            except NameError:
                print("No surface")
            except:
                print("Something else went wrong")
            '''
            '''
            try:
                cv2.imshow('img2',img2)# detects source object boundry
            except NameError:
                print("No surface")
            except:
                print("Something else went wrong")
            '''

            # cv2.imshow('imgFeatures',imgFeatures)#shows matching img features
            # cv2.imshow('Webcam',imgWebcam)
            # cv2.imshow('ImgTarget',imgTarget)
            # cv2.imshow('Target video',imgVideo)
            temp=0
            k = cv2.waitKey(1) & 0xFF  # make waitkey as 1 for live video
            if k == 27:
                temp=1
                break
            frameCounter += 1
        cv2.destroyAllWindows()
        cap.release()
        if temp==1:
            break
    return render(request,'product/productpage.html', {'product_detail': ProductForm.objects.filter(id=product_id)[0]})


@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        product = request.POST
        product_id = product['product_id']
        product_price = product['product_price']
        user_id = request.user.id
        cart_obj = Cart.objects.filter(user=user_id, is_paid__exact='no').first()


        if cart_obj:
            if cart_obj.transaction_id != '':
                response = settings.INSTAMOJO_API.payment_request_status(cart_obj.transaction_id)
                if response['payment_request']['status'] == 'Completed' and response['payment_request']['payments'][0]['status'] == 'Credit':
                    cart_obj.transaction_id = response['payment_request']['payments'][0]['payment_id']
                    cart_obj.is_paid = 'yes'
                    cart_obj.save()
                else:
                    cart_obj.transaction_id = ''
                    cart_obj.save()
                    purchases = Purchase.objects.filter(cart=cart_obj)

                    for item in purchases:
                        # print("add to cart function")
                        product = ProductForm.objects.filter(id=item.name.id).first()
                        product.stock = product.stock + item.quantity
                        product.save()


        cart_obj = Cart.objects.filter(user=user_id, is_paid__exact='no').first()
        product_obj = ProductForm.objects.filter(id=product_id).first()
        user_obj = User.objects.filter(id=user_id).first()

        if cart_obj:
            product_exist = Purchase.objects.filter(cart=cart_obj,name=product_obj).first()
            if product_exist:
                cart_obj.total_payment = cart_obj.total_payment - (product_exist.quantity)*(product_exist.price_per_item) + (product_exist.quantity+1)*(product_obj.price)
                cart_obj.save()
                product_exist.quantity += 1
                product_exist.price_per_item = product_obj.price
                product_exist.save()
            else:
                new_product = Purchase.objects.create(cart=cart_obj,name=product_obj,quantity=1,price_per_item=product_obj.price)
                cart_obj.total_payment += product_obj.price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(user=user_obj,address='',mobno=0,total_payment=product_obj.price,is_paid='no')
            new_product = Purchase.objects.create(cart=cart_obj,name=product_obj,quantity=1,price_per_item=product_obj.price)
        return JsonResponse({'status': 'OK'})
    else:
        raise Http404("Page not found")


@login_required(login_url='mainpage')
def cart(request):
    cart_obj = Cart.objects.filter(user=request.user.id, is_paid__exact='no').first()
    product_prices = []
    total_amount = 0
    ensure_stock = ''
    if not cart_obj:
        purchases = ''
    else:
        if cart_obj.transaction_id != '':
            response = settings.INSTAMOJO_API.payment_request_status(cart_obj.transaction_id)
            if response['payment_request']['status'] == 'Completed' and response['payment_request']['payments'][0]['status'] == 'Credit':
                purchases = ''
                cart_obj.transaction_id = response['payment_request']['payments'][0]['payment_id']
                cart_obj.is_paid = 'yes'
                cart_obj.save()
            else:
                cart_obj.transaction_id = ''
                cart_obj.save()
                purchases = Purchase.objects.filter(cart=cart_obj)

                for item in purchases:
                    # print("cart function")
                    product = ProductForm.objects.filter(id=item.name.id).first()
                    product.stock = product.stock + item.quantity
                    product.save()

                if not purchases:
                    purchases = ''
                else:
                    for product in purchases:
                        if product.quantity > product.name.stock:
                            ensure_stock = ''
                        else:
                            ensure_stock = 'ok'
                        product_prices.append(product.quantity*product.name.price)
                        total_amount += product.quantity*product.name.price
                        product.price_per_item = product.name.price
                        product.save()
                    cart_obj.total_payment = total_amount
                    cart_obj.save()
        else:
            purchases = Purchase.objects.filter(cart=cart_obj)
            if not purchases:
                purchases = ''
            else:
                for product in purchases:
                    if product.quantity > product.name.stock:
                        ensure_stock = ''
                    else:
                        ensure_stock = 'ok'
                    product_prices.append(product.quantity*product.name.price)
                    total_amount += product.quantity*product.name.price
                    product.price_per_item = product.name.price
                    product.save()
                cart_obj.total_payment = total_amount
                cart_obj.save()
    if purchases == '':
        return render(request, 'product/cart.html', {'purchases': zip(purchases,product_prices),'total_payment': total_amount,'is_empty': 'Yes','ensure_stock': ensure_stock})
    else:
        return render(request, 'product/cart.html', {'purchases': zip(purchases,product_prices),'total_payment': total_amount,'is_empty': 'No','ensure_stock': ensure_stock})


@csrf_exempt
@login_required(login_url='mainpage')
def update_cart(request):
    if request.method == 'POST':
        product = request.POST
        product_id = product['product_id']
        new_quantity = product['new_quantity']
        cart_obj = Cart.objects.filter(user=request.user.id, is_paid__exact='no').first()
        product_obj = ProductForm.objects.filter(id=product_id).first()
        purchase_obj = Purchase.objects.filter(cart=cart_obj, name=product_obj).first()
        cart_obj.total_payment = cart_obj.total_payment - (purchase_obj.quantity)*(purchase_obj.price_per_item) + (int(new_quantity))*(product_obj.price)
        cart_obj.save()
        purchase_obj.quantity = new_quantity
        purchase_obj.price_per_item = product_obj.price
        purchase_obj.save()

        return JsonResponse({'status': 'OK'})
    else:
        raise Http404("Page not found")



@csrf_exempt
@login_required(login_url='mainpage')
def delete_item(request):
    if request.method == 'POST':
        product = request.POST
        product_id = product['product_id']

        cart_obj = Cart.objects.filter(user=request.user.id, is_paid__exact='no').first()
        product_obj = ProductForm.objects.filter(id=product_id).first()
        purchase_obj = Purchase.objects.filter(cart=cart_obj, name=product_obj).first()
        cart_obj.total_payment = cart_obj.total_payment - (purchase_obj.quantity)*(purchase_obj.price_per_item)
        cart_obj.save()
        purchase_obj.delete()
        purchases = Purchase.objects.filter(cart=cart_obj)
        if not purchases:
            cart_obj.delete()
        return JsonResponse({'status': 'OK'})
    else:
        raise Http404("Page not found")


@login_required(login_url='mainpage')
def checkout_cart(request):
    if request.method == 'POST':
        form = AddressForm()
        return render(request, 'product/checkout_cart.html', {'address_form': form})
    else:
        raise Http404("Page not found")


@login_required(login_url='mainpage')
def payment(request):
    if request.method == 'POST':
        shipping_details = request.POST
        cart_obj = Cart.objects.filter(user=request.user.id, is_paid__exact='no').first()
        cart_obj.address = shipping_details['address']
        cart_obj.mobno = shipping_details['mobno']
        cart_obj.save()
        purchases = Purchase.objects.filter(cart=cart_obj)
        for item in purchases:
            product = ProductForm.objects.filter(id=item.name.id).first()
            # print(product.stock)
            product.stock = product.stock - item.quantity
            product.save()
            # print(product.stock)
        response = insta(request.user.email,request.user.username,cart_obj.mobno,request.build_absolute_uri(reverse('payment_details')),cart_obj.total_payment)
        # print(response)
        cart_obj.transaction_id = response['payment_request']['id']
        cart_obj.date = datetime.now()
        cart_obj.save()
        return redirect(response['payment_request']['longurl'])
    else:
        raise Http404("Page not found")



def insta(email, name, phone, redirect_url, amount):
    response = settings.INSTAMOJO_API.payment_request_create(
                    amount=str(amount),
                    purpose='ordering_items',
                    buyer_name=name,
                    send_email=True,
                    email=email,
                    send_sms=True,
                    phone=phone,
                    redirect_url=redirect_url,
                    #webhook=webhook, impp - webhook function must be csrf_exempt as instamojo server
                    # sends a post request to our server but without csrf token
            )
    return response


@login_required(login_url='mainpage')
def payment_details(request):
    try:
        payment_status = request.GET['payment_status']
        payment_request_id = request.GET['payment_request_id']
        payment_id = request.GET['payment_id']
    except:
        raise Http404('Page not found')

    if payment_status == 'Credit':
        product_prices = []
        cart_obj = Cart.objects.filter(user=request.user.id,is_paid__exact='no',transaction_id__exact=payment_request_id).first()
        cart_obj.transaction_id = payment_id
        cart_obj.is_paid = 'yes'
        cart_obj.save()
        purchases = Purchase.objects.filter(cart=cart_obj)
        for product in purchases:
            product_prices.append(product.quantity*product.price_per_item)
        return render(request, 'product/payment_details.html', {'cart': cart_obj, 'purchases': zip(purchases,product_prices)})

def display(request):
    address = request.POST.get('address')
    context = {
        'address' : address,
    }
    return render(request, 'product/final.html', context=context)

# def contact(request):
#     return render(request,'contact.html')

