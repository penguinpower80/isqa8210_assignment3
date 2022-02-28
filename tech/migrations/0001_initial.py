# Generated by Django 4.0.2 on 2022-02-28 13:20

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=25)),
                ('street1', models.CharField(max_length=80)),
                ('street2', models.CharField(blank=True, max_length=80, null=True)),
                ('city', models.CharField(max_length=80)),
                ('state', models.CharField(max_length=2)),
                ('zip', models.CharField(max_length=15)),
                ('comments', models.TextField(blank=True, null=True)),
                ('type', models.TextField(choices=[('C', 'Customer'), ('T', 'Technician'), ('S', 'Staff')], default='T', max_length=10)),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('first_name', models.CharField(max_length=25, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=25, verbose_name='Last Name')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('N', 'New'), ('O', 'Open'), ('X', 'Cancelled'), ('H', 'Hold'), ('W', 'Waiting'), ('C', 'Complete')], default='N', max_length=1)),
                ('level', models.CharField(choices=[('L', 'Low'), ('N', 'Normal'), ('C', 'Critical')], default='N', max_length=1)),
                ('description', models.TextField(help_text='Describe what the problem is.')),
                ('appointment', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobcustomer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('cost', models.FloatField(verbose_name='Cost $')),
                ('status', models.CharField(choices=[('X', 'Unknown'), ('W', 'At the warehouse'), ('U', 'Not Available'), ('D', 'Discontinued'), ('O', 'Ordered')], default='X', max_length=1)),
                ('leadtime', models.SmallIntegerField(blank=True, null=True, verbose_name='Lead Time (In days)')),
            ],
        ),
        migrations.CreateModel(
            name='PayRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=25)),
                ('payrate', models.FloatField()),
            ],
            options={
                'verbose_name': 'Pay Rate',
                'verbose_name_plural': 'Pay Rates',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WorkingDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='JobPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Pending'), ('D', 'Dispatched'), ('T', 'With the Technician'), ('O', 'Ordered'), ('I', 'Installed'), ('C', 'Cancelled')], default='P', max_length=1)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tech.job')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tech.part')),
            ],
        ),
        migrations.CreateModel(
            name='Technician',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Related System User')),
                ('days', models.ManyToManyField(blank=True, to='tech.WorkingDay', verbose_name='Working Days')),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tech.payrate', verbose_name='Experience Level')),
                ('skills', models.ManyToManyField(blank=True, to='tech.Skill', verbose_name='Technician Skills')),
            ],
            options={
                'verbose_name': 'Extra Tech Info',
                'verbose_name_plural': 'Extra Tech Info',
            },
        ),
        migrations.CreateModel(
            name='JobTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tech.job')),
                ('technician', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tech.technician')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='technician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobtechnician', to='tech.technician'),
        ),
    ]
