from django.db import models
from django.db.models.signals import post_save
# Create your models here.
from django.conf import settings
from accounts.models import GuestEmail

User  = settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
	def new_or_get(self,request):
		user = request.user
		guest_form_id = request.session.get('guest_email_id')
		billing_profile = None
		created = False
		if user.is_authenticated:
			billing_profile, created = self.model.objects.get_or_create(user = user, email = user.email)
		elif guest_form_id is not None:
			guest_obj = GuestEmail.objects.get(id = guest_form_id)
			billing_profile, created = self.model.objects.get_or_create(email = guest_obj.email)

		else:
			pass
		return billing_profile, created

class BillingProfile(models.Model):
	user 		= models.OneToOneField(User, null=True, blank=True, on_delete = True)
	email 		= models.EmailField()
	active		= models.BooleanField(default=True)
	timestamp	= models.DateTimeField(auto_now_add=True)
	update		= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.email
	objects = BillingProfileManager()	


def user_created_receiver(sender, instance, created, *args, **kwargs):
	if created and instance.email:
		BillingProfile.objects.get_or_created(user=instance, email=instance.email)

post_save.connect(user_created_receiver,sender=User)				