
models.py

class Client(models.Model):
	client_name = models.CharField(max_length=20)
	def __str__(self):
		return self.client_name



class Cycle(models.Model):
	cycle_type = models.CharField(default='sales', max_length=15)
	client_name = models.ForeignKey(Client, on_delete=models.CASCADE)
	# def __str__(self):
	# 	return str(self.cycle_name)
	def __str__(self):
		return str(self.cycle_type)


class Cycle_in_obj(models.Model):
	cycle_type = models.ForeignKey(Cycle, on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	client_name = models.ForeignKey(Client, on_delete=models.CASCADE)
	
	def __str__(self):
		return str(self.cycle_type)



class Objectives(models.Model): #Build

	medium = 'Med'
	low = 'Low'
	high = 'High'

	Med_High_CHOICES = (
	(medium, 'Med'),
	(low, 'Low'),
	(high, 'High'),
	)

	cycle = models.ForeignKey(Cycle_in_obj, related_name="has_objectives",on_delete=models.CASCADE)
	transaction_objective = models.CharField(max_length=100)
	assessed_cr = models.CharField(max_length=20, choices = Med_High_CHOICES)


Views.py


class CycleTransactionCreate(CreateView):
	model = Cycle_in_obj
	fields = ['cycle_type', 'client_name']
	template_name = 'cycle_form.html'
	# form_class = CycleForm
	success_url = reverse_lazy('saveData')
	# queryset = Objectives.objects.all()

	def get_context_data(self, **kwargs):
		data = super(CycleTransactionCreate, self).get_context_data(**kwargs)
		if self.request.POST:
			data['titles'] = ObjectivesFormSet(self.request.POST)
		
		else:
			data['titles'] = ObjectivesFormSet()
		return data
		

	def form_valid(self, form):
		print('HI')
		context = self.get_context_data()
		titles = context['titles']
		with transaction.atomic():
			form.instance.user = self.request.user
			self.object = form.save()


			if titles.is_valid():
				titles.instance.user = self.request.user
				titles.instance = self.object
				titles.save()

			# for title in titles:
					# print(title.prefix)
				# print(titles)
		return super(CycleTransactionCreate, self).form_valid(form)



forms.py

class ObjectivesForm(forms.ModelForm):
	
	class Meta:
		model = Objectives
		exclude = ('assessed_cr',)

	def __init__(self, *args, **kwargs):
		super(ObjectivesForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
		self.fields['transaction_objective'].widget.attrs['style'] = "width:850px"
		# self.fields['transaction_objective'].required = False
		# for i in range(2):
		# 	self.fields['assessed_cr_%d' % i] = forms.ChoiceField(choices = Med_High_CHOICES, required=False)
		# self.fields['cycle'].required = False
		# self.fields['assessed_cr'].required = False
      		


objective_query = Objectives.objects.all()
ObjectivesFormSet = inlineformset_factory(Cycle_in_obj, Objectives, form=ObjectivesForm,
	extra=1, can_delete=True, )



cycleform.html

<h2>Create Transaction Objectives</h2>
    <hr>
    <div class="col-md-4">

        <form action="" method="post">{% csrf_token %}
            
            {{ form.as_p }}
            
            <table class="table">
                {{ titles.management_form }}
                {% for form in titles.forms %}
                <tr class="{% cycle row1 row2 %} formset_row">
                {% for field in form.visible_fields %}
                <td>       {# Include the hidden fields in the form #}
                            {% if forloop.first %}
                            {% for hidden in form.hidden_fields %}
                                        {{ hidden }}
                                    {% endfor %}
                                {% endif %}
                                {{ field.errors.as_ul }}
                                {{ field }}
                            </td>
                        {% endfor %}
                    </tr>
                {% endfor %}
                
            </table>
            <input type="submit" value="Save"/> 
        </form>
    </div>


    <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
    < <script src="{% static 'js/jquery.formset.js' %}"></script>
    <script type="text/javascript">
        $('.formset_row').formset({
            addText: 'add objectives',
            deleteText: 'remove',
            prefix: 'has_objectives',
    
        });
    </script>

  <script>
    $("#id_cycle_type").change(function () {
      var objectives_trans = $(this).val();


      $.ajax({
        url: '{% url "CycleTransactionGet" %}',
        type: "get",
        data: {
          'objectives_trans' : objectives_trans
        },
      
        success: function(data, status) {
            // var items = data['objectives_trans']
            //  $.each(items, function(key, value) {
            //             console.log(value.objectives_trans);
            $("#id_has_objectives-0-transaction_objective").replaceWith(data);

          
          // $("#id_has_objectives-1-transaction_objective").replaceWith(data);
          // $("#form-1-Suggested_Sample_Size").replaceWith(data);
          // $("#form-2-Suggested_Sample_Size").replaceWith(data);
          // result = data;
          console.log(data);
        }
      });
    });
  </script>

	

	def __str__(self):
		return self.transaction_objective






