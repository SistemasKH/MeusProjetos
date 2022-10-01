# Generated by Django 4.0.5 on 2022-09-25 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0002_credito'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='credito',
            options={'ordering': ['-data_entrada'], 'verbose_name': 'Crédito Bancário',
                     'verbose_name_plural': 'Creditos Bancários'},
        ),
        migrations.RemoveField(
            model_name='credito',
            name='comprovante',
        ),
        migrations.CreateModel(
            name='Comprovante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comprovante', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Upload Receita')),
                ('credito', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='comprovante', to='financeiro.credito')),
            ],
        ),
    ]
