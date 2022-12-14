import datetime
import decimal
from datetime import date, time, timedelta
from django.db import models
from django.urls import reverse, reverse_lazy

from backend.core.constants import (
    ATENDIMENTO_CHOICES,
    CANCELAMENTO_CONSULTA_CHOICES,
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
    motivo_cancelamento = models.CharField('Motivo Cancelamento', max_length=30, choices=CANCELAMENTO_CONSULTA_CHOICES, blank=True, null=True)  # noqa E501

    class Meta:
        ordering = ('-data_consulta', '-hora')

    def __str__(self):
        return f'{self.pk} - {self.dependente} - {self.nome_especialista} - {self.especialidade}'  # noqa E501

    def get_absolute_url(self):
        return reverse("consulta_detail", kwargs={"pk": self.id})

    @property
    def list_url(self):
        return reverse_lazy('consulta_list')

    @property
    def update_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('consulta_edit', kwargs=kw)
        return None

    @property
    def delete_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('consulta_delete', kwargs=kw)
        return None


class PosConsulta(models.Model):
    consulta = models.OneToOneField(
        Consulta,
        on_delete=models.CASCADE,
        related_name='pos_consulta'
    )
    acompanhante_responsavel = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        verbose_name='Responsável'
    )
    diagnostico = models.TextField('Diagnóstico')  # noqa E501
    tratamento = models.TextField('Tratamento', blank=True, null=True)  # noqa E501
    observacao = models.TextField('Observação', blank=True, null=True)  # noqa E501

    def __str__(self):
        return f'{self.pk} - {self.consulta.dependente}'

    def get_upload_to(instance, filename):
        return instance.get_upload_to(filename)

    def get_absolute_url(self):
        return reverse("posconsulta_detail", kwargs={"pk": self.id})

    @property
    def list_url(self):
        return reverse_lazy('posconsulta_list')

    @property
    def update_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('posconsulta_edit', kwargs=kw)
        return None

    @property
    def delete_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('posconsulta_delete', kwargs=kw)
        return None


class Receita(models.Model):
    '''
    Insere várias receitas para a mesma pós-consulta.
    '''
    pos_consulta = models.ForeignKey(
        PosConsulta,
        on_delete=models.SET_NULL,
        related_name='receitas',
        null=True,
        blank=True
    )
    receita = models.ImageField('Upload Receita', upload_to='receitas/', blank=True, null=True)  # noqa E501

    def __str__(self):
        return f'{self.pos_consulta} - {self.receita}'


class Exame(models.Model):
    '''
    Insere vários pedido de exames para a mesma pós-consulta.
    '''
    pos_consulta = models.ForeignKey(
        PosConsulta,
        on_delete=models.SET_NULL,
        related_name='exames',
        null=True,
        blank=True
    )
    exame = models.ImageField('Upload Exames',  upload_to='exames/', blank=True, null=True)  # noqa E501

    def __str__(self):
        return f'{self.pos_consulta} - {self.exame}'


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

    @property
    def list_url(self):
        return reverse_lazy('medicamento_list')

    @property
    def update_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('medicamento_edit', kwargs=kw)
        return None

    @property
    def delete_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('medicamento_delete', kwargs=kw)
        return None


class Glicose(models.Model):
    dependente = models.ForeignKey(
        Dependente,
        on_delete=models.CASCADE,
        verbose_name='Dependente'
    )
    data_medicao = models.DateField('Data')  # noqa E501
    hora = models.TimeField('Hora')  # noqa E501
    estado_alimentar = models.CharField('Estado Alimentar', max_length=30, choices=REFEICAO_CHOICES)  # noqa E501
    taxa_glicose = models.IntegerField('Taxa de Glicose')  # noqa E501
    alimentos = models.TextField('Alimentação', blank=True, null=True)  # noqa E501
    tipo_insulina = models.CharField('Tipo da Insulina', max_length=30, choices=TIPO_INSULINA_CHOICES, blank=True, null=True)  # noqa E501
    qt_insulina = models.IntegerField('Quant. aplicada', default=0)  # noqa E501
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
    ultimo = models.BooleanField(default=False)

    class Meta:
        ordering = ('-data_medicao', '-hora')

    def __str__(self):
        return f'{self.cuidador} - {self.dependente} - {self.responsavel}'

    def get_absolute_url(self):
        return reverse("glicose_detail", kwargs={"pk": self.id})

    @property
    def list_url(self):
        return reverse_lazy('glicose_list')

    @property
    def update_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('glicose_edit', kwargs=kw)
        return None

    @property
    def delete_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('glicose_delete', kwargs=kw)
        return None


