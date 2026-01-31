"""
Django settings for amarce project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-!b57e3$pnahmh!z^ckxcl1v59pdw&7wzbd7bz-0kb8a4f=s9y+')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Mantener True temporalmente para desarrollo

# ⚠️ IMPORTANTE: Esto permite TODOS los hosts - SOLO TEMPORAL
# Para que el cliente pueda verlo sin saber tu dominio de PythonAnywhere
ALLOWED_HOSTS = ['*']  # ⚠️ Solo para prueba temporal

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stock',
    'rest_framework',
    'corsheaders',
    'whitenoise.runserver_nostatic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'amarce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'amarce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Para PythonAnywhere - Usaremos SQLite para simplificar
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Para MySQL en PythonAnywhere (si necesitas más adelante):
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tuusuario$amarce',  # Reemplaza 'tuusuario'
        'USER': 'tuusuario',  # Reemplaza 'tuusuario'
        'PASSWORD': 'tu_password',  # La contraseña de la base de datos
        'HOST': 'tuusuario.mysql.pythonanywhere-services.com',  # Reemplaza
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
"""

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuración para PythonAnywhere
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# WhiteNoise para servir archivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS configuration - Permitir todos temporalmente
CORS_ALLOW_ALL_ORIGINS = True  # ⚠️ Solo temporal para pruebas

# También puedes especificar los orígenes permitidos:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5174",
    "http://localhost:5173",
    "http://localhost:8000",
    "https://*.pythonanywhere.com",  # Permite cualquier subdominio de PythonAnywhere
]

# Para aceptar cualquier origen durante desarrollo
CORS_ALLOW_CREDENTIALS = True

# CSRF settings - IMPORTANTE para `ALLOWED_HOSTS = ['*']`
CSRF_TRUSTED_ORIGINS = [
    'https://*.pythonanywhere.com',  # Acepta cualquier subdominio de PythonAnywhere
    'http://localhost:5174',
    'http://localhost:5173',
]

# Authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# ⚠️ ADVERTENCIA: Configuraciones de seguridad relajadas para pruebas
# Esto NO es seguro para producción a largo plazo

# Desactivar algunas protecciones para pruebas
# (Remover cuando pases a producción)
if DEBUG:
    # Permitir iframes (puede ser necesario para algunas integraciones)
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    
    # No forzar HTTPS en desarrollo
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    # Configuraciones para cuando DEBUG=False
    X_FRAME_OPTIONS = 'DENY'
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
