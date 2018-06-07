from django.urls import include,path
from . import views

urlpatterns = [
	path('', views.index, name='index'), #Index

	#Tool paths
	path('tool/' , include([
	    path('', views.ToolListView.as_view(), name='tool'),
	    path('create/', views.ToolCreate.as_view(), name='tool-create'),
    	path('tool/<int:pk>/', include([
    	    path('', views.ToolDetailView.as_view(), name='tool-detail'),
    	    path('update/', views.ToolUpdate.as_view(), name='tool-update'),
    	    path('create/', views.create_toolsn, name='toolsn-create'),
    	])),
    ])),

	#Invetory Paths
	path('inventory/', include([
	    path('', views.ToolSNView.as_view(), name='toolsn'),
	    path('repair/', views.ToolSNRepairView.as_view(), name='toolsnrepair'),
	    path('pm/', views.ToolSNPMView.as_view(), name='toolsnpm'),
	    path('dup/', views.duplicateTools, name='toolsndup'),
	])),

	#ToolSN Views
	path('toolsn/<uuid:pk>/', include([
	    path('', views.ToolSNDetailView, name='toolsn-detail'),
	    path('update/', views.ToolSNUpdate.as_view(), name='toolsn-update'),
	    path('delete/', views.ToolSNDelete.as_view(), name='toolsn-delete'),
	    path('borrow/', views.borrow_tool, name='borrow-tool'),
	    path('<str:action>', views.ToolSNDetailView, name='toolsn-vault'),
    ])),

	#Location paths
	path('location/', include([
	    path('', views.LocationView.as_view(), name='location'),
	    path('create', views.LocationCreate.as_view(), name='location-create'),
	    path('<int:pk>/', include([
	        path('', views.LocationDetailView.as_view(), name='location-detail'),
	        path('update/', views.LocationUpdate.as_view(), name='location-update'),
	    ])),
	])),

	#Misc Paths
	path('borrowlog/', views.BorrowLogList.as_view(), name='borrowlog'),
	path('mytools/', views.BorrowedToolsByUserListView.as_view(), name='my-tools'),
	path('borrowedtools/', views.BorrowedToolsByAllListView.as_view(), name='borrowed-tools'),
	path('vaultlog/', views.VaultLogList.as_view(), name='vaultlog'),

]