class EscalaResponsavel(models.Model):
    responsavel_presencial = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        verbose_name='Resp. Presencial',
        related_name='responsavel_presencial'
    )
    data_inicio = models.DateField('Data de Chegada')  # noqa E501
    hora_inicio = models.TimeField('Hora de Chegada')  # noqa E501
    data_saida_presencial = models.DateField('Data Saída Presencial', null=True)  # noqa E501
    qt_dias_presenciais = models.IntegerField('Quant. dias presenciais ', default=0)  # noqa E501
    qt_horas_presentes = models.DecimalField('Quant. horas', decimal_places=2, default=0, max_digits=6)  # noqa E501
    hora_saida_presencial = models.TimeField('Hora de Saída')  # noqa E501
    responsavel_monitoramento = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        verbose_name='Resp. Monitoramento',
        related_name='responsavel_monitoramento'
    )
    data_fim = models.DateField('Data Final do Plantão', null=True)  # noqa E501
    observacao = models.TextField('Observação', blank=True, null=True)  # noqa E501

    class Meta:
        ordering = ('data_inicio', 'hora_inicio')
        verbose_name = 'Escala Responsável'
        verbose_name_plural = 'Escalas Responsáveis'

    def __str__(self):
        return f'{self.responsavel_presencial} - {self.responsavel_monitoramento} - {self.qt_horas_presentes} '

    def get_absolute_url(self):
        return reverse("escalaresponsavel_detail", kwargs={"pk": self.id})

    @property
    def list_url(self):
        return reverse_lazy('escalaresponsavel_list')

    @property
    def update_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('escalaresponsavel_edit', kwargs=kw)
        return None

    @property
    def delete_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('escalaresponsavel_delete', kwargs=kw)
        return None


class JornadaTrabalho(models.Model):
    cuidador = models.ForeignKey(
        Cuidador,
        on_delete=models.CASCADE,
        verbose_name='funcionario',
        related_name='funcionario'
    )
    dh_entrada = models.DateTimeField('Data/Hora entrada')  # noqa E501
    dh_saida = models.DateTimeField('Data/Hora saída')  # noqa E501
    horas_trabalhadas_diaria = models.DurationField('Horas Diarias')  # noqa E501
    soma_horas_semanal = models.DurationField('Horas semanais')
    soma_horas_mensal = models.DurationField('Horas mensais')
    feriado = models.BooleanField('Feriado', default=False)
    responsavel_dia = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        verbose_name='Responsavel do dia',
        related_name='responsavel_dia'
    )
    observacao = models.TextField('Observação', blank=True, null=True)  # noqa E501

    class Meta:
        ordering = 'dh_entrada', 'cuidador'
        verbose_name = 'Jornada de Trabalho',
        verbose_name_plural = 'Jornadas de Trabalho'

    def __str__(self):
        return f'{self.cuidador} -  {self.dh_entrada} - {self.responsavel_dia} - {self.horas_trabalhadas_diaria} - {self. soma_horas_semanal} - {self. soma_horas_mensal} '

    def get_absolute_url(self):
        return reverse("jornadatrabalho_detail", kwargs={"pk": self.id})

    @property
    def list_url(self):
        return reverse_lazy('jornadatrabalho_list')

    @property
    def update_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('jornadatrabalho_edit', kwargs=kw)
        return None

    @property
    def delete_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('jornadatrabalho_delete', kwargs=kw)
        return None
