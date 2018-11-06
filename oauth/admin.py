from django.contrib import admin
from oauth.models import Oauth


@admin.register(Oauth)
class SeminarInline(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
