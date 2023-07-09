from django.contrib import admin

from .models import User, Screenshot, Tag

admin.site.register([User, Screenshot, Tag])
