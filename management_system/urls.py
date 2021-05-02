from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from django.views.static import serve

from management_system import settings
from .views import error_404, admin_site
import management_system.admin

urlpatterns = [
    url(r'^$', admin_site, name="admin_site"),
    path('admin/', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^(?!media).*$', error_404, name="404")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
