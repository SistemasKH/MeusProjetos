# Generated by Django 4.0.5 on 2022-09-25 22:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0007_alter_comprovante_credito'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprovante',
            name='comprovante',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Upload Comprovante'),
        ),
        migrations.AlterField(
            model_name='comprovante',
            name='credito',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='comprovantes', to='financeiro.credito'),
        ),
    ]
