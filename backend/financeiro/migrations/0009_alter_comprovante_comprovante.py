# Generated by Django 4.0.5 on 2022-09-26 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0008_alter_comprovante_comprovante_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprovante',
            name='comprovante',
            field=models.ImageField(blank=True, null=True, upload_to='creditos/', verbose_name='Upload Comprovante'),
        ),
    ]
