# Generated by Django 4.0.7 on 2022-09-13 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0006_alter_escalaresponsavel_qt_dias_presenciais'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jornadatrabalho',
            options={'ordering': ('dh_entrada',), 'verbose_name': ('Jornada de Trabalho',), 'verbose_name_plural': 'Jornadas de Trabalho'},
        ),
        migrations.AlterField(
            model_name='posconsulta',
            name='consulta',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pos_consultas', to='consulta.consulta'),
        ),
    ]
