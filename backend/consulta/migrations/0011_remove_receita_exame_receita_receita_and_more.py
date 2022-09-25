# Generated by Django 4.0.5 on 2022-09-20 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0010_remove_receita_exames_remove_receita_receita_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receita',
            name='exame',
        ),
        migrations.AddField(
            model_name='receita',
            name='receita',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Upload Receita'),
        ),
        migrations.AlterField(
            model_name='receita',
            name='pos_consulta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receitas', to='consulta.posconsulta'),
        ),
        migrations.CreateModel(
            name='Exame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exame', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Upload Exames')),
                ('pos_consulta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exames', to='consulta.posconsulta')),
            ],
        ),
    ]