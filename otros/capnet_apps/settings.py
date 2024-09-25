import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-+_@giy9qwn1*a+d)d2*=qv5)8y-@2cuf__4l0vao(!((j@h$s("

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_drf_filepond",
    "django_q",
    "crispy_forms",
    "mathfilters",
    "rest_framework",
    "webpush",
    "pwa",
    "capnet_api",
    "seguimientolite_mazda_col",
    "tracker_pro_mazda_col",
    "citas_mazda_col_pro",
    "citas_mazda_col",
    
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "capnet_apps.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "capnet_apps.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "es-CO"

TIME_ZONE = "America/Bogota"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DJANGO_DRF_FILEPOND_FILE_STORE_PATH = os.path.join(BASE_DIR, "media")

DJANGO_DRF_FILEPOND_UPLOAD_TMP = os.path.join(BASE_DIR, "media", "temp")

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

CRISPY_TEMPLATE_PACK = "bootstrap4"

Q_CLUSTER = {  # Configuracion de django_q
    "timeout": 60,
    "sync": True,
    "redis": {
        "host": "localhost",
        "port": 6379,
        "db": 0,
    },
}

REST_FRAMEWORK = {  # Directiva de Seguridad de DRF
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ]
}

WEBPUSH_SETTINGS = {  # Configuracion de WebPush
    "VAPID_PUBLIC_KEY": "BK1dqUjiUGeX19M3-U0g6KxzU9wURYqZ_hI_93gOJg-tW9dvwylr8L0Gu_hmkYY-rnwIFnL2Dkrg9EpHpG3ZcuQ",
    "VAPID_PRIVATE_KEY": "7MzFSOuM3cQPBt8SWOgL2bkSgxxsVXFSmxyw-U4HeOo",
    "VAPID_ADMIN_EMAIL": "gamaliel.gutierrez@capnet.com.mx",
}

# Configuracion de Capnet Apps

DATABASES = {
    "default": {
        "ENGINE": "mssql",  # No se modifica
        "HOST": "201.150.44.27",  # Nombre de la instancia de SQL Server
        "NAME": "capnet_apps_nissan_demo",  # Nombre de la base de datos
        "USER": "sa",  # Usuario
        "PASSWORD": ".5capnet",  # Contraseña
    }
}

COREAPI = ""  # URL completa de API de WhatsApp

AGENCIA = "Capital Network"  # Nombre de la agencia

LOGO = ""  # URL completa del logo de la agencia

DOMINIO = "201.150.44.27"  # Direccion publica del servidor

PUERTO = "3101"  # Puerto publico de este proyecto

TELEFONO = ""  # Telefono de la agencia

AVISO_PRIVACIDAD = "https://www.nissan.com.co/privacidad.html"  # Link de aviso de privacidad/terminos y condiciones

TABLERO_DB = "Tablerov4_Nissan_Colombia_demo"  # Nombre de la base de datos de tablero

CURRENCY_SYMBOL = "$"

CURRENCY = "COP"

CITAS_TABLEROAPI = "http://201.150.44.27:8996"  # IP y puerto de la API de tablero

CITAS_CORREOS_INTERNOS = ["angiecastaneda.capnet@gmail.com"]  # Lista de correos internos a notificar cuando se agenda una cita

SEGUIMIENTOLITE_CORREOS_ASESORES = ["angiecastaneda.capnet@gmail.com"]  # Lista de correos internos a notificar en la fase de asesor

SEGUIMIENTOLITE_CORREOS_MANO_DE_OBRA = ["angiecastaneda.capnet@gmail.com"]  # Lista de correos internos a notificar en la fase de mano de obra

SEGUIMIENTOLITE_CORREOS_REFACCIONES = ["angiecastaneda.capnet@gmail.com"]  # Lista de correos internos a notificar en la fase de refacciones

SEGUIMIENTOLITE_IVA = 1.19  # IVA Para las operaciones del seguimiento en linea

SEGUIMIENTOLITE_PRECIO_UT = 140000  # Precio de la unidad de tiempo

TRACKER_PRO_DOCUMENTOS_DIGITALES = {  # Lista de documentos digitales para el tracker pro
    "Orden de Servicio": "http://201.150.44.27:8995/api/documentacion/getDocumentoPdf/folio/{{id_hd}}/origen/2.pdf",
    "Evidencia Fotográfica": "http://201.150.44.27:8995/ri/galeria/folio/{{id_hd}}",
}

# Correo
EMAIL_HOST = "smtp.gmail.com"  # Direccion del servidor de correo

EMAIL_PORT = 587  # Puerto

EMAIL_USE_SSL = False # Usar SSL

EMAIL_USE_TLS =  True  # Usar TLS

EMAIL_HOST_USER = "angiecastaneda.capnet@gmail.com"  # Direccion de correo

EMAIL_HOST_PASSWORD = "vtzewobzslheyfkm"  # Contraseña

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LOGOUT_REDIRECT_URL="staff_login"
