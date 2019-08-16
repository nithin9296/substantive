# Generated by Django 2.0.8 on 2019-08-09 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0010_auto_20190801_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='samples',
            name='client_name',
        ),
        migrations.RemoveField(
            model_name='samples',
            name='control_procedures',
        ),
        migrations.RemoveField(
            model_name='samples',
            name='cycle_type',
        ),
        migrations.AddField(
            model_name='test_of_controls',
            name='cycle_in_obj',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procedures.Cycle_in_obj'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cycle_in_obj',
            name='year',
            field=models.IntegerField(choices=[(2019, 2019), (2020, 2020)], null=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datafilemodel',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procedures.Client'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datafilemodel',
            name='cycle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procedures.Cycle'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='deficiency',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procedures.Client'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='deficiency',
            name='datafile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procedures.DatafileModel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='samples',
            name='sampling_method',
            field=models.CharField(choices=[('Random', 'Random')], max_length=20),
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
        migrations.AlterField(
            model_name='sampling',
            name='Suggested_Sample_Size',
            field=models.IntegerField(null=True,),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testing_of_controls',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procedures.Client'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testing_of_controls',
            name='cycle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procedures.Cycle'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testing_of_controls',
            name='deficient',
            field=models.CharField(choices=[('deficient', 'deficient')], default='s', max_length=8),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='xmlgraph',
            name='cycle_in_obj',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procedures.Cycle_in_obj'),
            preserve_default=False,
        ),
    ]