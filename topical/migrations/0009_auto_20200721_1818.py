# Generated by Django 3.0.8 on 2020-07-21 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topical', '0008_auto_20200719_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='upc',
            field=models.CharField(max_length=14, null=True, unique=True),
        ),
    ]
