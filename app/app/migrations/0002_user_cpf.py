# Generated by Django 4.2.6 on 2023-10-24 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cpf',
            field=models.CharField(default='', max_length=9),
        ),
    ]
