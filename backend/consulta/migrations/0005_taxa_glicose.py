# Generated by Django 4.0.5 on 2022-07-27 00:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_delete_dependente_dependente'),
        ('consulta', '0004_alter_consulta_dependente_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Taxa_glicose',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('data_medicao', models.DateField(verbose_name='Data')),
                ('hora', models.TimeField(verbose_name='Hora')),
                ('taxa_glicose', models.IntegerField(
                    verbose_name='Taxa de Glicose')),
                ('media_diaria', models.DecimalField(decimal_places=2,
                 default=0, max_digits=10, verbose_name='Media Diária')),
                ('media_mensal', models.DecimalField(decimal_places=2,
                 default=0, max_digits=10, verbose_name='Media Mensal')),
                ('estado_alimentar', models.CharField(choices=[('1', 'Em jejum'), ('2', 'Após café da manhã'), ('3', 'Antes de almoçar'), ('4', 'Após almoço'), (
                    '5', 'Antes do jantar'), ('6', 'Após jantar'), ('7', 'Antes de dormir'), ('8', 'Na madrugada')], max_length=30, verbose_name='Estado Alimentar')),
                ('cuidador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='cuidador_medicao', to='crm.cuidador', verbose_name='Cuidador')),
                ('dependente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 to='crm.dependente', verbose_name='Dependente')),
                ('responsavel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='resp_medicao', to='crm.responsavel', verbose_name='Responsável')),
            ],
            options={
                'ordering': ('data_medicao', 'hora'),
            },
        ),
    ]
