# Generated by Django 3.2.7 on 2022-01-08 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Krypta', '0019_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='wpis',
            name='type',
            field=models.CharField(choices=[('NEWS', 'NEWS'), ('EDUCATION', 'EDUCATION')], default='NEWS', max_length=16),
            preserve_default=False,
        ),
    ]
