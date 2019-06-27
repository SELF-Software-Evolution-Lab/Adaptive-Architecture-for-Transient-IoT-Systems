from django.conf.urls import url
from . import views


urlpatterns = [
            url(r'^$', views.index, name="index"),
            url(r'^post_service/$', views.post_service, name="post_service"),
]
