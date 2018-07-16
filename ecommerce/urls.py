"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from accounts.views import login_page,register_page, guest_login_view
from .views import home_page,about_page,contact_page
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from carts.views import cart_home
from django.contrib.auth.views import LogoutView

from addresses.views import checkout_address_view, checkout_address_use
#from .models import art

urlpatterns = [
	url(r'^$',home_page,name='home'),
	url(r'^about/$',about_page, name = 'about'),
	url(r'^contact/$',contact_page, name = 'contact'),
	url(r'^login/$',login_page,name = 'login'),
	url(r'^register/guest$',guest_login_view,name = 'guest'),
	url(r'^logout/',LogoutView.as_view(),name = 'logout'),
	url(r'^checkout/address/view',checkout_address_view,name = 'checkout_address'),
	url(r'^checkout/address/use',checkout_address_use,name = 'checkout_address_reuse'),
	#url(r'^cart/',cart_home,name = 'cart'),
	url(r'^cart/',include("carts.urls", namespace='cart')),
	url(r'^bootstrap/$',TemplateView.as_view(template_name = 'bootstrap/example.html')),
	url(r'^product/',include("products.urls", namespace='products')),
	url(r'^search/',include("search.urls", namespace='search')),	 url(r'^register/',register_page, name='register'),
	
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
	urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
	urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
