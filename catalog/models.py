from django.db import models
from django.urls import reverse #used to generate urls by reversing the url pattern
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User #for use with methods associated with users
from datetime import date, datetime
import uuid #Currently used way of generating unique IDs for tools

#MODEL Discipline model for Primary and Secondary tool disciplines
class Discipline(models.Model):
	name = models.CharField(unique=True, max_length=100, help_text="Enter the discipline name")
	#order by names
	class Meta:
		ordering = ["name"]
		verbose_name = _("Tool Discipline")
	def __str__(self):
		return self.name

# MODEL Locations for the tool
class Location(models.Model):
	name = models.CharField(unique=True, max_length=200, help_text="Enter tool location.",verbose_name="location Name")
	address = models.CharField(max_length=200, verbose_name="street address", default="N/A")
	notes = models.TextField(max_length=1000, help_text="Any comments that would help find this location.", blank="True")

	class Meta:
		ordering = ["id"]
		permissions = (("can_add_location", "Can add location"),)
	def __str__(self):
		return self.name

# MODEL General information for tool by tool number
class Tool(models.Model):
	num = models.CharField(unique=True, max_length=100, verbose_name="Tool No.")
	name = models.CharField(max_length=200, verbose_name="tool name")
	minneeded = models.IntegerField(verbose_name="minimum tools requiried" , default = "0")
	draw = models.CharField(max_length=200,blank=True, verbose_name="tool drawing(s)")
	dcatid = models.CharField (max_length=100, blank = True, verbose_name="DNGS CatID")
	pcatid = models.CharField (max_length=100, blank = True, verbose_name="PNGS CatID")
	primdisc = models.ForeignKey(Discipline, on_delete=models.SET_NULL, 
	verbose_name="primary discipline", related_name="primdic_tool", null=True)
	secdisc = models.ForeignKey(Discipline, on_delete=models.SET_NULL, 
	verbose_name="secondary discipline", related_name="secdisc_tool", blank=True, null=True)
	notes = models.TextField(max_length=1000, help_text="Enter any notes for this tool as necessary.",blank=True)
	#toolpic = models.ImageField (blank=True, null=True) If tool pics are available on intranet using toolID/num won't need this

	class Meta:
		ordering = ["id", "num"]
		verbose_name = _("Tool")
		permissions = (("can_edit_tool", "Can edit Tool"),)

	#String representing the tool name
	def __str__(self):
		return self.num + " ("+ self.name + ")" if self.num != self.name else self.num

	#returns the url to access a particular tool instance
	def get_absolute_url(self):
		return reverse('tool-detail', args=[str(self.id)]) #Maybe use tool name instead of ID in urls?

	def get_toolcount(self):
		return self.toolsn_set.count()

	def get_damagedtoolcount(self):
		return self.toolsn_set.filter(repair='True').count()

	def sufficienttools(self):
		return ( self.get_toolcount() - self.get_damagedtoolcount() ) > self.minneeded

#Look into custom managers

#MODEL tool instance by SN (for each specific tool)

class ToolSN (models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for tool")
	tool = models.ForeignKey(Tool,on_delete=models.CASCADE, verbose_name="tool no.")
	sn = models.CharField(max_length=10, verbose_name="tool SN")
	location = models.ForeignKey(Location,on_delete=models.SET_NULL, verbose_name="location of the tool", null=True)
	pm = models.BooleanField(max_length=50, help_text="Is PM complete for this tool?")
	repair = models.BooleanField(max_length=5, help_text="Does this tool need to be repaired?")
	checkdate = models.DateTimeField(verbose_name="time when tool was checked", null="True")
	comments = 	models.TextField(max_length=1000, help_text="Enter any comments for this tool as necessary.",blank=True)
	#check overdue tool
	@property
	def is_checkedout(self):
		#Check if the most recent vaultlog hasn't been returned yet
		return not self.vaultlog_set.latest().isreturned

	def mostRecentBorrow(self):
		#Return the most recent vault log
		return self.vaultlog_set.latest()

	class Meta:
		ordering = ["tool","sn"] #order by tool number when returned in a query
		verbose_name = _("Tool SN")

	#string representing the model object
	def __str__(self):
		return "%s SN-%s" % (self.tool, self.sn) if self.sn is not '-' else "%s" % self.tool

class VaultLog(models.Model):
	toolsn = models.ForeignKey(ToolSN, on_delete=models.DO_NOTHING, verbose_name="loaned tool")
	borrower = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="tool loaned to", related_name="borrower_log")
	approvedby = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="who approved the borrow", related_name="manager_log")
	borrowdate = models.DateField(verbose_name="time tool was checked out")
	returndate = models.DateField(verbose_name="time tool must be returned")
	isreturned = models.BooleanField(verbose_name="has tool been returned")
	notes = models.TextField(verbose_name="Logging Notes", null=True, blank=True)

	@property
	def is_overdue(self):
		return date.today() > self.returndate

	class Meta:
		verbose_name = ('Tool Vault Log')
		get_latest_by = ('borrowdate')

#Creatable tasks that can show what tools to take on what jobs, what disciplines they fall under, etc.
class Job(models.Model):
	name = models.CharField(max_length=200, verbose_name="job name")
	description = models.TextField(max_length=1000,help_text="Description of what the job entails", blank=True)
	image = models.ImageField(blank=True, null=True) #Needed for the design
	directions = models.TextField(max_length=1000,help_text="Step by step instructions for this job", blank=True)
	previousJob = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name = "previous required job", null=True)
	primdisc = models.ForeignKey(Discipline,on_delete=models.DO_NOTHING, verbose_name = "primary discipline", related_name="primdisc_job")
	secdisc = models.ForeignKey(Discipline, on_delete=models.DO_NOTHING, verbose_name = "secondary discipline", related_name="secdisc_job")

#Relational Table
class JobTool(models.Model):
	jobId = models.ForeignKey(Job , on_delete=models.CASCADE) #If they delete a job delete everything related in this table (cascade)
	toolId = models.ForeignKey(Tool, on_delete=models.DO_NOTHING) #If they delete a tool don't worry just remove it from the relation
