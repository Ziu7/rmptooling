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
from .models import Discipline, Location, Tool, ToolSN, VaultLog, BorrowLog
from .forms import newToolSNForm, BorrowToolForm, NewLocationForm

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
class BorrowedToolsByUserListView(LoginRequiredMixin, generic.ListView):
	model = VaultLog
	template_name ='catalog/toolsn_list_borrowed_user.html'
	def get_queryset(self):
		return BorrowLog.objects.filter(isreturned = False, borrower=self.request.user).select_related()

#View for tools on loan by all users
class BorrowedToolsByAllListView(PermissionRequiredMixin, generic.ListView):
	permission_required = 'catalog.can_mark_returned'
	model = VaultLog
	template_name ='catalog/toolsn_list_borrowed_all.html'
	def get_queryset(self):
		return BorrowLog.objects.filter(isreturned = False).select_related()

#Vault Log View
class VaultLogList(LoginRequiredMixin, generic.ListView):
	model = VaultLog
	#We want to get all of the vault log data and pre-grab any related data
	def get_queryset(self):
		return VaultLog.objects.select_related()

#Borrow Log View
class BorrowLogList(LoginRequiredMixin, generic.ListView):
	model = BorrowLog
	def get_queryset(self):
		return BorrowLog.objects.select_related()

####################################### Renew Tool Form

@permission_required('catalog.can_mark_returned') #can_mark_returned permission required to renew
def borrow_tool(request,pk):
	tool_sn=get_object_or_404(ToolSN, pk=pk)
	if request.method == 'POST':
		#create a form instance and populate it with data from the request
		form = BorrowToolForm(request.POST)
		#check if the form is valid:
		if form.is_valid():
			log = BorrowLog(toolsn = tool_sn, borrower = request.user, borrowdate = date.today(), 
			reason=form.cleaned_data['reason'], notes=form.cleaned_data['notes'])
			log.save()
			#redirect to a new URL:
			return HttpResponseRedirect(reverse('borrowed-tools'))
	
	form = BorrowToolForm()
	return render(request, 'catalog/tool_borrow.html', {'form':form, 'toolsn':tool_sn})

# Class based forms for MODEL: ToolSN
def create_toolsn(request,pk):
	tool = get_object_or_404(Tool, pk=pk)
	if request.method == 'POST':
		form = newToolSNForm(request.POST)
		
		if form.is_valid():
			t = ToolSN(tool=tool, sn=form.cleaned_data['sn'], location=form.cleaned_data['location'], 
			pm=form.cleaned_data['pm'], repair=form.cleaned_data['repair'], comments=form.cleaned_data['comments'])
			t.save()
			return HttpResponseRedirect(reverse('tool-detail', kwargs={'pk':pk}))
	
	form = newToolSNForm()
	return render(request, 'catalog/toolsn_create.html', {'form':form, 'tool':tool})



class ToolSNUpdate(LoginRequiredMixin, UpdateView):
	model = ToolSN
	fields = ['sn','location','pm','repair','comments']

	def get_success_url(self):
		return reverse('toolsn-detail', kwargs={'pk': self.kwargs['pk']})

	# set borrower to the user logged in who updated the ToolSN
	def form_valid(self, form):
		toolsn = form.save(commit=False)
		toolsn.save()
		return HttpResponseRedirect(self.get_success_url())

class ToolSNDelete(LoginRequiredMixin, DeleteView):
	model = ToolSN
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
