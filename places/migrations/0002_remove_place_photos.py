# Generated by Django 4.0.1 on 2022-02-28 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='photos',
        ),
    ]
