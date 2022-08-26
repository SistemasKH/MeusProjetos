import decimal
from datetime import date, timedelta

from django import forms

from backend.crm.models import Cuidador, Dependente, Responsavel, Usuario

from .models import (
    Consulta,
    EscalaResponsavel,
    Glicose,
    JornadaTrabalho,
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

        consulta_pk = request.path.split('/')[-2]
        consulta = Consulta.objects.filter(pk=consulta_pk)
        #self.fields['consulta'].queryset = consulta

        #consulta = Consulta.objects.filter(pk=self.instance.consulta.pk)
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
            instance.media = self.calcula_taxa_media_mensal_de_glicose(instance)  # noqa E501
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

    def conta_dias(self, instance):
        dias = ((instance.data_saida_presencial) - (instance.data_inicio))
        instance.qt_dias_presenciais = dias.days
        return dias.days

    def conta_horas(self, instance):
        inicio = instance.hora_inicio
        hora_em_minutos_inicio = (inicio.hour) * 60
        minutos_inicio = inicio.minute
        inicio_min = hora_em_minutos_inicio + minutos_inicio
        saida = instance.hora_saida_presencial
        hora_em_minutos_saida = (saida.hour) * 60
        minutos_saida = saida.minute
        saida_min = hora_em_minutos_saida + minutos_saida
        dia_minutos = 1440
        min_primeiro_dia = (dia_minutos - inicio_min)
        min_ultimo_dia = saida_min
        total_horas = (min_primeiro_dia + min_ultimo_dia) / 60
        dias = self.conta_dias(instance)
        horas = (((dias - 2) * 24) + total_horas)
        instance.qt_horas_presentes = horas
        print('salvando')
        return horas

    def save(self, commit=True):
        instance = super().save(commit=False)
        self.conta_dias(instance)
        self.conta_horas(instance)

        if commit:
            instance.save()
        return instance


class JornadaTrabalhoForm(forms.ModelForm):
    required_css_class = 'required'

    dh_entrada = forms.DateTimeField(
        label='Entrada',
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        input_formats=('%Y-%m-%dT%H:%M',),
    )
    dh_saida = forms.DateTimeField(
        label='Saída',
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        input_formats=('%Y-%m-%dT%H:%M',),
    )

    class Meta:
        model = JornadaTrabalho
        fields = '__all__'
        exclude = ('horas_trabalhadas_diaria', 'soma_horas_semanal', 'soma_horas_mensal')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        usuario = Usuario.objects.filter(user=user).first()
        familia = usuario.familia
        queryset_responsavel_dia = Responsavel.objects.filter(familia=familia)
        queryset_cuidador = Cuidador.objects.filter(familia=familia)
        self.fields['responsavel_dia'].queryset = queryset_responsavel_dia
        self.fields['cuidador'].queryset = queryset_cuidador

    def conta_horas(self, instance):
        inicio = instance.dh_entrada
        saida = instance.dh_saida
        duracao = saida - inicio
        instance.horas_trabalhadas_diaria = duracao
        return instance.horas_trabalhadas_diaria

    def soma_horas_semanal(self):
        return

    def soma_horas_mensal(self):
        return

    def save(self, commit=True):
        instance = super().save(commit=False)
        self.conta_horas(instance)
        if commit:
            instance.save()
        return instance
