# Generated by Django 4.0.5 on 2022-08-18 23:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endereco', models.CharField(blank=True, max_length=200, null=True, verbose_name='Endereço')),
                ('bairro', models.CharField(blank=True, max_length=200, null=True, verbose_name='Bairro')),
                ('cidade', models.CharField(blank=True, max_length=200, null=True, verbose_name='Cidade')),
                ('uf', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='UF')),
                ('active', models.BooleanField(default=True, verbose_name='ativo')),
                ('nome', models.CharField(max_length=200, unique=True, verbose_name='Nome da Família')),
            ],
            options={
                'verbose_name': 'Família',
                'verbose_name_plural': 'Famílias',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endereco', models.CharField(blank=True, max_length=200, null=True, verbose_name='Endereço')),
                ('bairro', models.CharField(blank=True, max_length=200, null=True, verbose_name='Bairro')),
                ('cidade', models.CharField(blank=True, max_length=200, null=True, verbose_name='Cidade')),
                ('uf', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='UF')),
                ('active', models.BooleanField(default=True, verbose_name='ativo')),
                ('data_nascimento', models.DateField(blank=True, null=True, verbose_name='Data de Nascimento')),
                ('rg', models.CharField(blank=True, max_length=20, null=True, verbose_name='RG')),
                ('cpf', models.CharField(blank=True, max_length=14, null=True, verbose_name='CPF')),
                ('celular_whatsapp', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='WhatsApp')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('estado_civil', models.CharField(blank=True, choices=[('1', 'Solteiro(a)'), ('2', 'Casado(a)'), ('3', 'Divorciado(a)'), ('4', 'Viuvo(a)'), ('5', 'União Estável'), ('6', 'Outros')], max_length=1, null=True, verbose_name='Estado Civil')),
                ('nome_conjuge', models.CharField(blank=True, max_length=100, null=True, verbose_name='Cônjuge')),
                ('naturalidade', models.CharField(blank=True, max_length=100, null=True, verbose_name='Naturalidade')),
                ('parentesco_do_responsavel', models.CharField(choices=[('F', 'Filho'), ('N', 'Neto'), ('I', 'Irmão'), ('O', 'Outro')], max_length=1, verbose_name='Parentesco do Responsável')),
                ('dependente_convenio_medico', models.CharField(blank=True, max_length=100, null=True, verbose_name='Convênio')),
                ('dependente_contato_fone_convenio', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone Convênio')),
                ('dependente_contato_endereco_convenio', models.CharField(blank=True, max_length=100, null=True, verbose_name='Endereço Convênio')),
                ('familia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='familia_usuarios', to='crm.familia', verbose_name='Família')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarios', to=settings.AUTH_USER_MODEL, verbose_name='usuário')),
            ],
            options={
                'ordering': ('user__first_name', 'user__last_name'),
            },
        ),
        migrations.CreateModel(
            name='Cuidador',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crm.usuario')),
                ('data_inicio', models.DateField(blank=True, null=True, verbose_name='Admissão')),
                ('data_fim', models.DateField(blank=True, null=True, verbose_name='Demissão')),
                ('regime_contratacao', models.CharField(blank=True, choices=[('CLT', 'CLT'), ('PJ', 'PJ'), ('FREE', 'Free Lance'), ('PS', 'Prestação Serviços')], max_length=10, null=True, verbose_name='Contratação')),
                ('carga_horaria_semanal', models.IntegerField(default=44, verbose_name='Carga Horária Semanal')),
                ('turno_trabalho', models.CharField(blank=True, choices=[('D', 'Diurno'), ('N', 'Noturno')], max_length=1, null=True, verbose_name='Turno')),
                ('quem_indicou', models.CharField(blank=True, max_length=100, null=True, verbose_name='Indicação')),
                ('salario_atual', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Salário')),
                ('adicional', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Adicional')),
                ('dia_pagamento', models.IntegerField(blank=True, null=True, verbose_name='Dia pagamento')),
                ('observacao', models.TextField(blank=True, null=True, verbose_name='Observação')),
            ],
            options={
                'verbose_name': 'Cuidador',
                'verbose_name_plural': 'Cuidadores',
            },
            bases=('crm.usuario',),
        ),
        migrations.CreateModel(
            name='Dependente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endereco', models.CharField(blank=True, max_length=200, null=True, verbose_name='Endereço')),
                ('bairro', models.CharField(blank=True, max_length=200, null=True, verbose_name='Bairro')),
                ('cidade', models.CharField(blank=True, max_length=200, null=True, verbose_name='Cidade')),
                ('uf', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='UF')),
                ('active', models.BooleanField(default=True, verbose_name='ativo')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='nome')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='sobrenome')),
                ('data_nascimento', models.DateField(blank=True, null=True, verbose_name='Data de Nascimento')),
                ('rg', models.CharField(blank=True, max_length=20, null=True, verbose_name='RG')),
                ('cpf', models.CharField(blank=True, max_length=14, null=True, verbose_name='CPF')),
                ('celular_whatsapp', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='WhatsApp')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('estado_civil', models.CharField(blank=True, choices=[('1', 'Solteiro(a)'), ('2', 'Casado(a)'), ('3', 'Divorciado(a)'), ('4', 'Viuvo(a)'), ('5', 'União Estável'), ('6', 'Outros')], max_length=1, null=True, verbose_name='Estado Civil')),
                ('nome_conjuge', models.CharField(blank=True, max_length=100, null=True, verbose_name='Cônjuge')),
                ('naturalidade', models.CharField(blank=True, max_length=100, null=True, verbose_name='Naturalidade')),
                ('parentesco_do_responsavel', models.CharField(choices=[('F', 'Filho'), ('N', 'Neto'), ('I', 'Irmão'), ('O', 'Outro')], max_length=1, verbose_name='Parentesco do Responsável')),
                ('dependente_convenio_medico', models.CharField(blank=True, max_length=100, null=True, verbose_name='Convênio')),
                ('dependente_contato_fone_convenio', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone Convênio')),
                ('dependente_contato_endereco_convenio', models.CharField(blank=True, max_length=100, null=True, verbose_name='Endereço Convênio')),
                ('familia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dependentes', to='crm.familia', verbose_name='Família')),
            ],
            options={
                'ordering': ('first_name',),
            },
        ),
        migrations.CreateModel(
            name='Responsavel',
            fields=[
            ],
            options={
                'verbose_name': 'Responsável',
                'verbose_name_plural': 'Responsáveis',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('crm.usuario',),
        ),
    ]
