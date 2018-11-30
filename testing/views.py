from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
import re
import xlrd
from .forms import PostForm, AuditorSignUpForm, ClientSignUpForm, SamplesForm, ClientForm, AuditorForm, ContactForm
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView)
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.db import transaction
from django.contrib import messages
from django.urls import reverse

# Create your views here.


from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
# from _compact import JsonResponse
from django import forms
from import_export import resources
import django_excel as excel
from testing.models import Question, samples, User, ObjectViewed, Membership, UserMembership, Subscription
from .decorators import client_required, auditor_required

data = [
    [1, 2, 3],
    [4, 5, 6]
]


def profile_view(request):

    user_membership = get_user_membership(request)
    print(user_membership)
    user_subscription = get_user_subscription(request)
    print(user_subscription)

    context = {
        'user_membership' : user_membership,
        'user_subscription' : user_subscription

    }

    return render(request, "testing/profile.html", context)

class SignUpView(CreateView):
    model = User
    form_class = AuditorSignUpForm
    template_name = 'signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'auditor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('select')



def home(request):
    if request.user.is_authenticated:
        if request.user.is_auditor:
            return redirect('question_list')
        else:
            return redirect('client_list')
    return render(request, 'home.html')




class ClientSignUpView(CreateView):
    model = User
    form_class = ClientSignUpForm
    template_name = 'client_profile.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('client_list')


class AuditorSignUpView(CreateView):
    model = User
    form_class = AuditorSignUpForm
    template_name = 'signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'auditor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('select')


@auditor_required
def import_data(request):
    
    if request.method == "POST":
        form = SamplesForm(request.POST,request.FILES)

        def choice_func(row):
            this_username=request.user
            row[9] = this_username
            return row

        if form.is_valid():
            data = form.cleaned_data

            # with transaction.atomic():
            #     try:
            request.FILES['samplesfile'].save_book_to_database(
            models=[samples],
                        initializers=[choice_func],
                        mapdicts=['transaction_Gldescription', 'transaction_GlCode', 'transaction_date', 'transaction_number', 'transaction_value', 'remarks', 'Area', 'Financial_Year', 'Client', 'username'])
            return redirect('question_list')
                # except:
                #     transaction.rollback()
                #     return HttpResponse("Error")

        else:
            print (form.errors)
            return HttpResponseBadRequest()
    else:
        form = SamplesForm(username=request.user)
    return render(
        request,
        'upload_form.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data as per the format'
        })



# def question_update(request, id=None):
# 	instance = get_object_or_404(Question, id=id)
# 	form = PostForm(request.POST or None,  request.FILES or None, instance=instance)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.save()
# 		return redirect('question')
# 	context = {

# 		"title": "instance.question_text",
# 		"instance": instance,
# 		"form": form
# 	}
# 	return render(request, "post_form.html", context)





# def question_review(request, id=None):
#     instance = get_object_or_404(Question, id=id)
#     form = PostForm(request.POST or None,  request.FILES or None, instance=instance)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.save()
#         return redirect('question')
#     context = {

#         "title": "instance.question_text",
#         "instance": instance,
#         "form": form
#     }
#     return render(request, "post_form.html", context)

# def post_create(request):
# 	form = PostForm(request.POST, request.FILES or None)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.save()
# 		return HttpResponseRedirect(instance.get_absolute_url())
# 	context = {
# 		"form": form,

# 	}


# 	return render(request, "post_form.html", context)

# def question_detail(request, id):
#     instance = get_object_or_404(samples, id=id)
    
#     context = {

# 		"title": "Detail",
# 		"instance": instance


# 	}
#     return render(request, "post_detail.html", context)


# def post_detail(request, id):
# 	instance = get_object_or_404(Question, id=id)
# 	context = {

# 		"title": "Detail",
# 		"instance": instance

# 	}
# 	return render(request, "post_detail.html", context)



