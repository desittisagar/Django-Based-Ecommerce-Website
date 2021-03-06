from django.db import models
import random
import os
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import unique_slug_generator
from django.urls import reverse
from django.db.models import Q

def get_filename_ext(filename):
	base_name = os.path.basename(filename)
	name, ext = os.path.splitext(base_name)
	return name, ext

# Create your models here.
def upload_img_path(instance,filename):
	print(instance)
	print(filename)
	new_filename = random.randint(1,12345)
	print(new_filename)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(
		new_filename=new_filename,
		ext=ext)
	return "products/{new_filename}/{final_filename}".format(
		new_filename=new_filename,
		final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet):
	def featured(self):
		return self.filter(featured=True)

	def active(self):
		return self.filter(active=True)	

	def search(self, query):
		lookups=(Q(title__icontains=query) | 
				Q(description__icontains=query) |
				Q(price__icontains=34) |
				Q(tag__title__icontains=query))

		return self.filter(lookups).distinct()	

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self):
		return self.get_queryset().active()

	def featured(self):
		return self.get_queryset().featured()

	def get_by_id(self,id):
		qs = self.get_queryset().filter(id=id)	
		if qs.count() == 1:
			return qs.first()
		return None	

	def search(self, query):
		lookups=Q(title__icontains=query) | Q(description__icontains=query)	
		return self.get_queryset().active().search(query)

class Product(models.Model):
	title 		= models.CharField(max_length = 120)
	slug		= models.SlugField(blank=True)
	description = models.TextField()
	price		= models.DecimalField(decimal_places = 2, max_digits = 10, default=39.90)
	image		= models.ImageField(upload_to=upload_img_path,null=True, blank=True)
	featured	= models.BooleanField(default = False)
	active		= models.BooleanField(default = True)
	timestamp	= models.DateTimeField()

	objects = ProductManager()
	def get_absolute_url(self):
		#return "/products/{slug}/".format(slug=self.slug)
		return reverse("products:detail",kwargs={"slug":self.slug})

	def __str__(self):
		return self.title

def prodduct_pre_save_receiver(sender,instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(prodduct_pre_save_receiver,sender=Product)		