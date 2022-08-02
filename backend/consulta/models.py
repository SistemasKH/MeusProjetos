from django.db import models
from django.urls import reverse

from backend.core.constants import (
    ATENDIMENTO_CHOICES,
    ESPECIALIDADE_CHOICES,
    FORNECEDOR_PRINCIPAL_CHOICES,
    POSOLOGIA_CHOICES,
    REFEICAO_CHOICES,
    TIPO_INSULINA_CHOICES,
    TIPO_MEDICAMENTO_CHOICES,
    USO_CONTINUO_CHOICES
)
from backend.crm.models import Cuidador, Dependente, Responsavel


class Consulta(models.Model):
    dependente = models.ForeignKey(
        Dependente,
        on_delete=models.CASCADE,
        related_name='consultas'
    )
    data_consulta = models.DateField('Data Consulta')
    hora = models.TimeField('Hora')
    especialidade = models.CharField('Especialidade', max_length=30, choices=ESPECIALIDADE_CHOICES)  # noqa E501
    local = models.CharField('Local', max_length=100, blank=True, null=True)  # noqa E501
    nome_especialista = models.CharField('Especialista', max_length=100)  # noqa E501
    fone_contato = models.CharField('Fone', max_length=100, blank=True, null=True)  # noqa E501
    atendimento = models.CharField('Atendimento', max_length=30, choices=ATENDIMENTO_CHOICES)  # noqa E501
    motivo_consulta = models.CharField('Motivo Consulta', max_length=300, blank=True, null=True)  # noqa E501
    sintomas = models.CharField('Sintomas', max_length=300, blank=True, null=True)  # noqa E501
    observacao = models.CharField('Observação', max_length=300, blank=True, null=True)  # noqa E501
    acompanhante_responsavel = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        verbose_name='Acompanhante Responsável'
    )
    cancelamento = models.DateField('Data Cancelamento', blank=True, null=True)  # noqa E501
    motivo_cancelamento = models.CharField('Motivo Cancelamento', max_length=30, choices=ATENDIMENTO_CHOICES, blank=True, null=True)  # noqa E501

    class Meta:
        ordering = ('data_consulta', 'hora')

    def __str__(self):
        return f'{self.pk} - {self.dependente} - {self.data_consulta} - {self.hora} - {self.nome_especialista} - {self.especialidade}'  # noqa E501

    def get_absolute_url(self):
        return reverse("consulta_detail", kwargs={"pk": self.id})


class PosConsulta(models.Model):
    consulta = models.ForeignKey(
        Consulta,
        on_delete=models.CASCADE,
        related_name='pos_consultas'
    )
    acompanhante_responsavel = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        verbose_name='Responsável'
    )
    diagnostico = models.TextField('Diagnóstico')  # noqa E501
    tratamento = models.TextField('Tratamento', blank=True, null=True)  # noqa E501
    receita = models.ImageField('Upload Receita', upload_to='', blank=True, null=True)  # noqa E501
    observacao = models.TextField('Observação', blank=True, null=True)  # noqa E501

    def __str__(self):
        return f'{self.pk} - {self.consulta.dependente}'

    def get_upload_to(instance, filename):
        return instance.get_upload_to(filename)

    def get_absolute_url(self):
        return reverse("posconsulta_detail", kwargs={"pk": self.id})


class Medicamento(models.Model):
    medicamento_prescrito = models.CharField('Medicamento Prescrito', max_length=100)  # noqa E501
    principio_ativo = models.CharField('Princípo Ativo', max_length=40, blank=True, null=False)  # noqa E501
    indicacoes = models.TextField('Indicações', blank=True, null=True)  # noqa E501
    tipo_medicamento = models.CharField('Tipo de Medicamento', max_length=18, choices=TIPO_MEDICAMENTO_CHOICES)  # noqa E501
    dosagem = models.CharField('Dosagem', max_length=40)  # noqa E501
    posologia = models.CharField('Posologia', max_length=30, choices=POSOLOGIA_CHOICES)  # noqa E501
    uso_continuo = models.CharField('Uso Continuo', max_length=30, choices=USO_CONTINUO_CHOICES)  # noqa E501
    data_inicio = models.DateField('Data Início', blank=True, null=True)  # noqa E501
    data_fim = models.DateField('Data Fim', blank=True, null=True)  # noqa E501
    forma_uso = models.TextField('Forma de Uso')  # noqa E501
    orientacao_tratamento = models.TextField('Orientações')  # noqa E501
    medico_responsavel = models.CharField('Médico Responsável', max_length=100, blank=True, null=True)  # noqa E501
    fornecedor_principal = models.CharField('Fornecedor', max_length=20, choices=FORNECEDOR_PRINCIPAL_CHOICES)  # noqa E501
    dependente = models.ForeignKey(
        Dependente,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('dependente', 'medicamento_prescrito')

    def __str__(self):
        return f'{self.medicamento_prescrito} - {self.dependente}'

    def get_absolute_url(self):
        return reverse("medicamento_detail", kwargs={"pk": self.id})


class Glicose(models.Model):
    dependente = models.ForeignKey(
        Dependente,
        on_delete=models.CASCADE,
        verbose_name='Dependente'
    )
    data_medicao = models.DateField('Data')  # noqa E501
    hora = models.TimeField('Hora')  # noqa E501
    estado_alimentar = models.CharField('Estado Alimentar', max_length=30, choices=REFEICAO_CHOICES)  # noqa E501
    taxa_glicose = models.IntegerField('Taxa de Glicose', max_length=3)  # noqa E501
    alimentos = models.TextField('Alimentação', blank=True, null=True)  # noqa E501
    tipo_insulina = models.CharField('Tipo da Insulina', max_length=30, choices=TIPO_INSULINA_CHOICES, blank=True, null=True)  # noqa E501
    qt_insulina = models.IntegerField('Qtdade aplicada', max_length=2, default=0)  # noqa E501
    observacao = models.TextField('Observação', blank=True, null=True)  # noqa E501
    media_diaria = models.DecimalField('Media Diária', max_digits=10, decimal_places=2, default=0, blank=True, null=True)  # noqa E501
    media_mensal = models.DecimalField('Media Mensal', max_digits=10, decimal_places=2, default=0, blank=True, null=True)  # noqa E501
    responsavel = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        verbose_name='Responsável',
        related_name='Responsavel'
    )
    cuidador = models.ForeignKey(
        Cuidador,
        on_delete=models.CASCADE,
        verbose_name='Cuidador',
        related_name='Cuidador'
    )

    class Meta:
        ordering = ('data_medicao', 'hora')

    def __str__(self):
        return f'{self.cuidador} - {self.dependente} - {self.responsavel}'

    def get_absolute_url(self):
        return reverse("glicose_detail", kwargs={"pk": self.id})


class EscalaResponsaveis(models.Model):
    responsavel = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        verbose_name='Responsável'
    )
    data_inicial = models.DateField('Data Inicial')  # noqa E501
    hora_inicio = models.TimeField('Hora Combinada')  # noqa E501
    data_fim = models.DateField('Data Final')  # noqa E501
    qt_dias = models.IntegerField('Qtdade dias', max_length=2, default=0)  # noqa E501
    observacao = models.TextField('Observação', blank=True, null=True)  # noqa E501

    class Meta:
        ordering = ('data_inicial', 'hora_inicio')

    def __str__(self):
        return f'{self.responsavel}'

    def get_absolute_url(self):
        return reverse("escalaresp_detail", kwargs={"pk": self.id})
