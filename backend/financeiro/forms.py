from django import forms
from backend.crm.models import Dependente, Usuario, Responsavel
from .models import ContasBancarias, Credito, Comprovante
from django.forms.widgets import ClearableFileInput


class ContasBancariasForm(forms.ModelForm):
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
        model = ContasBancarias
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
