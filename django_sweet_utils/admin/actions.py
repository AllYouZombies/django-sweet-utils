from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.action(description=_('Delete selected %(verbose_name_plural)s (hard)'))
def hard_delete_selected(modeladmin, request, queryset):
    queryset.hard_delete()