def question_list(request):
    # queryset = samples.objects.filter(User=request.user)  
    queryset = samples.objects.filter(username=request.user)
    object_list = SampleFilter(request.GET, queryset=queryset)
    context = {
		"filter": object_list,
		"samples": list
	}
    return render(request, "post_list.html", context)



def client_list(request):
    User = get_user_model()
    queryset = samples.objects.filter(Client=request.user)
    print(queryset)
    # clientname = get_user_model(username=username)
    # print (clientname)
    # queryset = samples.objects.filter(Client=clientname)
    # queryset = samples.objects.all()
    object_list = SampleFilter(request.GET, queryset=queryset)
    context = {
        # "object_list": queryset,
        "samples": list,
        "filter": object_list
    }
    return render(request, "client_list.html", context)
    
def client_update(request, id=None):
    instance = get_object_or_404(samples, id=id)
    form = ClientForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('client_list')

    context = {

        "instance": instance,
        "form": form,

    }
    return render(request, "post_form.html", context)

# def client_update(request, id=None):
#     instance = get_object_or_404(samples, id=id)
#     if request.method == 'POST':
#         form = ClientForm(request.POST or None,  request.FILES or None, instance=instance)
#     else:
#         form = ClientForm(instance=instance)
#     return client_save_book_form(request, form, 'includes/client_partial_samples_update.html')
    

    



def samples_update(request, id=None):
    instance = get_object_or_404(samples, id=id)
    if request.method == 'POST':
        form = AuditorForm(request.POST or None,  request.FILES or None, instance=instance)
    else:
        form = AuditorForm(instance=instance)
    return save_book_form(request, form, 'includes/partial_samples_update.html')
    
    # context = {

    #     "title": "instance.transaction_number",
    #     "instance": instance,
    #     "form": form
    # }
    # return render(request, "includes/partial_samples_update.html", context)

from django.http import JsonResponse

