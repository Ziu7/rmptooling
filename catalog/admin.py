from django.contrib import admin
from .models import Discipline, Location, Tool, ToolSN
from import_export.admin import ImportExportModelAdmin#import and export module for admin site

#admin.site.register(Discipline)
@admin.register(Discipline)
class DisciplineAdmin(ImportExportModelAdmin):
	model = Discipline
	list_display = ('id','name')

#admin.site.register(Location)
@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin):
	model = Location
	list_display = ('id','name')

#inline addition/ editing of ToolSN in add Tool page
class ToolSNInline(admin.TabularInline):
	model = ToolSN

#admin.site.register(Tool)
@admin.register(Tool)
class ToolAdmin (ImportExportModelAdmin):
	list_display = ('num','name','minneeded','dcatid','pcatid','primdisc','secdisc','draw')
	fields = [('num','name'),('minneeded','draw'),('dcatid','pcatid'),('primdisc','secdisc'),'notes']
	list_filter = ('primdisc','secdisc')
	#This creates an error with saving data in the admin backend. Remove for now.
	#inlines = [ToolSNInline]

#admin.site.register(ToolSN)
#class ToolSNAdmin(admin.ModelAdmin):
@admin.register(ToolSN)
class ToolSNAdmin(ImportExportModelAdmin):
	model = ToolSN

	#get 'primdisc' field from model Tool
	def get_primdisc(self, obj):
		return obj.tool.primdisc

	get_primdisc.admin_order_field = 'tool'
	get_primdisc.short_description = "Primary Discipline"

	#get 'secdisc' field from model Tool
	def get_secdisc(self, obj):
		return obj.tool.secdisc

	get_secdisc.admin_order_field = 'tool'
	get_secdisc.short_description = "Secondary Discipline"

	#get 'name' field from model Tool
	def get_toolname(self, obj):
		return obj.tool

	get_toolname.admin_order_field = 'tool'
	get_toolname.short_description = "Tool Name"

	list_display = ('tool','sn','get_toolname','location','pm','repair','checkdate','get_primdisc','get_secdisc')
	fields = [('tool','sn'),'location','vault',('pm','repair'),'comments']
	list_filter = ('location','pm','repair')


