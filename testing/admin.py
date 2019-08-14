from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.

from testing.models import Question, samples, Membership, UserMembership, Subscription, Answer, Question1, ChoiceAnswer, TextAnswer, BooleanAnswer

# Register your models here.
# admin.site.register(Question)
admin.site.register(samples)
admin.site.register(Membership)
admin.site.register(UserMembership)
admin.site.register(Subscription)
admin.site.register(Answer)
admin.site.register(Question1)
admin.site.register(ChoiceAnswer)
admin.site.register(TextAnswer)
admin.site.register(BooleanAnswer)



# admin.site.register(Client)
# admin.site.register(Financial_Year)
# admin.site.register(Area)

@admin.register(Question)
class PersonAdmin(ImportExportModelAdmin):
    pass