from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import ContactForm,LoginForm, RegisterForm
from django.contrib.auth import authenticate, login,get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

def home_page(request):
	#print(request.session.get('first_name','Unknown'))
	context = {
	"title": "Today's Content",
	}
	if request.user.is_authenticated:
		context['premium_content'] = "yaaaaaay"
	return render(request,"home_page.html",context)

def about_page(request):
	return render(request,"home_page.html",{})

def contact_page(request):
	contact_form = ContactForm(request.POST or None)
	context = {
	"title":"contact-us",
	"content":"welcome to contact page",
	"form":contact_form,
	#"brand":"new brand name",
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
	if(request.method == "POST"):
		print(request.POST.get('fullname'))
	return render(request,"contact.html",context)

