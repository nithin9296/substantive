# Generated by Django 2.0.8 on 2019-07-11 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0002_auto_20190622_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deficiency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('remarks', models.TextField(null=True)),
                ('financials', models.TextField(null=True)),
                ('suggestions', models.TextField(null=True)),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procedures.Cycle')),
            ],
        ),
        migrations.AlterField(
            model_name='sampling',
            name='Client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procedures.Client'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sampling',
            name='Cycle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procedures.Cycle'),
            preserve_default=False,
        ),
    ]