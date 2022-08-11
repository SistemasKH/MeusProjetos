from datetime import date, timedelta

from django import forms

from backend.crm.models import Cuidador, Dependente, Responsavel, Usuario

from .models import (
    Consulta,
    EscalaResponsavel,
    Glicose,
    Medicamento,
    PosConsulta
)


class DependentesDaFamiliaForm(forms.Form):
    dependente = forms.ModelChoiceField(
        label='Dependente',
        widget=forms.Select(
            attrs={'class': 'form-control'},
        ),
        queryset=Dependente.objects.all()
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        usuario = user.usuarios.first()
        familia = usuario.familia
        queryset = Dependente.objects.filter(familia__nome=familia)
        self.fields['dependente'].queryset = queryset


class ConsultaForm(forms.ModelForm):
    required_css_class = 'required'

    data_consulta = forms.DateField(
        label='Data Consulta',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        input_formats=('%Y-%m-%d',),
    )
    hora = forms.TimeField(
        label='Hora',
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control'
            }),
    )
    cancelamento = forms.DateField(
        label='Data Cancelamento',
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
        model = Consulta
        fields = '__all__'

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hora'].widget.attrs.update({'class': 'mask-hora'})

        usuario = Usuario.objects.filter(user=user).first()
        familia = usuario.familia
        queryset = Dependente.objects.filter(familia=familia)
        self.fields['dependente'].queryset = queryset

        queryset_responsavel = Responsavel.objects.filter(familia=familia)
        self.fields['acompanhante_responsavel'].queryset = queryset_responsavel


class PosConsultaForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = PosConsulta
        fields = '__all__'

    def __init__(self, request, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        consulta = Consulta.objects.filter(pk=self.instance.consulta.pk)
        self.fields['consulta'].queryset = consulta

        acompanhante_responsavel = consulta.first().acompanhante_responsavel
        queryset = Responsavel.objects.filter(pk=acompanhante_responsavel.pk)
        self.fields['acompanhante_responsavel'].queryset = queryset

        if len(consulta) == 1:
            # Remove os tracinhos.
            self.fields['consulta'].empty_label = None
            self.fields['acompanhante_responsavel'].empty_label = None


class MedicamentoForm(forms.ModelForm):
    required_css_class = 'required'

    data_inicio = forms.DateField(
        label='Data Início',
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
        label='Data Fim',
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
        model = Medicamento
        fields = '__all__'

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        usuario = Usuario.objects.filter(user=user).first()
        familia = usuario.familia
        queryset = Dependente.objects.filter(familia=familia)
        self.fields['dependente'].queryset = queryset


class GlicoseForm(forms.ModelForm):
    required_css_class = 'required'

    data_medicao = forms.DateField(
        label='Data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        input_formats=('%Y-%m-%d',),
    )
    hora = forms.TimeField(
        label='Hora',
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control'
            }),
    )

    class Meta:
        model = Glicose
        fields = '__all__'
        exclude = ('media_diaria', 'media_mensal')

    def calcula_taxa_media_diaria_de_glicose(self, instance):
        # Filtra pelo dependente e pela data_medicao.
        glicoses = Glicose.objects.filter(
            dependente=instance.dependente,
            data_medicao=instance.data_medicao,
        )
        taxas = [glicose.taxa_glicose for glicose in glicoses]
        taxas.append(instance.taxa_glicose)
        try:
            return sum(taxas) / len(taxas)
        except ZeroDivisionError:
            return sum(taxas)

    def calcula_taxa_media_mensal_de_glicose(self, instance):
        data_final = instance.data_medicao
        data_inicial = data_final - timedelta(30)
        glicoses = Glicose.objects.filter(
            dependente=instance.dependente,
            data_medicao__range=[data_inicial, data_final]
        )
        taxas = [glicose.taxa_glicose for glicose in glicoses]
        taxas.append(instance.taxa_glicose)
        try:
            return sum(taxas) / len(taxas)
        except ZeroDivisionError:
            return sum(taxas)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        usuario = Usuario.objects.filter(user=user).first()
        familia = usuario.familia

        queryset = Dependente.objects.filter(familia=familia)
        self.fields['dependente'].queryset = queryset

        queryset_responsavel = Responsavel.objects.filter(familia=familia)
        self.fields['responsavel'].queryset = queryset_responsavel

        queryset_cuidador = Cuidador.objects.filter(familia=familia)
        self.fields['cuidador'].queryset = queryset_cuidador

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.media_diaria = self.calcula_taxa_media_diaria_de_glicose(instance)  # noqa E501
            instance.media_mensal = self.calcula_taxa_media_mensal_de_glicose(instance)  # noqa E501
            instance.save()
        return instance


class EscalaResponsavelForm(forms.ModelForm):
    required_css_class = 'required'

    data_inicio = forms.DateField(
        label='Data Inicial',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        input_formats=('%Y-%m-%d',),
    )
    data_fim = forms.DateField(
        label='Data Final',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        input_formats=('%Y-%m-%d',),
    )
    data_saida_presencial = forms.DateField(
        label='Data Saída Presencial',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        input_formats=('%Y-%m-%d',),
    )
    hora_inicio = forms.TimeField(
        label='Hora de Chegada',
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control'
            }),
    )
    hora_saida_presencial = forms.TimeField(
        label='Hora de Saída',
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control'
            }),
    )

    class Meta:
        model = EscalaResponsavel
        fields = '__all__'
        exclude = ('qt_dias_presenciais', 'qt_horas_presentes')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        usuario = Usuario.objects.filter(user=user).first()
        familia = usuario.familia
        queryset_responsavel_presencial = Responsavel.objects.filter(familia=familia)
        queryset_responsavel_monitoramento = Responsavel.objects.filter(familia=familia)
        self.fields['responsavel_presencial'].queryset = queryset_responsavel_presencial
        self.fields['responsavel_monitoramento'].queryset = queryset_responsavel_monitoramento
