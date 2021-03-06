from django.db import models
from django.urls import reverse #used to generate urls by reversing the url pattern
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User #for use with methods associated with users
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
	name = models.CharField(max_length=200, help_text="Enter tool location.",verbose_name="location Name")
	stationChoices = (
	    ('A','Annex'),
	    ('D','DNGS'),
	    ('T','TMB'),
	)
	station = models.CharField(max_length=1, verbose_name="station", choices=stationChoices, default="D")
	notes = models.TextField(max_length=1000, help_text="Any comments that would help find this location.", blank="True")
	#Order by names
	class Meta:
		ordering = ["name"]
		verbose_name = _("Tool Location")
		unique_together = ('station', 'name',)
	def __str__(self):
		return self.get_station_display() + " " + self.name

# MODEL General information for tool by tool number
class Tool(models.Model):
	num = models.CharField(unique=True, max_length=100, verbose_name="tool no.", default="-")
	name = models.CharField(max_length=200, verbose_name="tool name", default="-")
	minneeded = models.IntegerField(verbose_name="minimum tools requiried" , default = "3")
	draw = models.CharField(max_length=200,blank=True, verbose_name="tool drawing(s)")
	drawingLink = models.CharField(max_length=200,blank=True, verbose_name="drawing link")
	dcatid = models.CharField (max_length=100, blank = True, verbose_name="DNGS CatID")
	pcatid = models.CharField (max_length=100, blank = True, verbose_name="PNGS CatID")
	primdisc = models.ForeignKey(Discipline, on_delete=models.SET_NULL, verbose_name = "primary discipline", related_name="primdic_tool", null=True)
	secdisc = models.ForeignKey(Discipline, on_delete=models.SET_NULL, verbose_name = "secondary discipline", related_name="secdisc_tool", blank=True, null=True)
	pmneeded = models.BooleanField(help_text = "Will this tool have PM checks done?", default=False, verbose_name = "PM checks required")
	notes = models.TextField(max_length=1000, help_text="Enter any notes for this tool as necessary.",blank=True)
	#toolpic = models.ImageField (blank=True, null=True) If tool pics are available on intranet using toolID/num won't need this
	class Meta:
		ordering = ["id", "num"]
		verbose_name = _("Tool")

	#String representing the tool name
	def __str__(self):
		return self.num + " ("+ self.name + ")" if self.num != self.name else self.num

	#returns the url to access a particular tool instance
	def get_absolute_url(self):
		return reverse('tool-detail', args=[str(self.id)]) #Maybe use tool name instead of ID in urls?

	#Properties determined by the toolSNs
	@property
	def toolcount(self):
		return self.toolsn_set.count()
	@property
	def damagedcount(self):
		return self.toolsn_set.filter(repair='1').count()
	@property
	def workingcount(self):
		return self.toolsn_set.filter(repair='0').count()
	@property
	def pmcount(self):
		return self.toolsn_set.filter(pm='0').count()
	@property
	def sufficienttools(self):
		return ( self.toolcount - self.damagedcount ) > self.minneeded

#MODEL tool instance by SN (for each specific tool)
class ToolSN (models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for tool")
	tool = models.ForeignKey(Tool,on_delete=models.CASCADE, verbose_name="tool no.")
	sn = models.CharField(max_length=10, verbose_name="tool SN")
	stationChoices = (
	    ('O','Obselete'),
	    ('C','Common'),
	    ('P','PNGS'),
	    ('D','DNGS'),
	)
	station = models.CharField(max_length=1, verbose_name="station", choices=stationChoices, default="D")
	location = models.ForeignKey(Location,on_delete=models.SET_NULL, verbose_name="location of the tool", null=True)
	pm = models.NullBooleanField(help_text="Is PM complete for this tool?", null=True)
	repair = models.BooleanField(help_text="Does this tool need to be repaired?", default=False)
	checkdate = models.DateTimeField(verbose_name="time when tool was checked", null="True", auto_now=True)
	comments = 	models.TextField(max_length=1000, help_text="Enter any comments for this tool as necessary.",blank=True)
	@property
	def is_invault(self):
		try:
		    if self.vaultlog_set.latest().action == "In":
			    return True
		    else:
			    return False
		except:
		    return False
	@property
	def is_borrowed(self):
		#Check if the most recent vaultlog hasn't been returned yet
		try:
			return not self.vaultlog_set.latest().isreturned
		except:
			return False
	@property
	def borrower(self):
		try:
			q = self.mostRecentBorrow()
			return q.borrower.username
		except:
			return "None"
	@property
	def needs_pm(self):
		return self.tool.pmneeded

	def mostRecentBorrow(self):
		#Return the most recent borrow log
		return self.borrowlog_set.filter(isreturned=0).latest()

	class Meta:
		ordering = ["tool","sn"] #order by tool number when returned in a query
		verbose_name = _("Tool SN")

	#string representing the model object
	def __str__(self):
		return "%s SN-%s" % (self.tool, self.sn) if self.sn is not '-' else "%s" % self.tool

class VaultLog(models.Model):
	vault_choices = (
		('in','In'),
		('out','Out')
	)
	toolsn = models.ForeignKey(ToolSN, on_delete=models.DO_NOTHING, verbose_name="loaned tool")
	action = models.CharField(verbose_name="action on the tool", choices=vault_choices, default='out', max_length=3)
	time = models.DateTimeField(verbose_name="log of when action was done", auto_now = True)
	class Meta:
		ordering = ('-time','id')
		verbose_name = ('Tool Vault Log')
		get_latest_by = ('time','id')


class BorrowLog(models.Model):
	toolsn = models.ForeignKey(ToolSN, on_delete=models.DO_NOTHING, verbose_name="loaned tool")
	borrower = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="tool loaned to", related_name="borrower_log")
	approvedby = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="who approved the borrow", related_name="manager_log", blank=True, null=True)
	borrowdate = models.DateField(verbose_name="time tool was checked out", auto_now_add=True)
	reason = models.TextField(verbose_name="why was tool taken out", null=True, blank=True)
	isreturned = models.BooleanField(verbose_name="is the tool returned?", default='0')
	notes = models.TextField(verbose_name="logging Notes", null=True, blank=True)
	time = models.DateTimeField(verbose_name="log of when action was done", auto_now = True)

	class Meta:
		ordering = ('-time','id')
		verbose_name = ('Tool Vault Log')
		get_latest_by = ('borrowdate','id')

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
