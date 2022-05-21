from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url( r'^login/',views.login1, name='login'),
    url( r'^logout/',auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    url(r'^signup/', views.signup, name='signup'),
]