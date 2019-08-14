models.py

"""
THis is more like a quiz application where for each samplke selected, an auditor has to enter remarks, 
click if deficient and upload attachement"""


class DatafileModel(models.Model):

    data = PickledObjectField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    class Meta:
        ordering = ["updated", "pk" ]

    def __str__(self):
    	return str(self.data)




class testing_of_controls(models.Model):
	Option_CHOICES = (
    ('defecient','defecient'),
)
	data = models.ForeignKey(DatafileModel, on_delete=models.CASCADE)
	remarks = models.TextField(null=True)
	attachment = models.FileField(null=True, blank=True)
	defecient = models.CharField(max_length=8, choices=Option_CHOICES)



	def __str__(self):
		return str(self.data)

urls.py

 url(r'^(?P<id>\d+)/edit/$', views.TOC_update, name='TOC_update'),

views.py


def TOC_update(request, id=None):
	instance = get_object_or_404(DatafileModel, id=id)

	form = TOC_Form(request.POST or None, instance=instance)
	# the_next = instance.get_next_by_timestamp()
	newest = DatafileModel.objects.all().first()
	the_next = next_in_order(newest)


	if form.is_valid():
		print("HI")
		# form.save()

		# data_id = DatafileModel.objects.get(data=instance).id
		defecient_selected = form.cleaned_data.get("defecient")
		remarks_selected = form.cleaned_data.get("remarks")
		new_object = testing_of_controls.objects.create(defecient=defecient_selected, remarks=remarks_selected, data_id=id)



	else:
		print(form.errors)
		# print(form.non_form_errors())


	context = {
    				
    			"instance": instance,
    			"form": form,
    			"the_next" : the_next,
 
    	}

	return render(request, 'sample_form.html', context)


sample_form.html

{% extends 'base.html' %}

{% load crispy_forms_tags %}


{% block content %}


<table>

 <thead>
    <tr>
      <th>{{instance.data }} </td>
    </tr>
  </thead>

</table>


<tbody>
    

<form action="" method="post" enctype="multipart/form-data">
	{% csrf_token %}
    {{ form.non_field_errors }}

        {{ form.defecient.errors }}
       <b> {{ form.defecient|as_crispy_field }}</b>
        {{ form.attachment.errors }}
        {{ form.attachment|as_crispy_field }}
        {{ form.remarks.errors }}
        {{ form.remarks|as_crispy_field }}

     <input type="submit" value="Save">
         
</form>

             
</tbody>


<div class="modal-footer">

    <button type="submit" class="btn btn-primary"><li><a href="/procedures/{{ the_next.id }}/edit/">Next Sample</a></li></button>
    <button type="submit" class="btn btn-primary"><li><a href="/procedures/{{ prev_in_order.id }}/edit/">Previous Sample</a></li></button>
    
  </div>




<!-- {{the_next}}
 -->



<!-- {% with next=instance.get_next_by_data %}
    {% if next %}
        <a href="{% url 'TOC_update' id=obj.id %}">next</a>
    {% endif %}
{% endwith %} -->

<!-- {% if the_next %}
<a href="{% url 'TOC_update' the_next.id %}">Next</a>
{% else %}
This is the last film!
{% endif %} -->

{% endblock %}



