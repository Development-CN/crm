from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("pwa.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("capnet_api.urls")),
    path("citas/", include("citas_mazda_col.urls")),
    path("citas_pro/", include("citas_mazda_col_pro.urls")),
    path("seguimiento/", include("seguimientolite_mazda_col.urls")),
    path("tracker/", include("tracker_pro_mazda_col.urls")),
    path("fp/", include("django_drf_filepond.urls")),
    path("webpush/", include("webpush.urls")),
    
]

admin.site.site_header = settings.AGENCIA
admin.site.site_title = settings.AGENCIA
admin.site.index_title = ""
