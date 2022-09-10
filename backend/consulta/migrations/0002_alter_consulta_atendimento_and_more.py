# Generated by Django 4.0.5 on 2022-09-09 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consulta',
            name='atendimento',
            field=models.CharField(choices=[('1', 'Primeira'), ('2', 'Retorno-Exames'), ('3', 'Retorno'),
                                   ('4', 'Emergência'), ('5', 'Remoto')], max_length=30, verbose_name='Atendimento'),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='especialidade',
            field=models.CharField(choices=[('1', 'Alergista'), ('2', 'Cardiologia'), ('3', 'Clinico Geral'), ('4', 'Dermatologia'), ('5', 'Endocrinologia'), ('6', 'Fisiatria'), ('7', 'Fonoaudiologia'), ('8', 'Gastroenterologia'), ('9', 'Geriatria'), ('10', 'Ginecologia'), ('11', 'Nefrologia'), ('12', 'Neurologia'), ('13', 'Nutrição'), ('14', 'Obstetrícia'), (
                '15', 'Odontologia'), ('16', 'Oftalmologia'), ('17', 'Oncologia'), ('18', 'Ortopedia'), ('19', 'Otorrinolaringologia'), ('20', 'Pediatria'), ('21', 'Pneumologia'), ('22', 'Proctologia'), ('23', 'Psicologia'), ('24', 'Psiquiatria'), ('25', 'Reumatologia'), ('26', 'Traumatologia'), ('27', 'Urologia'), ('28', 'Outras')], max_length=30, verbose_name='Especialidade'),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='motivo_cancelamento',
            field=models.CharField(blank=True, choices=[('1', 'Primeira'), ('2', 'Retorno-Exames'), ('3', 'Retorno'),
                                   ('4', 'Emergência'), ('5', 'Remoto')], max_length=30, null=True, verbose_name='Motivo Cancelamento'),
        ),
        migrations.AlterField(
            model_name='glicose',
            name='tipo_insulina',
            field=models.CharField(blank=True, choices=[(
                '1', 'Lantus'), ('2', 'NovoRapid'), ('3', 'Nenhuma')], max_length=30, null=True, verbose_name='Tipo da Insulina'),
        ),
        migrations.AlterField(
            model_name='medicamento',
            name='posologia',
            field=models.CharField(choices=[('1 vez ', '1 vez'), ('2 vezes ', '2 vezes'), ('3 vezes ', '3 vezes'), (
                '4 vezes ', '4 vezes'), ('5 vezes ', '5 vezes'), ('6 vezes ', '6 vezes')], max_length=30, verbose_name='Posologia'),
        ),
        migrations.AlterField(
            model_name='medicamento',
            name='tipo_medicamento',
            field=models.CharField(choices=[('1', 'Comprimido'), ('2', 'Cápsulas'), ('3', 'Creme'), ('4', 'Gotas'), ('5', 'Injeção Musc'), ('6', 'Injeção Subcutânea'), (
                '7', 'Injeção Venosa'), ('8', 'Pomada'), ('9', 'Solução'), ('10', 'Spray'), ('11', 'Supositório'), ('12', 'Outros')], max_length=18, verbose_name='Tipo de Medicamento'),
        ),
    ]
