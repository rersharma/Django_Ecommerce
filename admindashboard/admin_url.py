from django.urls import path,include
from . import views
urlpatterns = [
path('check_user',views.check_user,name="check_user"),
path("admin_dashboard",views.admin_dash,name="admin_dashboard"),
path('product_add',views.product_add,name='product_add'),
path('logout',views.Logout,name='logout'),
path('manage_product',views.manage_product,name='manage_product'),
path('product_delete/<int:id>/',views.product_delete,name='product_delete'),
path('userorder',views.userorder,name="userorder"),
path('remark_order',views.remark_order,name='remark_order'),
path("inbox",views.admininbox,name="inbox")
]