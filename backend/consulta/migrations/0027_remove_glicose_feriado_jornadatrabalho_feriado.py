# Generated by Django 4.0.5 on 2022-10-19 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0026_glicose_feriado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='glicose',
            name='feriado',
        ),
        migrations.AddField(
            model_name='jornadatrabalho',
            name='feriado',
            field=models.BooleanField(default=False, verbose_name='Feriado'),
        ),
    ]
