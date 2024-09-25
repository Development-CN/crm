from django.urls import path
from .views import *


urlpatterns = [
    path("login/", TrackerProLogin.as_view(), name="tracker_pro_login"),
    path("cliente/", TrackerProView.as_view(), name="tracker_pro"),
    path("cliente/<str:no_orden>/", TrackerProLoginlessView.as_view(), name="tracker_pro_loginless"),
    path("entrevista/", EntrevistaProfesionalView.as_view(), name="tracker_pro_entrevista"),
    path("api/citas/", TrackerProAPI.as_view(), name="tracker_pro_api"),
    path("api/informacion_vin/", TrackerProEstados.as_view(), name="tracker_pro_api_estados"),
    path("logout/", TrackerProLogout.as_view(), name="tracker_pro_logout"),
]
