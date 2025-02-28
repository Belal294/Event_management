from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.conf import settings
from core.views import home, no_permission

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')), 
    path('users/', include('users.urls')),
    path('',home,name="home"),
    path('no-permission/', no_permission, name='no-permission')

]+ debug_toolbar_urls()


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])   
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
