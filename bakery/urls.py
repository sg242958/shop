"""bakery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from store import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about-us', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('admin_login', views.admin_login, name='admin'),
    path('admin_login/admin_home', views.admin_home, name='admin_home'),
    path('admin_login/admin_user', views.admin_user, name='admin_user'),
    path('logout', views.Logout_Admin, name='logout'),
    path('logout_user', views.Logout_User, name='logout1'),
    path('admin_login/admin_add_category', views.admin_add_category, name='admin_add_category'),
    path('admin_login/view_category', views.view_category, name='view_category'),
    path('admin_login/category_delete/<int:id>/', views.category_delete, name='category_delete'),
    path('admin_login/product_delete/<int:id>/', views.product_delete, name='product_delete'),
    path('admin_login/add_product', views.add_product, name='add_product'),
    path('admin_login/view_product', views.view_product, name='view_product'),
    path('user', views.user_login, name='user'),
    path('home', views.user_home, name='home1'),
    path('user/profile', views.profile, name='profile'),
    path('user/user_edit', views.edit, name='edit'),
    path('user/change_password', views.change_password, name='change_password'),
    path('signup', views.signup, name='signup'),
    path('user/user_view_product', views.user_view_product, name='user_view_product'),
    path('user/user_home', views.user_homes, name='user_home'),
    path('user/send_feedback', views.send_feedback, name='send_feedback'),
    path('admin_login/view_feedback', views.view_feedback, name='view_feedback'),
    path('admin_login/feedback_delete/<int:id>/', views.feedback_delete, name='feedback_delete'),
    path('user/product_detail/<int:id>/', views.product_detail, name='product_detail'),
    path('user/add_cart/<int:id>/', views.add_cart, name='add_cart'),
    path('user/cart', views.cart, name='cart'),
    path('user/cart_product_delete/<int:id>/', views.cart_delete, name='delete'),
    path('user/buy_one/<int:id>/', views.buy_one, name='buy_one'),
    path('user/user_view_order', views.user_view_order, name='user_view_order'),
    path('admin_login/admin_view_order', views.admin_view_order, name='admin_view_order'),
    path('admin_login/admin_view_order1/<int:id>', views.admin_view_order1, name='admin_view_order1'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
