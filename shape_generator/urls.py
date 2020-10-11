from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^signup', SignupViews.as_view(), name='signup'),
    url('^login', LoginViews.as_view(), name='login'),
    url('^shape', ShapeViews.as_view(), name='shape'),
]
