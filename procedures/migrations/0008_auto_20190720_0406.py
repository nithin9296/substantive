# Generated by Django 2.0.8 on 2019-07-20 04:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0007_auto_20190719_0816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testing_of_controls',
            name='defecient',
        ),
        migrations.AddField(
            model_name='testing_of_controls',
            name='deficient',
            field=models.CharField(choices=[('deficient', 'deficient')], null=True, max_length=8),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='deficiency',
            name='datafile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procedures.DatafileModel'),
            preserve_default=False,
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
            field=models.IntegerField(null=True),
            preserve_default=False,
        ),
    ]
