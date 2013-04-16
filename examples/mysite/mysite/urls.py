from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


## extdirectrpc
from extdirectrpc.views import extdirect_rpc_urls
urlpatterns += extdirect_rpc_urls()
##

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

urlpatterns += (
    url(r'^', direct_to_template, {'template': 'base.html'}),
)
