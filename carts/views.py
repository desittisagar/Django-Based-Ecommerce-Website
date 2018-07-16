from django.shortcuts import render, redirect
from orders.models import Order
# Create your views here.
from .models import Cart
from products.models import Product
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.forms import GuestForm
from accounts.models import GuestEmail
from addresses.models import Address
from addresses.forms import AddressForm

def cart_home(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	
	return render(request,"carts/home.html",{"cart":cart_obj})

def checkout(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	order_obj = None
	if cart_created or cart_obj.products.count() == 0:
		return redirect("cart:home")

	loginform = LoginForm()
	guestform = GuestForm()
	address_form = AddressForm()
	#address_form_billing = AddressForm()

	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
	shipping_address_id = request.session.get("shipping_address_id",None)
	billing_address_id = request.session.get("billing_address_id",None)
	address_ = None
	if billing_profile is not None:
		if request.user.is_authenticated:
			address_ = Address.objects.filter(billing_profile = billing_profile)
		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

		if shipping_address_id:
			order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
			del request.session["shipping_address_id"]
		if billing_address_id:
			order_obj.billing_address = Address.objects.get(id=billing_address_id)
			del request.session["billing_address_id"]
		if 	shipping_address_id or billing_address_id:
			order_obj.save()	

	if request.method == "POST":
		is_done = order_obj.check_done()
		if is_done:
			order_obj.mark_paid()	
			request.session['cart_items'] = 0
			del request.session['cart_id']		
			return redirect("cart:success")

	context = {
	"order":order_obj,
	"billing_profile": billing_profile,
	"loginform": loginform,
	"guestform":guestform,
	"address_form":address_form,
	"address_":address_,
	#"address_form_billing":address_form_billing,
	}	
	
	return render(request,"carts/checkout.html",context)

def cart_update(request):
	print(request.POST)
	product_id = request.POST.get('product_id')
	if request.is_ajax():
		print("Ajax request")
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("show msg to user")
			return redirect("cart:home")
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
		else:
			cart_obj.products.add(product_obj)
		#return redirect(product_obj.get_absolute_url())
		request.session['cart_items'] = cart_obj.products.count()
	return redirect("cart:home")


def checkout_done(request):
	return render(request,"carts/checkout-done.html",{})	