#models

"""
selects samples based on the population csv upload
"""

class samples(models.Model):


	control_procedures = models.ForeignKey(Test_of_Controls, on_delete=models.CASCADE)
	samples = models.FileField(null=True, blank=True)
	Actual_Sample_Size = models.ForeignKey(Test_of_Controls, related_name="Actual_Sample_Size", on_delete=models.CASCADE)

	Random = 'Random'
	Condition = 'Condition'
	Weights = 'Weights'

	Sampling_CHOICES = (
	(Random, 'Random'),
	(Condition, 'Condition'),
	(Weights, 'Weights'),
	)
	sampling_method = models.CharField(max_length=20, choices = Sampling_CHOICES)
	client_name = models.ForeignKey(Client, on_delete=models.CASCADE)
	cycle_type = models.ForeignKey(Cycle, on_delete=models.CASCADE)



	def __str__(self):
		return str(self.samples)

#Views.py

import os, pandas as pd
from django.core.files.storage import FileSystemStorage
import numpy as np


def upload_sample(request):
    if request.method == 'POST':
    	form = samples_form(request.POST, request.FILES)
    	if form.is_valid():
    		print('HI')
    		filehandle = pd.read_csv(request.FILES['file'])
    		sampling_mtd_selected = form.cleaned_data.get("sampling_method")
    		print(sampling_mtd_selected)

    		if sampling_mtd_selected == "Random":
    			IC_values = filehandle.sample(n=10)
    			print(IC_values)

    		# if sampling_mtd_selected == "Condition":
    		# 	Field_selected = form.cleaned_data.get("field_selected")
    		# 	field_selected_value = form.cleaned_data.get("field_selected_value")
    		# 	IC_values = filehandle[filehandle['Field_selected'] < ['field_selected_value']].sample(frac=.1).head()
    		# 	print(Field_selected)
    		# 	print(IC_values)


    		IC_values = filehandle.sample(n=10)
    		for row in IC_values.iterrows():
    			datafile = DatafileModel()
    			datafile.data = row
    			datafile.save()
    			# print(datafile.data)
    		object_list = DatafileModel.objects.all().first()
    		

    		context = {
    				"object_list": object_list,
    				"IC_values": IC_values
    		}
    		return render(request, 'table.html', context)
    		# data_set.head()

    	else:
    		print(form.errors)
    		# print(form.non_form_errors())

    else:
    	form = samples_form()


    return render(request, 'select_sample.html', {'form': form})

#url.py

url(r'^upload_sample/$', views.upload_sample, name='upload_sample'),

#select_Sample.html

{% extends 'base.html' %}

{% load static %}

{% load crispy_forms_tags %}

{% block content %}
{% load widget_tweaks %}
	




     <form id="sampling_method" method="POST" enctype="multipart/form-data">
     	{% csrf_token %}
     	<div class="modal-header">
     	
    	<h4 class="modal-title">Select the sampling method and Upload Population file</h4>
  		</div>
   <!--      {{ form.sampling_method }}
        {{ form.field_selected }}
        {{ form.field_selected_value }}
        {{ form.samples}} -->
        {% for field in form %}


  <div class="form-group{% if field.errors %} has-error{% endif %}">
    <label for="{{ field.id_for_label }}">{{ field.label }}</label>
    {% render_field field class="form-control" %}
    {% for error in field.errors %}
      <p class="help-block">{{ error }}</p>
    {% endfor %}
     </div>
{% endfor %}

<!-- 
	 <input type="file" class="btn btn-purple" name="file" >
                        &nbsp;&nbsp;
    <button name="upload_populations" id="upload_population" class="btn btn-purple btn-labeled fa dropzone" >Upload Population</button> -->
   <!--    <div class="form-actions">
 		<input type="submit" />
 		</div> -->
 	<div class="modal-footer">
 	<input type="file" class="modal-title" name="file" >
    <button type="submit" class="btn btn-primary">Select Samples</button>
  </div>

        </form>

 <!--  <form id = "sample-list" method="post" enctype="multipart/form-data">
    {% csrf_token %}
    
    <input type="file" class="btn btn-purple" name="file" >
                        &nbsp;&nbsp;
    <button name="upload_inventory" id="upload_inventory" class="btn btn-purple btn-labeled fa dropzone" >Upload Inventory</button> -->
   <!--  <button type="submit">Upload</button> -->
       {% if form.errors %}
          {% for field in form.forms %}
              {% for error in field.errors %}
                    <div class="alert alert-danger">
                    <strong>{{ error|escape }}</strong>
                    </div>
              {% endfor %}
            {% endfor %}
          {% for error in form.non_field_errors %}
                    <div class="alert alert-danger">
                    <strong>{{ error|escape }}</strong>
                    </div>
        {% endfor %}
      {% endif %}
  </form>

  


     





<head>

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>

    <script>
        $(document).ready(function (){
            $("#id_sampling_method").change(function() {
                // foo is the id of the other select box 
                if ($(this).val() == "Condition") {
                    $("#id_field_selected").show();
                    $("#id_field_selected_value").show();
                }else{
                    $("#id_field_selected").hide();
                    $("#id_field_selected_value").hide();
                } 
            });
            $(function() {
                // foo is the id of the other select box 
                if ($(this).val() == "Condition") {
                    $("#id_field_selected").show();
                    $("#id_field_selected_value").show();
                }else{
                    $("#id_field_selected").hide();
                    $("#id_field_selected_value").hide();
                } 
            });
        });
    </script>

</head>
{% endblock %}

