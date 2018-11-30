from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.

from testing.models import Question, samples, Membership, UserMembership, Subscription

# Register your models here.
# admin.site.register(Question)
admin.site.register(samples)
admin.site.register(Membership)
admin.site.register(UserMembership)
admin.site.register(Subscription)

# admin.site.register(Client)
# admin.site.register(Financial_Year)
# admin.site.register(Area)

@admin.register(Question)
class PersonAdmin(ImportExportModelAdmin):
    pass