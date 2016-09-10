from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'profile/(?P<user_pk>\d+)/$', views.profile_show, name='profile'),
    url(r'profile/change_password/$', views.change_password, name='change_password'),
    url(r'profile/edit/$', views.profile_edit, name='profile_edit'),
    url(r'sign_in/$', views.sign_in, name='sign_in'),
    url(r'sign_up/$', views.sign_up, name='sign_up'),
    url(r'sign_out/$', views.sign_out, name='sign_out'),
]
