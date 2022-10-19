# Generated by Django 4.0.5 on 2022-10-19 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0017_alter_despesa_credor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesa',
            name='credor',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Pago a '),
        ),
        migrations.AlterField(
            model_name='despesa',
            name='forma_pagamentocredor',
            field=models.CharField(choices=[('1', 'Cheque'), ('2', 'Débito cartão'), ('3', 'Débitado em conta corrente'), ('4', 'Dinheiro')], max_length=15, verbose_name='Forma de Pagamento'),
        ),
    ]
