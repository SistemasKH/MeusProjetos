# Generated by Django 4.0.5 on 2022-10-06 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0019_alter_consulta_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consulta',
            options={'ordering': ('data_consulta', 'hora')},
        ),
    ]