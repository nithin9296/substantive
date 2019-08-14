from django import forms
from .models import Question, samples,Question1, ChoiceAnswer, BooleanAnswer, TextAnswer

from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class PostForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = [
			"question_text",
			"pub_date" ,
			"image"

		]



# class AuditorSignUpForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_auditor = True
#         if commit:
#             user.save()
#         return user


# class ClientSignUpForm(UserCreationForm):
# 	Client = forms.CharField(required=True)
# 	class Meta(UserCreationForm.Meta):
# 		model = User
# 		fields =["Client", 'username', 'password1', 'password2']

# 	@transaction.atomic
# 	def save(self, commit=True):	
# 		user = super().save(commit=False)
# 		user.is_client = True
# 		if commit:
# 			user.save()
# 		return user


class SamplesForm(forms.Form):
	samplesfile = forms.FileField(
        label = 'Upload samples as per the format' 
        )
	def __init__(self,*args,**kwargs):
		self.username=kwargs.pop('username',None)
		super(SamplesForm,self).__init__(*args,**kwargs)
		self.helper = FormHelper(self)
		self.helper.add_input(Submit('submit', 'Submit', css_class="btn-xs"))
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-sm-2'
		self.helper.field_class = 'col-sm-4'

	# class Meta:
	# 	model = samples
	# 	fields = ["username"]

	


class AuditorForm(forms.ModelForm):
	class Meta:
		model = samples
		fields = [
			"transaction_Gldescription",
			"transaction_GlCode",
			# "transaction_date",
			"transaction_number",
			"transaction_value",
			"remarks",
			"attachment",
			"action"
		]
		

class ClientForm(forms.ModelForm):
	class Meta:
		model = samples
		fields = [
			"remarks",
			"attachment"
		]
		
"""
Add a simple form, which includes the hidden payment nonce field.

You might want to add other fields like an address, quantity or
an amount.

"""
class ContactForm(forms.Form):

    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    # phone = forms.CharField(required=False)
    # website = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)


# class ContactForm(forms.Form):

#     name = forms.CharField(required=True)
#     email = forms.EmailField(required=True)
#     phone = forms.CharField(required=False)
    
#     message = forms.CharField(widget=forms.Textarea)


class ChoiceAnswerForm(forms.ModelForm):
    class Meta:
        model = ChoiceAnswer
        exclude=("question1",)

ChoiceAnswer.form = ChoiceAnswerForm




class BooleanAnswerForm(forms.ModelForm):
    class Meta:
        model = BooleanAnswer
        exclude=("question1",)
BooleanAnswer.form= BooleanAnswerForm

class TextAnswerForm(forms.ModelForm):
    class Meta:
        model = TextAnswer
        exclude=("question1",)
TextAnswer.form = TextAnswerForm


