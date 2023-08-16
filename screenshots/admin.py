from django.contrib import admin

from screenshots.models import User
from screenshots.models.screenshot import Screenshot
from screenshots.models.tag import Tag

admin.site.register([User, Screenshot, Tag])
