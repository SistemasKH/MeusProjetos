# Generated by Django 4.0.5 on 2022-07-22 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_alter_usuario_naturalidade_alter_usuario_telefone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='parentesco_do_responsavel',
            field=models.CharField(blank=True, choices=[('F', 'Filho'), ('N', 'Neto'), (
                'I', 'Irmão'), ('O', 'Outro')], max_length=1, verbose_name='Parentesco do Responsável'),
        ),
    ]