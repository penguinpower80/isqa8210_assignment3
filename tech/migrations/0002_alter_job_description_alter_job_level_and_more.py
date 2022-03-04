# Generated by Django 4.0.2 on 2022-03-03 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tech', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(help_text='Describe in detail what the problem is.'),
        ),
        migrations.AlterField(
            model_name='job',
            name='level',
            field=models.CharField(choices=[('L', 'Low'), ('N', 'Normal'), ('C', 'Critical')], default='N', help_text='How urgent do you think this problem is?', max_length=1),
        ),
        migrations.AlterField(
            model_name='job',
            name='technician',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobtechnician', to='tech.technician'),
        ),
    ]
