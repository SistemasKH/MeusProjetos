# Generated by Django 4.0.5 on 2022-07-22 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_alter_usuario_parentesco_do_responsavel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='parentesco_do_responsavel',
            field=models.CharField(choices=[('F', 'Filho'), ('N', 'Neto'), ('I', 'Irmão'), (
                'O', 'Outro')], default='F', max_length=1, verbose_name='Parentesco do Responsável'),
        ),
    ]