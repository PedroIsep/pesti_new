# Generated by Django 3.2.25 on 2024-06-13 21:55

from django.db import migrations
from django.contrib.auth import get_user_model

def create_default_user(apps, schema_editor):
    User = get_user_model()
    if not User.objects.filter(username='default_username').exists():
        User.objects.create_user(username='default_username', password='default_password')

class Migration(migrations.Migration):

    dependencies = [
        ('casnet', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_user),
    ]