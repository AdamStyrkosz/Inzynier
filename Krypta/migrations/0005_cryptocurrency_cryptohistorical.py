# Generated by Django 3.2.7 on 2021-09-26 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Krypta', '0004_alter_wpis_zawartosc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cryptocurrency',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('short_name', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='CryptoHistorical',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('datetime', models.DateTimeField()),
                ('cryptocurrency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Krypta.cryptocurrency')),
            ],
        ),
    ]
