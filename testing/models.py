from django.db import models

# Create your models here.
from django.conf import settings

from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
from datetime import datetime


class Question(models.Model):
    Approve = 1
    Reject = 2
    Options = (
        (Approve, 'Approve'),
        (Reject, 'Reject'),
        )
    question_text = models.CharField(max_length=200)
    image = models.FileField(null=True, blank=True)
    pub_date = models.DateTimeField('date published')
    slug = models.CharField(max_length=10,
                            default="question")

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
    	return reverse("question_update", kwargs={"id": self.id})
    	# return "posts/%s/" %(self.id)



# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

#     def __str__(self):
#         return self.choice_text
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
import stripe

# class User(AbstractUser):
#     is_client = models.BooleanField(default=False)
#     is_auditor = models.BooleanField(default=False)

    

# class Client(AbstractUser):
#     is_client = models.BooleanField(default=False)
#     Client_name = models.CharField(max_length=20, null=True)

#     def __str__(self):
#         return self.Client_name

Option_CHOICES = (
    ('approve','APPROVE'),
    ('reject', 'REJECT'),

)


# class Client(models.Model):
#     Client = models.CharField(max_length=20,verbose_name='client')
#     User = models.OneToOneField(User,on_delete=models.CASCADE)

#     def create_client_profile(sender, instance, created, **kwargs):
#         if created:
#             Profile.objects.create(user=instance)
#             signals.post_save.connect(create_client_profile, sender=User)

#     def __str__(self):
#         return self.Client

# Year_Choices = (
#     ('2018', '2018'),
#         ('2019', '2019'),
#     )

# class Financial_Year(models.Model):
#     Financial_Year = models.CharField(max_length=4,choices=Year_Choices, default='2018')
#     Client = models.ForeignKey('client', on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.Financial_Year

# class Area(models.Model):
#     Area = models.CharField(max_length=15,verbose_name='area')
#     Financial_Year = models.ForeignKey(Financial_Year, on_delete=models.CASCADE)
#     Client= models.ForeignKey('client', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.Area


MEMBERSHIP_CHOICES = (
    ('Professional', 'pro'),
    ('Free', 'free'),
)



class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, default='Free',  max_length=30)
    price = models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type

class UserMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
    

def post_save_usermembership_create(sender, instance, created, *args, **kwargs):
    if created:
        UserMembership.objects.get_or_create(user=instance)

        user_membership, created = UserMembership.objects.get_or_create(user=instance)

        if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
            new_customer_id = stripe.Customer.create(email=instance.email)
            user_membership.stripe_customer_id = new_customer_id['id']
            user_membership.save()

post_save.connect(post_save_usermembership_create, sender=settings.AUTH_USER_MODEL)


class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username

    @property
    def get_created_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.created)
    
    @property
    def get_next_billing_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.current_period_end)
    


class samples(models.Model):
    
    transaction_Gldescription = models.CharField(max_length=30)
    transaction_GlCode = models.CharField(max_length=15)
    transaction_date = models.DateTimeField(auto_now=True)
    transaction_number = models.IntegerField(default=0)
    transaction_value = models.IntegerField(default=0)
    remarks = models.TextField(null=True)
    attachment = models.FileField(null=True, blank=True)
    action = models.CharField(max_length=8, choices=Option_CHOICES, default="approve")
    Area = models.CharField(max_length=20)
    Financial_Year = models.IntegerField(default=2018)
    Client = models.CharField(max_length=20)
    # Area =  models.ForeignKey('area', on_delete=models.CASCADE)
    # Financial_Year = models.ForeignKey(Financial_Year, on_delete=models.CASCADE)
    # Client = models.ForeignKey('client', on_delete=models.CASCADE)
    # username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    allowed_memberships = models.ManyToManyField(Membership)

    def __str__(self):
        return self.transaction_Gldescription

    def get_absolute_url(self):
        return reverse("client_update", kwargs={"id": self.id})


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .signals import object_viewed_signal


class ObjectViewed(models.Model):
    # User = models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    ip_address = models.CharField(max_length=120, blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self, ):
        return "%s viewed: %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'

def object_viewed_recevier(sender, instance, request, *args, **kwargs):
    c_type = ContentType.get_for_model(sender)
    ip_adress = None
    try:
        ip_adress = get_client_ip(request)
    except:
        pass
    new_view_instance = ObjectViewed.objects.create(
                user=request.user,
                content_type=c_type,
                object_id=instance.id,
                ip_address=ip_address
                )
object_viewed_signal.connect(object_viewed_recevier)


class DataSetManager(models.Manager):
    def create_new(self, qs, fields=None):
        df  = convert_to_dataframe(qs, fields=fields)
        fp = StringIO()
        fp.write(df.to_csv())
        date = timezone.now().strftime("%m-%d-%y")
        model_name = slugify(qs.model.__name__)
        filename = "{}-{}.csv".format(model_name, date)
        obj = self.model(
            name = filename.replace('.csv', ''),
                app = slugify(qs.model._meta.app_label),
                model = qs.model.__name__,
                lables = fields,
                object_count = qs.count()
            )
        obj.save()
        obj.csvfile.save(filename, File(fp)) #saves file to the file field
        return obj

class DatasetModel(models.Model):
    name                = models.CharField(max_length=120)
    app                 = models.CharField(max_length=120, null=True, blank=True)
    model               = models.CharField(max_length=120, null=True, blank=True)
    lables              = models.TextField(null=True, blank=True)
    object_count        = models.IntegerField(default=0)
    csvfile             = models.FileField(upload_to='datasets/', null=True, blank=True)
    timestamp           = models.DateTimeField(auto_now_add=True)



CHOICES=((1,'exactly true'),(2,'mostly true'),(3,'mostly untrue'),(4,'untrue'),(5,'I don\'t know '))

class Answer(models.Model):
    question1 = models.ForeignKey("Question1", on_delete=models.CASCADE)
    

class ChoiceAnswer(Answer):
    answer = models.IntegerField(max_length=1, choices=CHOICES)
    
    def __unicode__(self):
        return u'%s: %s'%(self.question1, self.answer)

class TextAnswer(Answer):
    answer= models.TextField()


    def __unicode__(self):
        return u'%s: %s'%(self.question1, self.answer)


class BooleanAnswer(Answer):
    answer= models.BooleanField(choices=((True,'yes'),(False,'no')))

    def __unicode__(self):
        return u'%s: %s'%(self.question1, self.answer)


class Question1(models.Model):
    question1 = models.CharField(max_length=255)
    answer_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)


    def __unicode__(self):
        return u'%s'%self.question