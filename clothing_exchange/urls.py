from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('items.urls', namespace='items')),
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns

    # Раздача медиафайлов в режиме разработки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
