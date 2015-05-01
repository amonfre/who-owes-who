from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new', views.new_transaction, name='new'),
    url(r'^visualjson', views.visualize_json, name='vjson'),
    url(r'^visual', views.visual, name='visual'),
    url(r'^cvisualjson', views.cvisualize_json, name='cvjson'),
    url(r'^cvisual', views.cvisual, name='cvisual'),
    url(r'^transactions', views.transactions, name='transactions'),
    url(r'^respond', views.respond, name='respond'),
    url(r'^friends', views.friends, name='friends'),
    url(r'^processfriendship', views.processfriendship, name='processfriendship'),
    url(r'^cancelfriendrequest', views.cancelfriendrequest, name='cancelfriendrequest'),
    url(r'^canceltransactionrequest', views.canceltransactionrequest, name='canceltransactionrequest'),
    url(r'^createSampleTransactions', views.createSampleTransactions, name='createSampleTransactions'),

    url(r'^profile', views.profile, name='profile')

]


