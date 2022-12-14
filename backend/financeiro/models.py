from django.db import models
from django.urls import reverse, reverse_lazy

from backend.core.constants import (
    CREDITO_REF_CHOICES,
    DESPESA_CHOICES,
    FORMA_PAGAMENTO_CHOICES,
    TIPO_CONJUNTA_CHOICES,
    TIPO_CONTA_CHOICES
)
from backend.crm.models import Dependente, Responsavel


class ContaBancaria(models.Model):
    titular_dependente = models.ForeignKey(
        Dependente,
        on_delete=models.CASCADE,
        verbose_name='Nome Titular',
        related_name='titular_dependente'
    )
    data_abertura = models.DateField('Data Abertura',  blank=True, null=True)  # noqa E501
    nome_banco = models.CharField('Nome do Banco', max_length=30)  # noqa E501
    numero_banco = models.IntegerField('Número banco')  # noqa E501
    agencia = models.CharField('Agência', default=0, max_length=10)  # noqa E501
    cidade = models.CharField('Cidade', max_length=30,  blank=True, null=True)  # noqa E501
    conta = models.CharField('Tipo conta', max_length=30, choices=TIPO_CONTA_CHOICES)  # noqa E501
    numero_conta = models.CharField('Número conta', max_length=30)  # noqa E501
    conjunta = models.CharField('Conjunta', max_length=30, choices=TIPO_CONJUNTA_CHOICES)
    saldo_inicial = models.DecimalField('Saldo Inicial', max_digits=15, decimal_places=2, default=0)  # noqa E501
    saldo_atual = models.DecimalField('Saldo Atual', max_digits=15, decimal_places=2, default=0)  # noqa E501
    data_encerramento = models.DateField('Data Encerramento', blank=True, null=True)  # noqa E501
    observacao = models.TextField('Observação', blank=True, null=True)  # noqa E501

    class Meta:
        ordering = ('nome_banco',)
        verbose_name = 'Conta Bancária'
        verbose_name_plural = 'Contas Bancárias'


    def __str__(self):
        return f'{self.titular_dependente} -  {self.nome_banco} '

    def get_absolute_url(self):
        return reverse("contabancaria_detail", kwargs={"pk": self.id})

    @property
    def list_url(self):
        return reverse_lazy('contabancaria_list')

    @property
    def update_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('contabancaria_edit', kwargs=kw)
        return None

    @property
    def delete_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('conta_bancaria_delete', kwargs=kw)
        return None


class Credito(models.Model):
    data_entrada = models.DateField('Data Entrada')  # noqa E501
    referencia = models.CharField('Referência', max_length=30, choices=CREDITO_REF_CHOICES)  # noqa E501
    depositante = models.CharField('Depositante', max_length=100, blank=True, null=True)  # noqa E501
    valor = models.DecimalField('Valor',  max_digits=15, decimal_places=2, default=0)  # noqa E501
    saldo_atual = models.DecimalField('Saldo Atual', max_digits=15, decimal_places=2, default=0) # noqa E501
    conta_credito = models.ForeignKey(
        ContaBancaria,
        on_delete=models.CASCADE,
        verbose_name='Conta Crédito'
    )
    responsavel_lancamento = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        verbose_name='Responsável'
    )
    observacao = models.CharField('Observação', max_length=300, blank=True, null=True)  # noqa E501

    class Meta:
        ordering = ('-data_entrada', 'conta_credito')
        verbose_name = 'Crédito Bancário'
        verbose_name_plural = 'Creditos Bancários'

    def __str__(self):
        return f'{self.pk} - {self.data_entrada} - {self.depositante} - {self.conta_credito} - {self.valor} - {self.comprovantes} -{self.responsavel_lancamento}'  # noqa E501

    def get_upload_to(instance, filename):
        return instance.get_upload_to(filename)

    def get_absolute_url(self):
        return reverse("credito_detail", kwargs={"pk": self.id})

    @property
    def list_url(self):
        return reverse_lazy('credito_list')

    @property
    def update_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('credito_edit', kwargs=kw)
        return None

    @property
    def delete_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('credito_delete', kwargs=kw)
        return None


class Comprovante(models.Model):
    '''
    Insere vários comprovantes para o mesmo crédito.
    '''
    credito = models.ForeignKey(
        Credito,
        on_delete=models.SET_NULL,
        related_name='comprovantes',
        null=True,
        blank=True
    )
    comprovante = models.ImageField(
        'Upload Comprovante',
        upload_to='creditos/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.credito}-{self.comprovante}'


class Despesa(models.Model):
    data_saida = models.DateField('Data Saída')  # noqa E501
    referencia = models.CharField('Referência', max_length=30, choices=DESPESA_CHOICES)  # noqa E501
    forma_pagamentocredor = models.CharField('Forma de Pagamento', max_length=15, choices=FORMA_PAGAMENTO_CHOICES)  # noqa E501
    credor = models.CharField('Pago a ', max_length=70, blank=True, null=True)  # noqa E501
    valor = models.DecimalField('Valor',  max_digits=15, decimal_places=2, default=0)  # noqa E501
    saldo_atual = models.DecimalField('Saldo Atual',  max_digits=15, decimal_places=2, default=0)  # noqa E501
    conta_bancaria = models.ForeignKey(
        ContaBancaria,
        on_delete=models.CASCADE,
        verbose_name='Conta Bancária'
    )
    responsavel_lancamento = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        verbose_name='Responsável'
    )
    observacao = models.CharField('Observação', max_length=300, blank=True, null=True)  # noqa E501

    class Meta:
        ordering = ('-data_saida', 'conta_bancaria')
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'

    def __str__(self):
        return f'{self.pk} - {self.data_saida} - {self.conta_bancaria} - {self.referencia} - {self.forma_pagamentocredor} - {self.valor} - {self.responsavel_lancamento}'  # noqa E501

    def get_upload_to(instance, filename):
        return instance.get_upload_to(filename)

    def get_absolute_url(self):
        return reverse("despesa_detail", kwargs={"pk": self.id})

    @property
    def list_url(self):
        return reverse_lazy('despesa_list')

    @property
    def update_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('despesa_edit', kwargs=kw)
        return None

    @property
    def delete_url(self):
        if self.pk:
            kw = {'pk': self.pk}
            return reverse_lazy('despesa_delete', kwargs=kw)
        return None


class ComprovanteDespesa(models.Model):
    '''
    Insere vários comprovantes para a mesma despesa.
    '''
    despesa = models.ForeignKey(
        Despesa,
        on_delete=models.SET_NULL,
        related_name='comprovantes',
        null=True,
        blank=True
    )
    comprovante = models.ImageField(
        'Upload Comprovante',
        upload_to='despesa/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.despesa}-{self.comprovante}'
