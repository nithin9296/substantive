# Generated by Django 2.0.8 on 2018-11-28 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0004_auto_20181128_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='membership_type',
            field=models.CharField(choices=[('Professional', 'pro'), ('Free', 'free')], default='Free', max_length=30),
        ),
    ]
