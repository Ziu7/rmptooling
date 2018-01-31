from django.utils.translation import ugettext_lazy as _ #for use with Verbose Name for models (allow easy
from django import forms #form class for creating user input forms
from django.core.exceptions import ValidationError
import datetime #for checking renewal date range
from .models import Discipline, Location, Tool, ToolSN

# Renew tool form
class BorrowToolForm (forms.Form):
	reason = forms.CharField(widget=forms.Textarea,help_text="Reason for the borrow")
	notes = forms.CharField(widget=forms.Textarea,help_text="Any notes regarding the borrow", required=False)

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
