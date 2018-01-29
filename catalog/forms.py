from django.utils.translation import ugettext_lazy as _ #for use with Verbose Name for models (allow easy
from django import forms #form class for creating user input forms
from django.core.exceptions import ValidationError
import datetime #for checking renewal date range
from .models import Discipline, Location, Tool, ToolSN

# Renew tool form
class RenewToolForm (forms.Form):
	renew_date = forms.DateField(help_text="Enter date between now and 4 weeks.")

	def clean_renew_date(self):
		data = self.cleaned_data['renew_date']

		#check date is not in the past.
		if data < datetime.date.today():
			raise ValidationError(_('Invalid date - date is in the past'))

		#check date is in range of renewal (4 weeks max)
		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_('Invalid date - cannot extend beyond 4 weeks'))

		# remember to always return the cleaned data
		return data

# New location Form
class NewLocationForm(forms.ModelForm):

	class Meta:
		model = Location
		fields ='__all__'

# Vault Status Update Out Form - Readonly Fields
class VaultUpdateOutForm(forms.ModelForm):
	class Meta:
		model = ToolSN
		fields = ['vault','vaultouttime']
		
	vaultouttime = forms.DateTimeField(disabled=True, label='Vault Out Time')
	vault = forms.CharField(disabled=True, label='Change Vault Status to')

# Vault Status Update In Form - Readonly Fields
class VaultUpdateInForm(forms.ModelForm):
	class Meta:
		model = ToolSN
		fields = ['vault','vaultintime']
		
	vaultintime = forms.DateTimeField(disabled=True, label='Vault In Time')
	vault = forms.CharField(disabled=True, label='Change Vault Status to')
