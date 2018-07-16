from .models import Address
from django import forms

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = [
		#'billing_profile',
		#'Address_type',
		'address_line_1',
		'address_line_2',
		'city',
		'country',
		'state',
		'state',
		'postal_code',
		]