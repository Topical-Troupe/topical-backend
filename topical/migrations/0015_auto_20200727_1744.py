# Generated by Django 3.0.8 on 2020-07-27 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topical', '0014_user_is_setup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_setup',
            field=models.BooleanField(),
        ),
    ]
