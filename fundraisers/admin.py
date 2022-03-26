from django.contrib import admin

from fundraisers.models import Category, Fundraiser, Transaction


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


class FundraiserAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Fundraiser, FundraiserAdmin)
admin.site.register(Transaction)
