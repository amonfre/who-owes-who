from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new', views.new_transaction, name='new'),
    url(r'^visualjson', views.visualize_json, name='vjson'),
    url(r'^visual', views.visual, name='visual'),
]

