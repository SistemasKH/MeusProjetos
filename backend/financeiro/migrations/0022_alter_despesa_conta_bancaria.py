# Generated by Django 4.0.5 on 2022-10-25 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0021_alter_despesa_conta_bancaria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesa',
            name='conta_bancaria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financeiro.contabancaria', verbose_name='Conta Bancária'),
        ),
    ]