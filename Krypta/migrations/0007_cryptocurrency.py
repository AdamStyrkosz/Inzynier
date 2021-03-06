# Generated by Django 3.2.7 on 2021-10-13 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Krypta', '0006_auto_20210929_1921'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cryptocurrency',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('description', models.TextField(max_length=2000)),
                ('website', models.URLField()),
                ('whitepaper', models.URLField()),
                ('connected_news', models.ManyToManyField(to='Krypta.Wpis')),
            ],
        ),
    ]
