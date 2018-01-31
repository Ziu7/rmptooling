from django.conf.urls import url
from . import views

urlpatterns = [
	#Standard List Views
	url(r'^$', views.index, name='index'), #function based view
	url(r'^tool/$' , views.ToolListView.as_view(), name='tool'),
	url(r'^inventory/$' , views.ToolSNView.as_view(), name='toolsn'),
	url(r'^inventory/repair$' , views.ToolSNRepairView.as_view(), name='toolsnrepair'),
	url(r'^inventory/pm$' , views.ToolSNPMView.as_view(), name='toolsnpm'),
	url(r'^location/$', views.LocationView.as_view(), name='location'),
	url(r'^vaultlog/$', views.VaultLogList.as_view(), name='vaultlog'),

	#Tool detailed view, including ToolSN instances
	url(r'^tool/(?P<pk>\d+)$', views.ToolDetailView.as_view(), name='tool-detail'),

	#Location detailed view, including ToolSN instances
	url(r'^location/(?P<pk>\d+)$', views.LocationDetailView.as_view(), name='location-detail'),

	#ToolSN detailed view
	url(r'^toolsn/(?P<pk>[-\w]+)$', views.ToolSNDetailView.as_view(), name='toolsn-detail'),

	#Loaned tools views
	url(r'^mytools/$', views.LoanedToolsByUserListView.as_view(), name='my-tools'),
	url(r'^loanedtools/$', views.LoanedToolsByAllListView.as_view(), name='loaned-tools'),
	url(r'^tool/(?P<pk>[-\w]+)/renew/$', views.renew_tool, name='renew-tool'), #function based view

	#ToolSN forms (Create, Update, Delete)
	url(r'^toolsn/(?P<pk>\d+)/create$', views.ToolSNCreate.as_view(), name='toolsn-create'),
	url(r'^toolsn/(?P<pk>[-\w]+)/update$', views.ToolSNUpdate.as_view(), name='toolsn-update'),
	url(r'^toolsn/(?P<pk>[-\w]+)/delete$', views.ToolSNDelete.as_view(), name='toolsn-delete'),

	#Tool forms (Create)
	url(r'^tool/create$', views.ToolCreate.as_view(), name='tool-create'),

	#Tool Checkout Forms
	url(r'^vaultlog/(?P<pk>[-\w]+)/(?P<action>[-\w]+)$', views.VaultUpdate.as_view(), name='vault-update'),

	#Location forms (Create, Update)
	url(r'^location/create$', views.LocationCreate.as_view(), name='location-create'),

	url(r'^location/new$', views.add_location, name='add-location'),

	url(r'^location/(?P<pk>\d+)/update$', views.LocationUpdate.as_view(), name='location-update'),
]
