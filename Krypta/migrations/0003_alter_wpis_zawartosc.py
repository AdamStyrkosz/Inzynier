# Generated by Django 3.2.7 on 2021-09-18 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Krypta', '0002_alter_wpis_obraz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wpis',
            name='zawartosc',
            field=models.TextField(max_length=250),
        ),
    ]
