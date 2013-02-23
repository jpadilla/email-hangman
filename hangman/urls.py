from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'hangman.core.views.index', name='home'),
    url(r'^webhook/$', 'hangman.core.views.webhook', name='webhook'),
    # url(r'^hangman/', include('hangman.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
