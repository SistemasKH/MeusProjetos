from django import forms
from backend.crm.models import Dependente, Usuario
from .models import ContasBancarias
from django.shortcuts import redirect, render, resolve_url
from django.contrib import messages


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