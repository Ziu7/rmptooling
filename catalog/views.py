from datetime import date
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
from django.db.models import Count,Q,F
from .models import Location, Tool, ToolSN, VaultLog, BorrowLog
from .forms import newToolSNForm, BorrowToolForm
from django.db import connection

#View for index (regular function)
@login_required
def index(request):
	num_tool=Tool.objects.all().count()
	num_toolSN=ToolSN.objects.all().count()
	num_repair=ToolSN.objects.filter(repair='True').count()
	num_pm=ToolSN.objects.filter(pm='False',tool__pmneeded='True').count()
	#Tools in need of urgent attention (Under min req)
	urgent_tools = Tool.objects.annotate(working_count=Count('toolsn',filter=Q(toolsn__repair=False)),total_count=Count('toolsn')).filter(working_count__lt= F('minneeded') ).select_related('primdisc','secdisc')
	with connection.cursor() as cursor:
	    cursor.execute('select COUNT(*) as num from `catalog_toolsn` s1, `catalog_toolsn` s2 where s1.tool_id=s2.tool_id AND s1.sn=s2.sn')
	    row = cursor.fetchone()
	connection.close()
	return render(
		request,
		'catalog/index.html',
		context={'urgent_tools':urgent_tools,'num_tool':num_tool,'num_toolSN':num_toolSN,'num_repair':num_repair,'num_pm':num_pm,'num_dup':row},
	)

#View for Location List (class based, list view)
class LocationView(LoginRequiredMixin, generic.ListView):
	model = Location
	def get_queryset(self):
	    return Location.objects.annotate(tool_count=Count('toolsn'))

#View for Tool List (class based, list view)
class ToolListView(LoginRequiredMixin, generic.ListView):
	model = Tool
	def get_queryset(self):
	    return Tool.objects.annotate(working_count=Count('toolsn',filter=Q(toolsn__repair=False)),total_count=Count('toolsn')).select_related('primdisc','secdisc')

#View for ToolSN List (class based, list view)
class ToolSNView(LoginRequiredMixin, generic.ListView):
	model = ToolSN
	def get_queryset(self):
	    return ToolSN.objects.select_related('location','tool__primdisc','tool__secdisc')

#View for all items in need of repair
class ToolSNRepairView(LoginRequiredMixin, generic.ListView):
	model = ToolSN
	def get_queryset(self):
		return ToolSN.objects.filter(repair='True').select_related('location','tool__primdisc','tool__secdisc')

#View for all items in need of PM
class ToolSNPMView(LoginRequiredMixin, generic.ListView):
	model = ToolSN
	def get_queryset(self):
		return ToolSN.objects.filter(tool__pmneeded=1,pm=0).select_related('location','tool__primdisc','tool__secdisc')

#Temporary view for all duplicates
def duplicateTools(request):
	duplicate_tools =  ToolSN.objects.raw('select *,count(*) as dupcount from `catalog_toolsn` group by `tool_id`,`sn` having count(*) > 1')
	return render(
		request,
		'catalog/toolsn_dups.html',
		context={'duplicate_tools':duplicate_tools},
	)

#View for detailed tool list for each SN (class based, detail view)
class ToolDetailView(LoginRequiredMixin, generic.DetailView):
	model = Tool

#View for detailed tool list by location (class based, detail view)
class LocationDetailView(LoginRequiredMixin, generic.DetailView):
	model = Location
	#def get_queryset(self):
	#    return Location.objects.select_related('toolsn__tool__primdisc','toolsn__tool__secdisc')

#View for detailed view for ToolSN
def ToolSNDetailView(request,pk,action=''):
	toolSN = get_object_or_404(ToolSN, pk=pk)
	if action == "In":
	    if toolSN.is_invault:
	        message = "Tool is already in the vault"
	        status = "danger"
	    else:
	        newVault = VaultLog(toolsn=toolSN, action=action.title())
	        newVault.save()
	        message = "Tool has been vaulted in"
	        status = "success"
	elif action == "Out":
	    if toolSN.is_invault:
	        message = "Tool has been vaulted out"
	        status = "success"
	        newVault = VaultLog(toolsn=toolSN, action=action.title())
	        newVault.save()
	    else:
	        message = "Tool is already out of the vault"
	        status = "danger"
	else:
	    message = ""
	    status = ""
	return render(request, 'catalog/toolsn_detail.html', {'toolsn':toolSN , 'message':message, 'status':status})

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
		form = newToolSNForm(request.POST,pm_needed=tool.pmneeded)
		if form.is_valid():
			t = ToolSN(tool=tool, sn=form.cleaned_data['sn'], location=form.cleaned_data['location'], station=form.cleaned_data['station'],
			pm=form.cleaned_data['pm'] if tool.pmneeded else "None" , repair=form.cleaned_data['repair'], comments=form.cleaned_data['comments'])
			t.save()
			return HttpResponseRedirect(reverse('tool-detail', kwargs={'pk':pk}))

	form = newToolSNForm(pm_needed=tool.pmneeded) #Edit this to disable PM if it's not needed for this tool
	return render(request, 'catalog/toolsn_create.html', {'form':form, 'tool':tool})

#Update Classes

class ToolSNUpdate(LoginRequiredMixin, UpdateView):
	model = ToolSN
	fields = ['sn','station','location','pm','repair','comments']

	def get_success_url(self):
		return reverse('toolsn-detail', kwargs={'pk': self.kwargs['pk']})

	# set borrower to the user logged in who updated the ToolSN
	def form_valid(self, form):
		toolsn = form.save(commit=False)
		toolsn.save()
		return HttpResponseRedirect(self.get_success_url())

class ToolUpdate(LoginRequiredMixin, UpdateView):
	model = Tool
	fields = ['minneeded','draw','drawingLink','dcatid','pcatid','primdisc','secdisc','pmneeded','notes']

	def get_success_url(self):
		return reverse('tool-detail', kwargs={'pk': self.kwargs['pk']})

	# set borrower to the user logged in who updated the ToolSN
	def form_valid(self, form):
		toolsn = form.save(commit=False)
		toolsn.save()
		return HttpResponseRedirect(self.get_success_url())

#Delete Classes

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
