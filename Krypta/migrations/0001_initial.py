# Generated by Django 3.2.7 on 2021-09-17 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wpis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tytul', models.CharField(max_length=50)),
                ('zawartosc', models.CharField(max_length=250)),
                ('obraz', models.ImageField(upload_to='')),
                ('data_utworzenia', models.DateTimeField()),
            ],
        ),
    ]