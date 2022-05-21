from .models import Category,SUPERCATEGORY_CHOICES
from users.forms import UserProfileForm, UserLoginForm

def all_categories(request):
    signup_form = UserProfileForm()
    login_form = UserLoginForm()
    data = {}
    for category in SUPERCATEGORY_CHOICES:
        data.update({category[1]: Category.objects.filter(superCategory=category[0])})
    return {'login_form': login_form,'signup_form': signup_form,'data': data}