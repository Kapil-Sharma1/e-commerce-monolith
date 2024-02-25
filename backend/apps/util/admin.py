from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ['uid']
    ordering = ['-id']

