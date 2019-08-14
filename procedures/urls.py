from django.conf.urls import url, include
from procedures import views





urlpatterns = [
   
    url(r'^internal_control_procedures/$', views.internal_control_procedures.as_view(), name='internal_control_procedures'),
    url(r'^saveData/$', views.saveData, name='saveData'),
    url(r'^openfile/$', views.openfile, name='openfile'),
    # url(r'^savefile/$', views.savefile, name='savefile'),
    url(r'^open/$', views.open, name='open'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^transaction_objective_update/$', views.transaction_objective_update, name='transaction_objective_update'),
    url(r'^sample_view/$', views.sample_view, name='sample_view'),
    url(r'^xml_to_table/$', views.xml_to_table, name='xml_to_table'),
    url(r'^update_pressure/$', views.update_pressure, name='update_pressure'),
    url(r'^CycleCreate/$', views.CycleCreate.as_view(), name='CycleCreate'),
    url(r'^ClientCreate/$', views.ClientCreate, name='ClientCreate'),
    url(r'^CycleTransactionCreate/$', views.CycleTransactionCreate.as_view(), name='CycleTransactionCreate'),
    url(r'^CycleUpdate/<init:pk>/$', views.CycleUpdate.as_view(), name='cycle_update'),
    url(r'^CycleDelete/<init:pk>/$', views.CycleDelete.as_view(), name='cycle_delete'),
    url(r'^sample_size/$', views.sample_size, name='sample_size'),
    url(r'^audit_report/$', views.audit_report, name='audit_report'),
    url(r'^sugg_samples/$', views.sugg_samples, name='sugg_samples'),
    url(r'^upload_sample/$', views.upload_sample, name='upload_sample'),
    url(r'^CycleTransactionGet/$', views.CycleTransactionGet, name='CycleTransactionGet'),
    url(r'^deficiency/$', views.deficiency, name='deficiency'),
    url(r'^report_form/$', views.report_form, name='report_form'),
    # url(r'^TOC_detail/$', views.TOC_detail, name='TOC_detail'),
    url(r'^(?P<id>\d+)/$', views.TOC_detail, name='TOC_detail'),
    url(r'^(?P<id>\d+)/edit/$', views.TOC_update, name='TOC_update'),
    url(r'^grapheditor/$', views.grapheditor, name='grapheditor'),
    url(r'^loadgraph/$', views.loadgraph, name="loadgraph"),
    url(r'^savegraph/$', views.savegraph, name='savegraph'),
    url(r'^blog/$', views.blog, name='blog'),
    url(r'^contact/$', views.contact, name='contact'),

    ]