# Generated by Django 4.0.5 on 2022-10-18 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0015_contabancaria_saldo_atual'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='credito',
            options={'ordering': ('-data_entrada', 'conta_credito'), 'verbose_name': 'Crédito Bancário', 'verbose_name_plural': 'Creditos Bancários'},
        ),
        migrations.AlterModelOptions(
            name='despesa',
            options={'ordering': ('-data_saida', 'conta_bancaria'), 'verbose_name': 'Despesa', 'verbose_name_plural': 'Despesas'},
        ),
    ]
