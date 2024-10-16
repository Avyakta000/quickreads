# grappelli
# settings.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _("My Blog Admin")
admin.site.site_title = _("My Blog Admin Portal")
admin.site.index_title = _("Welcome to My Blog Admin")
