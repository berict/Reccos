from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
    url(r'', include('market.urls', namespace='market')),
    # url(r'^admin/', include(admin.site.urls)),
    path('admin/', admin.site.urls),
]