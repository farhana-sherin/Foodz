
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("web.urls",namespace='web')),
    path('manager/',include("manager.urls",namespace='manager')),
    path('store_owner/',include("store_owner.urls",namespace='store_owner')),
    path('api/v1/customer/',include("api.v1.customer.urls")),

]


if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )

