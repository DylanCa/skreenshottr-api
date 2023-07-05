from django.contrib import admin

from .models import User, Screenshot

admin.site.register([User, Screenshot])
