from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout
from .views import (
	        home, 
	        add_camp, 
	        camp_list, 
	        camp_detail,
	        post_review,
	        login_view, 
	        signup)


urlpatterns = [
    url(r'^$', home, name='camp_home'),
    url(r'^list/$', camp_list, name='camp_list'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout, {'next_page': 'login'} ,name='logout'),
    url(r'^(?P<slug>[\w-]+)/$', camp_detail, name='camp_detail'),
    url(r'^post-review/(?P<slug>[\w-]+)/$', post_review, name='post_review'),
]