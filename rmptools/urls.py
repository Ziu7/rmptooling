"""rmptools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView
import nexus

#admin site header and title
admin.site.site_header = 'RMP Tooling Administration'
admin.site.site_title = 'RMP Tooling Administration'

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/catalog', permanent=True)),
    url(r'^rmpadministration/', admin.site.urls),
    url(r'^catalog/', include('catalog.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url('^nexus/', include(nexus.site.urls)),
]

#use static() to add url mapping to serve static files during development (only)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns