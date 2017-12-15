from django.conf.urls import url
from . import views

app_name = 'market'

urlpatterns = [
    url(r'^$',views.main,name="main"),
    url(r'^new$', views.item_new, name='item_new'),
    url(r'^item/(?P<pk>\d+)/$',views.item_detail,name="item_detail"),
    url(r'^item/(?P<pk>\d+)/edit$',views.item_edit,name="item_edit"),
    url(r'404',views.render_404,name="render_404"),
]
