# Generated by Django 3.2.7 on 2021-11-29 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Krypta', '0009_cryptocurrencyexchangemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocurrencyexchangemodel',
            name='count',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
