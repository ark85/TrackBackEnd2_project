"""stackoverflow URL Configuration

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
from django.contrib import admin
from jsonrpc import jsonrpc_site
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^categories/', include(('categories.urls', 'categories'), namespace='categories')),
    url(r'^questions/', include(('questions.urls', 'questions'), namespace='questions')),
    url(r'^answers/', include(('answers.urls', 'answers'), namespace='answers')),

    url(r'', include(('core.urls', 'core'), namespace='core')),
    url('', include('social_django.urls', namespace='social'))
]

urlpatterns += staticfiles_urlpatterns()