def client_save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            samples_list = samples.objects.all()
            samples_filter = SampleFilter(request.GET, queryset=samples_list)

            data['html_object_list'] = render_to_string('includes/client_partial_samples_list.html', {
                'filter': samples_filter
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


 
def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            samples_list = samples.objects.all()
            samples_filter = SampleFilter(request.GET, queryset=samples_list)
            data['html_object_list'] = render_to_string('includes/partial_samples_list.html', {
                'filter': samples_filter
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)



from django.contrib.auth.models import User
from django.shortcuts import render
from .filters import SampleFilter
from django.contrib.auth import get_user_model
try:
    from io import BytesIO as IO
except ImportError:
    from StringIO import StringIO as IO
import pandas as pd
import xlsxwriter
import datetime as dt

def search(request):
    # User = get_user_model()
    samples_list = samples.objects.all()
    samples_filter = SampleFilter(request.GET, queryset=samples_list)
    return render(request, 'samples_search.html', {'filter': samples_filter})



from .utils import convert_to_dataframe

from .utils import get_lookup_fields, qs_to_dataset


def qs_to_local_csv(qs, fields=None, path=None, filename=None):
    if path is None:
        path = os.path.join(os.path.dirname(BASE_DIR), 'csvstorage')

        if not os.path.exists(path):
            os.mkdir(path)

    if filename is None:
        model_name = slugify(qs.model.__name__)
        file_name = "{}.csv".format(model_name)
    filepath = os.path.join(path, filename)
    lookups = get_lookup_fields(qs.model, fields=fields)
    dataset = qs_to_dataset(qs, fields)
    row_done = 0
    with open(filepath, 'w') as my_file:
        writer = csv.DictWriter(my_file, filenames=lookups)
        writer.writeheader()
        for data_item in dataset:
            writer.writerow(data_item)
            rows_done += 1
    print("{} rows completed".format(rows_done))

class Echo:
    def write (self, value):
        return value




def downloadreport(request):
    samples_list = samples.objects.all()
    samples_filter = SampleFilter(request.GET, queryset=samples_list)

    df1 = convert_to_dataframe(samples_list, fields=['transaction_GlCode', 'transaction_date', 'transaction_number', 'transaction_value',
            'remarks', 'action', 'Area', 'Financial_Year', 'Client'])
    frames = [df1]
    result = pd.concat(frames)
    excel_file = IO()

    xlwriter = pd.ExcelWriter(excel_file, engine='openpyxl')
    result.to_excel(xlwriter, 'sheetname')
    xlwriter.save()
    xlwriter.close()
    excel_file.seek(0)
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['content-Disposition'] = 'attachment; filename=myfile.xlsx'
    return response


from django.http import HttpResponse
from wsgiref.util import FileWrapper
from .utils import convert_to_dataframe2


import os
from django.conf import settings


def download(request):
    samples_list = samples.objects.none()
    df1 = convert_to_dataframe2(samples_list,fields=['transaction_GlCode', 'transaction_date', 'transaction_number', 'transaction_value',
            'remarks', 'action', 'Area', 'Financial_Year', 'Client'])
    frames = [df1]
    result = pd.concat(frames)
    excel_file = IO()

    xlwriter = pd.ExcelWriter(excel_file, engine='openpyxl')
    result.to_excel(xlwriter, 'sheetname')
    xlwriter.save()
    xlwriter.close()
    excel_file.seek(0)
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['content-Disposition'] = 'attachment; filename=sample_format.xlsx'
    return response

    # file_path = os.path.join(settings.MEDIA_ROOT, path)
    # if os.path.exists(file_path):
    #     with open(file_path, 'rb') as fh:
    #         response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
    #         response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
    #         return response
    # raise Http404

    # filename = "samples.xlsx"
    # with open(filename, 'rb') as f:
    #     response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
    #     response['Content-Disposition'] = 'attachment; filename=' + filename
    #     response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-16'
    #     return response





# class CSVDownloadView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         qs = ObjectViewed.objects.all()
#         model_name = slugify(qs.model.__name__)
#         filename = "{}.csv".format(model_name)
#         fp = StringIO()
#         pseudo_buffer = Echo()
#         outcsv = csv.writer(pseudo_buffer)
#         writer = csv.DictWriter(my_file, fieldnames=lookups)
#         writer.writeheader()
#         for data_item in dataset:
#             writer.writerow(data_item)
#         stream_file = file(fp)
#         response = StreamingHttpResponse(stream_file,
#                                         content_type ="text/csv")
#         response['content-Disposition'] = 'attachment; filename="{}"'.format(filename)
#         return response


# def post_update(request, id=None):
#   instance = get_object_or_404(Question, id=id)
#   form = PostForm(request.POST or None,  request.FILES or None, instance=instance)
#   if form.is_valid():
#       instance = form.save(commit=False)
#       instance.save()
#       return HttpResponseRedirect(instance.get_absolute_url())
#   context = {

#       "title": "instance.question_text",
#       "instance": instance,
#       "form": form
#   }
#   return render(request, "post_form.html", context)


# def post_list(request):
#   queryset = Question.objects.all()
#   context = {
#       "object_list": queryset,
#       "Question": list
#   }
#   return render(request, "base.html", context)



# class UploadFileForm(forms.Form):
#     file = forms.FileField()

"""
Adds simple form view, which communicates with Braintree.

There are four steps to finally process a transaction:

1. Create a client token (views.py)
2. Send it to Braintree (js)
3. Receive a payment nonce from Braintree (js)
4. Send transaction details and payment nonce to Braintree (views.py)

"""
from django.core.mail import send_mail, BadHeaderError

def email(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail(name, message, from_email, ['shrotaapp@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('home')
    return render(request, "email.html", {'form': form})

def thanks(request):
    return HttpResponse('Thank you for your message.')


import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# def checkout(request):
#     publishKey = settings.STRIPE_TEST_PUBLIC_KEY
#     if request.method == "POST":
#         token = request.POST.get('stripeToken', False)
#         if token:
#             try:
#                 charge = stripe.Charge.create(
#                     amount=20,
#                     interval = 'month',
#                     currency='usd',
#                     description='PRO Plan',
#                     trial_period_days=30,
#                     source=token,
#                 )

#                 return redirect(reverse('home',
#                         kwargs={
#                             'token': token
#                         })
#                     )
#             except stripe.CardError as e:
#                 message.info(request, "Your card has been declined.")
       
            
#     context = {
       
        
#         'STRIPE_PUBLISHABLE_KEY': publishKey
#     }

#     return render(request, 'checkout.html', context)

def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None

def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None

        
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None


def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
                    membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None


class MembershipSelectView(ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context

    def post(self, request, **kwargs):
        selected_membership_type = request.POST.get('membership_type')
        
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)

        selected_membership_qs = Membership.objects.filter(
                membership_type=selected_membership_type
            )
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()


        '''
        Validation

        '''

        if user_membership.membership == selected_membership:
            if user_subscription != None:
                messages.info(request, "You already have this membership. YOur next payment \
                    is due {}".format('get this value from stripe'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        #assign to the session
        request.session['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('payment'))

def PaymentView(request):

    user_membership = get_user_membership(request)

    selected_membership = get_selected_membership(request)

    publishKey = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == "POST":
        try:
            token = request.POST['stripeToken']
            subscription = stripe.Subscription.create(
              customer=user_membership.stripe_customer_id,
              items=[
                {
                  "plan": selected_membership.stripe_plan_id,
                },
              ],
              source=token # 4242424242424242
            )

            return redirect(reverse('update-transactions',
                kwargs={
                    'subscription_id': subscription.id
                }))

        except stripe.error.CardError as e:
            messages.info(request, "Your card has been declined")

    context = {
        'publishKey': publishKey,
        'selected_membership': selected_membership
    }

    return render(request, "testing/membership_payment.html", context)

# def PaymentView(request):

#     user_membership = get_user_membership(request)

#     selected_membership = get_selected_membership(request)

#     publishKey = settings.STRIPE_PUBLISHABLE_KEY

#     if request.method == "POST":
#             try:
#                 token = request.POST['stripeToken']
#                 subscription = stripe.Subscription.create(
#                 customer=user_membership.stripe_customer_id,
#                 items=[
#                     {
#                     "plan": selected_membership.stripe_plan_id,
#                     },
#                 ],
#                 source=token # 4242424242424242
#                 )

#                 return redirect(reverse('update_transactions',
#                     kwargs={
#                         'subscription_id':subscription.id
#                     }))

#             except stripe.CardError as e:
#                 messages.info(request, "Your card has been declined")




#     context = {
#         'publishKey': publishKey,
#         'selected_membership': selected_membership

#     }
#     return render(request, "testing/membership_payment.html", context)


# def update_transactions(request, subscription_id):

#     user_membership = get_user_membership(request)
#     selected_membership = get_selected_membership(request)

#     user_membership.membership = selected_membership
#     user_membership.save()

#     sub, created = Subscription.objects.get_or_create(user_membership=user_membership)

#     sub.stripe_subscription_id = subscription_id
#     sub.active = True
#     sub.save()

#     try:
#         del request.session['selected_membership_type']
#     except:
#         pass

#     messages.info(request, "Sucessfully created {} emebership".format(selected_membership))

#     return redirect('/question_list')


def updateTransactionRecords(request, subscription_id):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)

    user_membership.membership = selected_membership
    user_membership.save()

    sub, created = Subscription.objects.get_or_create(user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    try:
        del request.session['selected_membership_type']
    except:
        pass

    messages.info(request, 'Successfully created {} membership'.format(selected_membership))
    return redirect('client_list')


def cancelSubscription(request):

    user_sub = get_user_subscription(request)

    if user_sub.active == False:
        messages.info(request, "You dont have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
    sub.delete()

    user_sub.active = False
    user_sub.save()


    free_membership = Membership.objects.filter(membership_type='Free').first()
    user_membership = get_user_membership(request)
    user_membership.membership = free_membership
    user_membership.save()

    messages.info(request, "Successfully cancelled membership.")
    # sending an email here

    return redirect('/testing')



