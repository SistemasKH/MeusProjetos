from django import forms

from backend.core.services import has_group

from .models import Cuidador, Dependente, Familia, Responsavel


class CustomUserForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nome',
        max_length=150,
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150,
    )
    email = forms.EmailField(
        label='E-mail',
    )

    class Meta:
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if kwargs['instance']:
            user_instance = kwargs['instance'].user

        if user:
            self.fields['first_name'].initial = user_instance.first_name
            self.fields['last_name'].initial = user_instance.last_name
            self.fields['email'].initial = user_instance.email

            if not has_group(user, 'responsavel_principal'):
                self.fields['first_name'].widget.attrs['readonly'] = True
                self.fields['last_name'].widget.attrs['readonly'] = True


class FamiliaForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Familia
        fields = (
            'nome',
            'endereco',
            'bairro',
            'cidade',
            'uf',
        )


class DataNascimentoForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        label='Data de Nascimento',
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
        fields = ('data_nascimento',)


class ResponsavelAddForm(CustomUserForm, DataNascimentoForm):
    required_css_class = 'required'

    class Meta:
        model = Responsavel
        fields = CustomUserForm.Meta.fields + DataNascimentoForm.Meta.fields + (
            'rg',
            'cpf',
            'celular_whatsapp',
            'telefone',
            'estado_civil',
            'nome_conjuge',
            'naturalidade',
            'parentesco_do_responsavel',
            'endereco',
            'bairro',
            'cidade',
            'uf',
        )


class ResponsavelUpdateForm(CustomUserForm, DataNascimentoForm):
    required_css_class = 'required'

    class Meta:
        model = Responsavel
        fields = CustomUserForm.Meta.fields + DataNascimentoForm.Meta.fields + (
            'rg',
            'cpf',
            'celular_whatsapp',
            'telefone',
            'estado_civil',
            'nome_conjuge',
            'naturalidade',
            'parentesco_do_responsavel',
            'endereco',
            'bairro',
            'cidade',
            'uf',
        )

    def save(self, commit=True):
        instance = super().save(commit=False)

        user = instance.user

        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']

        if commit:
            user.username = email
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            instance.save()
        return instance


class CuidadorAddForm(CustomUserForm, DataNascimentoForm):
    required_css_class = 'required'

    data_inicio = forms.DateField(
        label='Admissão',
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        input_formats=('%Y-%m-%d',),
    )
    data_fim = forms.DateField(
        label='Demissão',
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
        model = Cuidador
        fields = CustomUserForm.Meta.fields + DataNascimentoForm.Meta.fields + (
            'rg',
            'cpf',
            'celular_whatsapp',
            'telefone',
            'estado_civil',
            'nome_conjuge',
            'naturalidade',
            'endereco',
            'bairro',
            'cidade',
            'uf',
            'data_inicio',
            'data_fim',
            'regime_contratacao',
            'carga_horaria_semanal',
            'turno_trabalho',
            'quem_indicou',
            'salario_atual',
            'adicional',
            'dia_pagamento',
            'observacao',
        )


class CuidadorUpdateForm(CustomUserForm, DataNascimentoForm):
    required_css_class = 'required'

    data_inicio = forms.DateField(
        label='Admissão',
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        input_formats=('%Y-%m-%d',),
    )
    data_fim = forms.DateField(
        label='Demissão',
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
        model = Cuidador
        fields = CustomUserForm.Meta.fields + DataNascimentoForm.Meta.fields + (
            'rg',
            'cpf',
            'celular_whatsapp',
            'telefone',
            'estado_civil',
            'nome_conjuge',
            'naturalidade',
            'endereco',
            'bairro',
            'cidade',
            'uf',
            'data_inicio',
            'data_fim',
            'regime_contratacao',
            'carga_horaria_semanal',
            'turno_trabalho',
            'quem_indicou',
            'salario_atual',
            'adicional',
            'dia_pagamento',
            'observacao',
        )

    def save(self, commit=True):
        instance = super().save(commit=False)

        user = instance.user

        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']

        if commit:
            user.username = email
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            instance.save()
        return instance


class DependenteAddForm(DataNascimentoForm):
    required_css_class = 'required'

    class Meta:
        model = Dependente
        fields = (
            'first_name',
            'last_name',
            'data_nascimento',
            'rg',
            'cpf',
            'celular_whatsapp',
            'telefone',
            'estado_civil',
            'nome_conjuge',
            'naturalidade',
            'endereco',
            'bairro',
            'cidade',
            'uf',
            'dependente_convenio_medico',
            'dependente_contato_fone_convenio',
            'dependente_contato_endereco_convenio',
        )


class DependenteUpdateForm(forms.ModelForm):
    required_css_class = 'required'

    data_nascimento = forms.DateField(
        label='Data de Nascimento',
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
        model = Dependente
        fields = (
            'first_name',
            'last_name',
            'data_nascimento',
            'rg',
            'cpf',
            'celular_whatsapp',
            'telefone',
            'estado_civil',
            'nome_conjuge',
            'naturalidade',
            'endereco',
            'bairro',
            'cidade',
            'uf',
            'dependente_convenio_medico',
            'dependente_contato_fone_convenio',
            'dependente_contato_endereco_convenio',
        )
