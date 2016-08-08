from django.conf.urls import patterns, url
from views import *

urlpatterns = [
    url(r'^topnews/', display_news),
    url(r'^search/', search_article)
]
