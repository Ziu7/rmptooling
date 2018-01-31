from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy #used to generate urls by reversing the url pattern
from django.shortcuts import render
from django.contrib.auth.decorators import login_required #login requirement for function based views
from django.contrib.auth.mixins import LoginRequiredMixin #login requirement for class based views
from django.contrib.auth.decorators import permission_required #permission requirement for function based views
from django.contrib.auth.mixins import PermissionRequiredMixin #permission requirement for class based views
from django.contrib.auth.models import User #for use with methods associated with users
from django.db import models
from django import forms #form class for creating user input forms
from .models import Discipline, Location, Tool, ToolSN, VaultLog
from .forms import VaultUpdateInForm, VaultUpdateOutForm, RenewToolForm, NewLocationForm

#View for index (regular function)
@login_required
def index(request):
	num_tool=Tool.objects.all().count()
	num_toolSN=ToolSN.objects.all().count()
	num_repair=ToolSN.objects.filter(repair='True').count()
	num_pm=ToolSN.objects.filter(pm='False').count()
	#Tools in need of urgent attention (Under min req)
	urgent_tools = Tool.objects.raw('select c.*, (Select count(*) from catalog_toolsn as s where c.id = s.tool_id and s.repair = 0) as num_working from catalog_tool as c where num_working < c.minneeded')
	return render(
		request,
		'catalog/index.html',
		context={'urgent_tools':urgent_tools,'num_tool':num_tool,'num_toolSN':num_toolSN,'num_repair':num_repair,'num_pm':num_pm},
	)

#View for Location List (class based, list view)
class LocationView(LoginRequiredMixin, generic.ListView):
	model = Location

#View for Tool List (class based, list view)
class ToolListView(LoginRequiredMixin, generic.ListView):
	model = Tool

#View for ToolSN List (class based, list view)
class ToolSNView(LoginRequiredMixin, generic.ListView):
	model = ToolSN

#View for all items in need of repair
class ToolSNRepairView(LoginRequiredMixin, generic.ListView):
	model = ToolSN
	def get_queryset(self):
		return ToolSN.objects.filter(repair='True')

#View for all items in need of PM
class ToolSNPMView(LoginRequiredMixin, generic.ListView):
	model = ToolSN
	def get_queryset(self):
		return ToolSN.objects.filter(pm='False')

#View for detailed tool list for each SN (class based, detail view)
class ToolDetailView(LoginRequiredMixin, generic.DetailView):
	model = Tool

#View for detailed tool list by location (class based, detail view)
class LocationDetailView(LoginRequiredMixin, generic.DetailView):
	model = Location

#View for detailed view for ToolSN
class ToolSNDetailView(LoginRequiredMixin, generic.DetailView):
	model = ToolSN

#View for tools on loan by User
class LoanedToolsByUserListView(LoginRequiredMixin, generic.ListView):
	model = VaultLog
	template_name ='catalog/toolsn_list_borrowed_user.html'
	def get_queryset(self):
		return VaultLog.objects.filter(isreturned = False, borrower=self.request.user).select_related()

#View for tools on loan by all users
class LoanedToolsByAllListView(PermissionRequiredMixin, generic.ListView):
	permission_required = 'catalog.can_mark_returned'
	model = VaultLog
	template_name ='catalog/toolsn_list_borrowed_all.html'
	def get_queryset(self):
		return VaultLog.objects.filter(isreturned = False).select_related()

#Vault Log View
class VaultLogList(LoginRequiredMixin, generic.ListView):
	model = VaultLog
	#We want to get all of the vault log data and pre-grab any related data
	def get_queryset(self):
		return VaultLog.objects.select_related()
	
####################################### Renew Tool Form

@permission_required('catalog.can_mark_returned') #can_mark_returned permission required to renew
def renew_tool(request,pk):
	tool_sn=get_object_or_404(ToolSN, pk=pk)
	tool_log = tool_sn.mostRecentBorrow()
	if request.method == 'POST':
		#create a form instance and populate it with data from the request
		form = RenewToolForm(request.POST)
		#check if the form is valid:
		if form.is_valid():
			newLog = VaultLog(toolsn=tool_sn, borrower=tool_log.borrower, approvedby = request.user, borrowdate = date.today(), returndate = form.cleaned_data['expiry_date'])
			newLog.save()
			tool_log.isreturned = True
			tool_log.notes = "Return date extended" 
			#Add to notes everytime something is renewed, or kill the previous entry and add a new one. Adding to notes what happened.
			tool_log.save()
			tool_sn.save()
			#redirect to a new URL:
			return HttpResponseRedirect(reverse('loaned-tools'))
	else:
		default_renew_date = date.today() + timedelta(weeks=3) # default renew date + 3weeks
		form = RenewToolForm(initial={'expiry_date':default_renew_date,})

	return render(request, 'catalog/tool_renew.html', {'form':form, 'toolsn':tool_sn, 'log':tool_log })

#############################FORMS: Class Based#############################

# Class based forms for MODEL: ToolSN
class ToolSNCreate(LoginRequiredMixin, CreateView):
	model = ToolSN
	fields = ['tool','sn','location','pm','repair','checkdate','comments']
	initial={'checkdate':date.today(),'tool': "Bolts"}

	def get_success_url(self):
		return reverse('tool-detail', kwargs={'pk': self.kwargs['pk']})

class ToolSNUpdate(LoginRequiredMixin, UpdateView):
	model = ToolSN
	fields = ['sn','location','pm','repair','checkdate','comments']
	initial={'checkdate':date.today()}

	def get_success_url(self):
		return reverse('toolsn-detail', kwargs={'pk': self.kwargs['pk']})

	# set borrower to the user logged in who updated the ToolSN
	def form_valid(self, form):
		toolsn = form.save(commit=False)
		toolsn.save()
		return HttpResponseRedirect(self.get_success_url())

class ToolSNDelete(LoginRequiredMixin, DeleteView):
	model =ToolSN
	success_url = reverse_lazy('tool')

# Class based forms for MODEL: Tool
class ToolCreate(LoginRequiredMixin, CreateView):
	model = Tool
	fields = '__all__'
	success_url = reverse_lazy('tool')

# Class based forms for MODEL: Location
class LocationCreate(LoginRequiredMixin, CreateView):
	model = Location
	fields = '__all__'

	success_url = reverse_lazy('location')

class LocationUpdate(LoginRequiredMixin, UpdateView):
	model = Location
	fields = ['id','location']
	success_url = reverse_lazy('location')

#Tool Checkout
class VaultUpdate(LoginRequiredMixin, UpdateView):
	permission_required = 'catalog.can_log_vault'
	template_name ='catalog/vaultlogout_form.html'	
	model = ToolSN
	form_class= VaultUpdateOutForm
	initial={'vaultouttime': datetime.now(), 'vault':'Out'}	

	success_url = reverse_lazy('vaultlogout')

###########FUNCTION BASED LOCATION CREATE FORM###########
def add_location(request):
	loc=Location
	if request.POST:
		form = NewLocationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('location'))
	else:
		form = NewLocationForm()#initial={'location':Location.objects.get(id=2)})

	return render(request, 'catalog/location_form _function.html', {'form':form,'loc':loc})
