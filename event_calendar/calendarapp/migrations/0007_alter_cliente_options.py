# Generated by Django 4.2.7 on 2024-05-29 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0006_clientestatuslog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={'ordering': ['nome']},
        ),
    ]
