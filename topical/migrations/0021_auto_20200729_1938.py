# Generated by Django 3.0.8 on 2020-07-29 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topical', '0020_ingredienttagdict_ingredienttagentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredienttagentry',
            name='matches',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='ingredienttagentry',
            name='total',
            field=models.IntegerField(default=-1),
        ),
    ]
