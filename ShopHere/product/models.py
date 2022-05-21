from django.db import models
from tinymce.models import HTMLField
from users.models import User
from tinymce import models as tinymce_models
from PIL import Image


SUPERCATEGORY_CHOICES = (

        (3, 'Tiles'),

)

class Category(models.Model):
    name = models.CharField(max_length=250)
    superCategory = models.IntegerField(choices=SUPERCATEGORY_CHOICES, default=1)
    description = models.CharField(max_length=5000)
    categoryIcon = models.ImageField(upload_to='category_images/', height_field=None, width_field=None, max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class ProductForm(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=5000)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    uploadedDate = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', height_field=None, width_field=None, max_length=100)

    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = 'Products'

    def save(self):
        super().save()  # saving image first

        img = Image.open(self.image.path) # Open image using self

        if img.height > 500 or img.width > 300:
            new_img = (300, 500)
            img.thumbnail(new_img)
            img.save(self.image.path)  # saving image at the same path

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    address = models.TextField(blank=True)
    mobno = models.CharField(max_length=10,blank=True)
    total_payment = models.FloatField()
    is_paid = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100,blank=True,default='')
    date = models.DateTimeField(auto_now=True)



class Purchase(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    name = models.ForeignKey(ProductForm, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    price_per_item = models.PositiveIntegerField()

    def __str__(self):
        return str('Username--') + str(self.cart.user.username) + str(' Product_name--') + str(self.name.name) + str(' Quantity--') + str(self.quantity)


    # phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))