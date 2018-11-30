from django.contrib.auth.models import User
from .models import Question, samples, User
import django_filters

class SampleFilter(django_filters.FilterSet):
	
	# Client_name = django_filters.ModelChoiceFilter(queryset=samples.objects.order_by('Client_name'))
	# Area = django_filters.ModelChoiceFilter(queryset=samples.objects.order_by('Area__Area'))
	# Financial_Year = django_filters.ModelChoiceFilter(queryset=samples.objects.order_by('Financial_Year__Financial_Year'))
	# # transaction_GlCode = django_filters.NumberFilter(lookup_expr='icontains')
	# transaction_Gldescription = django_filters.CharFilter(lookup_expr='icontains')
	# transaction_date = 
	# transaction_number = django_filters.NumberFilter(lookup_expr='icontains')
	# remarks = django_filters.CharFilter(lookup_expr='icontains')
	# action = django_filters.CharFilter(lookup_expr='icontains')

	class Meta:
		model = samples
		fields = [
		'Client',
		'Area',
		'Financial_Year',
    	'transaction_GlCode',
    	"transaction_Gldescription",
    	"transaction_date",
    	"transaction_number",
    	"transaction_value",
    	"remarks",
    	"action" ]
 