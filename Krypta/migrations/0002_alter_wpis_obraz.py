# Generated by Django 3.2.7 on 2021-09-17 19:37

import Krypta.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Krypta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wpis',
            name='obraz',
            field=models.ImageField(upload_to=Krypta.models.filepath),
        ),
    ]
