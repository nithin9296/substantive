#models.py


"""
Still to add foregn key for client, cycle here"""


class sampling(models.Model):
	control_procedures = models.ForeignKey(Test_of_Controls, on_delete=models.CASCADE)
	Estimated_Population_Exception_Rate = models.IntegerField()
	#EPER - Exception Rate that the auditor expects to find in the population 
	Tolerable_Exception_Rate = models.IntegerField() 
	#TPER - Exception Rate that the auditor will permit in the population and still be willing to conclude that -
	# - controls are operating effectively
	Population_Size = models.IntegerField()
	Suggested_Sample_Size = models.IntegerField()
	Actual_Sample_Size = models.IntegerField() #page-525
	Number_of_Exceptions = models.IntegerField()
	Sample_Exception_Rate = models.IntegerField()
	#Number of exceptions in sample divided by the sample size
	Computed_Upper_Exception_Rate = models.IntegerField()
	#The higest estimated exception rate in the population at a given ARACR


	def __str__(self):
		return str(self.control_procedures)

#url.py

url(r'^sample_size/$', views.sample_size, name='sample_size'),


#view.py
"""
Given Estimate population exception rate, Tolerable exception rate, population size, the function will suggest samples.
Still to include in the function where the form data is saved in sampling model against client and cycle
"""

def sample_size(request):

	control_proceduress = Test_of_Controls.objects.all()

	if request.method == 'POST':
		
		# formset = BaseSamplingDatasheetFormset(control_proceduress=control_proceduress, data=request.POST)
		formset = SamplingForm(data=request.POST)
	
		# print(formset)
		if formset.is_valid():
			print('HI')

			data = formset.cleaned_data.get("Estimated_Population_Exception_Rate")
			data1 = formset.cleaned_data.get("Tolerable_Exception_Rate")
			# data1 = form.cleaned_data.get("Actual_Sample_Size")
			# data1 = form.cleaned_data.get("Population_Size_0")
			print(data)
			print(data1)
			return redirect ('upload_sample')
			# new_object = ICmatrix.objects.create(mxcell_id=creator_id, option=s, objectives_id=obj_id)

		else:
			print(formset.errors)
			print(formset.non_form_errors())


	else:
		control_proceduress = Test_of_Controls.objects.all()
		formset = SamplingForm()
	

	context = { 'formset' : formset }

	return render(request, 'sampling.html', context)



def sugg_samples(request):
		#population_size, margin_error=.05, confidence_level=0.99, sigma=1/2

	"""
	Calculate the minimal sample size to use to achieve a certain margin of error
	and confidence level for a sample estimate of the population mean
	
	Inputs - 
	population_size: integer
		Total size of the population that the sample is to be drawn from.

	margin_error: number
		Maximum expected difference between the true population parameter,
		suvch as mean and sample estimate

	confidence_level: If we were to draw a large number of equal samples from the population,
	the true population parametere should lie within this percentage of the intervals (sample parameter -e, sample parameter + e)
	where e is the margin for error

	Confidence level tell you how sure you can be, It is expreseed as a percetange and represents how often 
	the true percentage of the population would pick an answer lies witihin the confidence interval.

	Estimated population exception rate can be same as that of confidence_level


	sigma: number
	The standard devisation of the population. For the case of estimating a parameter in the interval [0,1]
	sigma =1/2 should be sufficient

	"""
	if request.method == "GET":
		print(request.GET.get('Population_Size'))

	formset = SamplingForm(request.POST)
	# request.session['population_size_1'] = formset.data['Population_Size']
	# print('population_size_1')
	print(request.GET.get('Population_Size'))
	EPER = float(request.GET.get('Estimated_Population_Exception_Rate', '.50'))
	print(EPER)
	TER = float(request.GET.get('Tolerable_Exception_Rate', '2'))
	print(TER)
	population = request.GET.get('Population_Size')
	
	print(population)

	alpha = 1 - (EPER)
	sigma = 1/2

	zdict = {
		.90: 1.645,
		.91: 1.695,
		.99: 2.576,
		.97: 2.17,
		.94: 1.881,
		.93: 1.812,
		.95: 1.96,
		.98: 2.326,
		.96: 2.054,
		.92: 1.751
			}

	if EPER in zdict:
		z = zdict[EPER]
	else:
		from scipy.stats import norm
		z = norm.ppf(1 - (alpha/2))
		# print(z)

		N = TER
		M = TER
			
		numerator = float(z**2 * sigma**2 * (N / (N-1)))
		# print(numerator)
		denom = M**2 + ((z**2 * sigma**2)/ (N-1))
		# print(denom)

		sample_size = float(numerator/denom)
		# print(sample_size)


	return HttpResponse(sample_size)

#sampling.html

{% extends 'base.html' %}


{% load crispy_forms_tags %}

{% block content %}
 

<form id="a-good-form-name" method="POST">
    <!-- {{ formset.management_form }} -->
    <table class="table table-hover">
      {% csrf_token %}
<!--       <thead>
          <tr>
            <th> Description of Attributes</th>
            <th> EPER </th>
             <th> TER </th>
             <th> ARACR </th>
             <th> Suggested Sample Size </th>
             <th> Actual Sample Size </th>
        </tr>
        
</thead> -->

<form action="" method="post" enctype="multipart/form-data">
  {% csrf_token %}
    {{ formset.non_field_errors }}

        {{ formset.Estimated_Population_Exception_Rate.errors }}
       <b> {{ formset.Estimated_Population_Exception_Rate|as_crispy_field }}</b>
        {{ formset.Tolerable_Exception_Rate.errors }}
        {{ formset.Tolerable_Exception_Rate |as_crispy_field }}
        {{ formset.Suggested_Sample_Size.errors }}
        {{ formset.Suggested_Sample_Size|as_crispy_field }}
        {{ formset.Actual_Sample_Size.errors }}
        {{ formset.Actual_Sample_Size|as_crispy_field }}
        {{ formset.Population_Size.errors }}
        {{ formset.Population_Size|as_crispy_field }}

</form>

           

             
</tbody>
   
    {% if formset.errors %}
          {% for field in formset.forms %}
              {% for error in field.errors %}
                    <div class="alert alert-danger">
                    <strong>{{ error|escape }}</strong>
                    </div>
              {% endfor %}
            {% endfor %}
          {% for error in formset.non_field_errors %}
                    <div class="alert alert-danger">
                    <strong>{{ error|escape }}</strong>
                    </div>
        {% endfor %}
      {% endif %}

</table>
  <div class="form-actions">
 <input type="submit" />
 </div>
</form>

<div class='col-sm-6 col-sm-offset-3'>
{{ result}}



{% endblock content %}

{% block javascript %}
  <script>
    $("#id_Population_Size").change(function () {
      var sample_size = $(this).val();
      var AA = $('#id_Population_Size').val();
      var AB = $('#id_Tolerable_Exception_Rate').val();
      var AC = $('#id_Estimated_Population_Exception_Rate').val();
      console.log(AA);
      console.log(AB);
      console.log(AC);
      var Alpha = 1 - AC;
      var sigma = 0.5;
      

      // var result="";
      // console.log( $(this).val() );

      $.ajax({
        url: '{% url "sugg_samples" %}',
        type: "get",
        data: {
          'sample_size' : sample_size
        },
      
        success: function(data) {
          
          $("#id_Suggested_Sample_Size").replaceWith(data);
          // $("#form-1-Suggested_Sample_Size").replaceWith(data);
          // $("#form-2-Suggested_Sample_Size").replaceWith(data);
          // result = data;
          console.log(data);
        }
      });
    });
  </script>
{% endblock %}



