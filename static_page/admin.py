from django.contrib import admin

from static_page.models import StaticPage


class StaticPageAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


admin.site.register(StaticPage, StaticPageAdmin)
