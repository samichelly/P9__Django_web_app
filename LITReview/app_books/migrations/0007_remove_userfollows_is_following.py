# Generated by Django 4.2.4 on 2023-09-06 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_books', '0006_userfollows_is_following_alter_review_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfollows',
            name='is_following',
        ),
    ]