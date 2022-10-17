from django import forms
from django.forms import inlineformset_factory

from backend.core.forms import ImagePreviewWidget
from backend.crm.models import Dependente, Responsavel, Usuario

from .models import (
    Comprovante,
    ComprovanteDespesa,
    ContaBancaria,
    Credito,
    Despesa
)


class ContaBancariaForm(forms.ModelForm):
    required_css_class = 'required'

    data_abertura = forms.DateField(
        label='Data Abertura',
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        input_formats=('%Y-%m-%d',),
    )
    data_encerramento = forms.DateField(
        label='Data Encerramento',
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        input_formats=('%Y-%m-%d',),
    )

    class Meta:
        model = ContaBancaria
        fields = '__all__'

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        usuario = Usuario.objects.filter(user=user).first()
        familia = usuario.familia
        queryset = Dependente.objects.filter(familia=familia)
        self.fields['titular_dependente'].queryset = queryset


class CreditoForm(forms.ModelForm):
    required_css_class = 'required'

    data_entrada = forms.DateField(
        label='Entrada',
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        input_formats=('%Y-%m-%d',),
    )
    comprovante = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    class Meta:
        model = Credito
        fields = (
            'data_entrada',
            'referencia',
            'depositante',
            'valor',
            'conta_credito',
            'responsavel_lancamento',
            'comprovante',
            'observacao',
        )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        usuario = Usuario.objects.filter(user=user).first()
        familia = usuario.familia

        queryset_responsavel = Responsavel.objects.filter(familia=familia)
        self.fields['responsavel_lancamento'].queryset = queryset_responsavel


class CreditoUpdateForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Credito
        fields = (
            'data_entrada',
            'referencia',
            'depositante',
            'valor',
            'conta_credito',
            'responsavel_lancamento',
            'observacao',
        )


class ComprovanteAddForm(forms.ModelForm):
    '''
    Insere vários Comprovantes ao editar um crédito.
    '''
    comprovante = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    class Meta:
        model = Comprovante
        fields = ('credito', 'comprovante')

    def __init__(self, credito_pk=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        queryset = Credito.objects.filter(pk=credito_pk)
        self.fields['credito'].queryset = queryset

        if len(queryset) == 1:
            # Remove os tracinhos.
            self.fields['credito'].empty_label = None
            self.fields['credito'].widget = forms.HiddenInput()


class ComprovanteForm(forms.ModelForm):
    '''
    Comprovantes do Crédito.
    '''
    comprovante = forms.ImageField(widget=ImagePreviewWidget,)

    class Meta:
        model = Comprovante
        fields = ('credito', 'id', 'comprovante')


ComprovantesFormset = inlineformset_factory(
    Credito,
    Comprovante,
    form=ComprovanteForm,
    extra=0,
    can_delete=False,
    min_num=1,
    validate_min=True,
)


class DespesaForm(forms.ModelForm):
    required_css_class = 'required'

    data_saida = forms.DateField(
        label='Dta Saída',
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        input_formats=('%Y-%m-%d',),
    )
    comprovante = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    class Meta:
        model = Despesa
        fields = (
            'data_saida',
            'conta_bancaria',
            'referencia',
            'forma_pagamentocredor',
            'credor',
            'valor',
            'responsavel_lancamento',
            'comprovante',
            'observacao',
        )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        usuario = Usuario.objects.filter(user=user).first()
        familia = usuario.familia

        queryset_responsavel = Responsavel.objects.filter(familia=familia)
        self.fields['responsavel_lancamento'].queryset = queryset_responsavel


class DespesaUpdateForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Despesa
        fields = (
            'data_saida',
            'conta_bancaria',
            'forma_pagamentocredor',
            'referencia',
            'credor',
            'valor',
            'responsavel_lancamento',
            'observacao',
        )


class ComprovanteDespesaAddForm(forms.ModelForm):
    '''
    Insere vários Comprovantes ao editar uma Despesa.
    '''
    comprovante = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    class Meta:
        model = ComprovanteDespesa
        fields = ('despesa', 'comprovante')

    def __init__(self, despesa_pk=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        queryset = Despesa.objects.filter(pk=despesa_pk)
        self.fields['despesa'].queryset = queryset

        if len(queryset) == 1:
            # Remove os tracinhos.
            self.fields['despesa'].empty_label = None
            self.fields['despesa'].widget = forms.HiddenInput()


class ComprovanteDespesaForm(forms.ModelForm):
    '''
    Comprovantes de Despesa.
    '''
    comprovante = forms.ImageField(widget=ImagePreviewWidget,)

    class Meta:
        model = ComprovanteDespesa
        fields = ('despesa', 'id', 'comprovante')


ComprovantesDespesaFormset = inlineformset_factory(
    Despesa,
    ComprovanteDespesa,
    form=ComprovanteDespesaForm,
    extra=0,
    can_delete=False,
    min_num=1,
    validate_min=True,
)
