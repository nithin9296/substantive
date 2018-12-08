from django.conf.urls import url, include
from testing import views
from testing.sitemaps import samplesSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'samples': samplesSitemap
}
urlpatterns = [
    # url(r'^$', views.ca_import, name='uplink'),
    # url(r'^posts$', views.post_list, name='posts'),
    url(r'^$', views.home, name='home'),
    url(r'^search/$', views.search, name='search'),
    url(r'^sitemap\.xml/$', sitemap, {'sitemaps': sitemaps } , name='sitemap'),
    url(r'^survey/', include('survey.urls')),
    
    url(r'^question_list/', views.question_list, name='question_list'),
    url(r'^helpusgrow/', views.helpusgrow, name='helpusgrow'),
    url(r'^challenge/', views.challenge, name='challenge'),
    url(r'^client_list/', views.client_list, name='client_list'),
    # url(r'^create$', views.post_create, name='create'),
    # url(r'^posts/(?P<id>\d+)/$', views.post_detail, name='detail'),
    # url(r'^posts/(?P<id>\d+)/$', views.question_detail, name='question_detail'),
    # url(r'^(?P<id>\d+)/edit/$', views.post_update, name='update'),
    url(r'^(?P<id>\d+)/update/$', views.samples_update, name='samples_update'),
    url(r'^(?P<id>\d+)/edit/$', views.client_update, name='client_update'),
    # url(r'^(?P<id>\d+)/update/$', views.question_update, name='question_update'),
    # url(r'^(?P<id>\d+)/review/$', views.question_review, name='question_review'),
    url(r'^import_data/', views.import_data, name="import_data"),
    # url(r'^survey/', views.survey, name="survey"),
    url(r'^downloadreport/', views.downloadreport, name="downloadreport"),
    url(r'^download/', views.download, name="download"),
    # url(r'^checkout/', views.CheckoutView.as_view(), name="checkoutview"),
    url(r'^stripe/', include('djstripe.urls', namespace="djstripe")),
    url(r'^email/$', views.email, name="email"),
     url(r'^thanks/$', views.thanks, name="thanks"),
     # url(r'^checkout/', views.checkout, name="checkout"),
     url(r'^select/', views.MembershipSelectView.as_view(), name="select"),
     url(r'^payment/', views.PaymentView, name="payment"),
     url(r'^update-transactions/(?P<subscription_id>\w+)/$', views.updateTransactionRecords, name="update-transactions"),
      url(r'^profile/', views.profile_view, name="profile"),
      url(r'^cancel/', views.cancelSubscription, name="cancel"),
    # url(r'^download/', views.download, name="download"),
    # url(r'^export/(.*)', views.export_data, name="export"),
    # url(r'^handson_view/', views.handson_table, name="handson_view"),

   
]