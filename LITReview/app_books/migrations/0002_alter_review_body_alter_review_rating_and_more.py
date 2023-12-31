# Generated by Django 4.2.4 on 2023-08-29 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
        ),
        migrations.AlterField(
            model_name='review',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_books.ticket'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='ticket_images/'),
        ),
    ]
