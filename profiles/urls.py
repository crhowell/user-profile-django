from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'user/(?P<profile_slug>\w+)/$', views.show_profile, name='show'),
    url(r'me/$', views.my_profile, name='me'),
    url(r'create/$', views.create_profile, name='create'),
    url(r'edit/$', views.edit_profile, name='edit'),
]
