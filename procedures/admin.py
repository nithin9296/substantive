from django.contrib import admin
from .models import InternalControlTable, Member, Title, XMLGraph, Mxcell, Objectives, ICmatrix, Cycle, Test_of_Controls, sampling, samples, DatafileModel, testing_of_controls, Cycle_in_obj, Client, Client_Create, Deficiency, Report

# Register your models here.



admin.site.register(InternalControlTable)
admin.site.register(Member)
admin.site.register(Title)
admin.site.register(XMLGraph)
admin.site.register(Mxcell)
admin.site.register(Objectives)
admin.site.register(ICmatrix)
admin.site.register(Cycle)
admin.site.register(Test_of_Controls)
admin.site.register(sampling)
admin.site.register(samples)
admin.site.register(DatafileModel)
admin.site.register(testing_of_controls)
admin.site.register(Cycle_in_obj)
admin.site.register(Client)
admin.site.register(Client_Create)
admin.site.register(Deficiency)
admin.site.register(Report)

