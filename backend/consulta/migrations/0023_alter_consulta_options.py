# Generated by Django 4.0.5 on 2022-10-09 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0022_alter_glicose_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consulta',
            options={'ordering': ('-data_consulta', '-hora')},
        ),
    ]
