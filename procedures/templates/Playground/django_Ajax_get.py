#base.html

<html>
	<head>
	<meta charset="utf-8"
	<script src="https://code.jquery.com/jquery-3.1.0min.js"></script>
	{% block Javascript %} {% endblock %}
</html>

The jquery library and all the javascript resources stays in the end of html for 2 reasons
 - To guarantee the DOM will be loaded when the script is executed and to avoid inline scripts
  - All the extra or specific javascript goes inside the {% block javascript %} {% endblock %}

 Sample Scenario - 

  - Let's say you want to validate the username field in a sign up view, as soon as the user'
  	finish typing the desired username.
   - YOu want to simple check, if the username is already taken or not

 Views.py

 from django.contrib.auth.forms import UserCreationForm
 from django.views.generic.edit import CreateView

 class SignUpView(CreateView):
    template_name = 'core/signup.html'
    form_class = UserCreationForm

urls.py

from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
]

signup.html

{% extends 'base.html' %}

{% block javascript %}
<script>
	$("#id_username").change(function() {
		console.log( $(this).val() );
		});
	</script>
	{% endblock %}



{% block content %}
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Sign up</button>
  </form>
{% endblock %}


Ajax request


















