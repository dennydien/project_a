# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 07:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import homepage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True, verbose_name='username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('follows', models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL, verbose_name='user follows')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', homepage.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='name')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='address')),
                ('info', models.TextField(blank=True, verbose_name='info')),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100, verbose_name='address')),
                ('start_date', models.DateTimeField(blank=True, verbose_name='start date')),
                ('end_date', models.DateTimeField(blank=True, verbose_name='end date')),
            ],
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, verbose_name='name')),
                ('from_address', models.CharField(blank=True, max_length=100, verbose_name='address')),
                ('to_address', models.CharField(blank=True, max_length=100, verbose_name='address')),
                ('start_date', models.DateTimeField(blank=True, verbose_name='start date')),
                ('end_date', models.DateTimeField(blank=True, verbose_name='end date')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Untitled Trip', max_length=30, verbose_name='name')),
                ('status', models.CharField(choices=[('I', 'In Progress'), ('U', 'Upcoming'), ('C', 'Completed')], default='U', max_length=1, verbose_name='status')),
                ('start_date', models.DateTimeField(blank=True, verbose_name='start date')),
                ('end_date', models.DateTimeField(blank=True, verbose_name='end date')),
                ('stops', models.ManyToManyField(to='homepage.Stop', verbose_name='stops on trip')),
                ('transports', models.ManyToManyField(to='homepage.Transport', verbose_name='transport on trip')),
            ],
        ),
        migrations.AddField(
            model_name='place',
            name='stop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.Stop', verbose_name='related stop'),
        ),
        migrations.AddField(
            model_name='user',
            name='trips',
            field=models.ManyToManyField(to='homepage.Trip', verbose_name="user's trips"),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
