from django.urls import path
from . import views
urlpatterns = [
    path("",views.Home_Main_Page,name="Start Page"),
    path("about",views.about,name="about"),
    path('contact',views.contacts,name="contact"),
    path("Newuser",views.create_account,name="Newuser"),
    path("login",views.login,name="Login Page"),
    path("dashboard",views.Dashboard,name="dashboard"),
    path("logout",views.Logout,name="Logout User"),
    path("changepaasword",views.change_password,name="changepaasword"),
    path("order",views.product_order,name="Product Order"),
    path("buynow",views.buynow,name='buynow'),
    path("my_order_list",views.my_order_list,name="my_order_list"),
    path("cancelorder/<int:id>/",views.cancelorder,name="cancelorder"),
    path("myprofile",views.myprofile,name="myprofile"),
    path("userinbox",views.userinbox,name="userinbox"),
]