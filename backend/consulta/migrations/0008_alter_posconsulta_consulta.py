# Generated by Django 4.0.7 on 2022-09-13 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0007_alter_jornadatrabalho_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posconsulta',
            name='consulta',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pos_consulta', to='consulta.consulta'),
        ),
    ]
