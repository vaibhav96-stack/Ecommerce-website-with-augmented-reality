from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.mainpage, name='mainpage'),
    url(r'^(?P<product_id>[0-9]+)/$', views.productpage, name='productpage'),
    # url(r'^(?P<product_id>[0-9]+)/order_details/$', views.order_details, name='order_details'),
    url(r'^add_to_cart/$', views.add_to_cart, name='add_to_cart'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^update_cart/$', views.update_cart, name='update_cart'),
    url(r'^delete_item/$', views.delete_item, name='delete_item'),
    url(r'^checkout_cart/$', views.checkout_cart, name='checkout_cart'),
    url(r'^payment/$', views.payment, name='payment'),
    url(r'^payment_details/$', views.payment_details, name='payment_details'),
    path('arr_real<int:product_id>',views.arr_real,name="arr_real"),
    path('temp<int:product_id>', views.temp,name="temp"),
    path('subproduct<int:subcat>',views.subproduct,name="subproduct"),
    path('display', views.display,name="display"),
    path('contact',views.contact,name='contact'),
    path('about', views.about, name='about'),
]