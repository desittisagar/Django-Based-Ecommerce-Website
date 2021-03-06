from django.shortcuts import render

# Create your views here.
from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import LoginForm, RegisterForm, GuestForm
from django.contrib.auth import authenticate, login,get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.http import is_safe_url
from .models import GuestEmail

User = get_user_model()

def guest_login_view(request):
	form = GuestForm(request.POST or None)
	context = {
		"form":form,
		}
	next_ = request.GET.get('next')	
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post
	if form.is_valid():
		print(form.cleaned_data)
		email	 = form.cleaned_data.get("email")
		guest_email = GuestEmail.objects.create(email = email)
		request.session['guest_email_id'] = guest_email.id
		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)
		else:	
			return redirect("/register/")	
	return redirect("/register/")

def login_page(request):
	form = LoginForm(request.POST or None)
	context = {
		"form":form,
		}
	next_ = request.GET.get('next')	
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(request,username = username, password = password)
		print(request.user.is_authenticated)
		if user is not None:
			print(request.user.is_authenticated)
			print("sagar")
			login(request,user)
			try:
				request.session['guest_email_id']
			except:
				pass	
			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
			else:	
				return redirect("/")
		else:
			print("error")	
	return render(request,"accounts/login.html",context)


#User = get_user_model()
def register_page(request):
	#form = UserCreationForm(request.POST or None)
	form = RegisterForm(request.POST or None)
	context = {
	"form":form,
	}
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		new_user = User.objects.create_user(username, email, password)
		print(new_user)
	return render(request,"accounts/register.html",context)	