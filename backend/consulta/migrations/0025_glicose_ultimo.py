# Generated by Django 4.0.7 on 2022-10-17 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0024_alter_jornadatrabalho_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='glicose',
            name='ultimo',
            field=models.BooleanField(default=False),
        ),
    ]
