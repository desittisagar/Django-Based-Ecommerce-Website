from django.conf.urls import url

from .views import cart_home, cart_update,checkout,checkout_done
app_name = 'carts'

urlpatterns = [
	url(r'^$',cart_home, name='home'),
	url(r'^update/$',cart_update,name = 'update'),
	url(r'^checkout/$',checkout,name = 'checkout'),
	url(r'^checkout/success/$',checkout_done,name = 'success'),
    
]


