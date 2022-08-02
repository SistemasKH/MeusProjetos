from datetime import date

from django import forms

from backend.crm.models import Cuidador, Dependente, Responsavel, Usuario

from .models import (
    Consulta,
    EscalaResponsaveis,
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
        # self.fields['data_consulta'].widget.attrs.update({'class': 'mask-date'})   # noqa E501
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

        # pega o penúltimo item da lista
        # sendo que a lista é ex:
        # '/consulta/posconsulta/add/3/'
        # request.path.split('/')
        # ['', 'consulta', 'posconsulta', 'add', '3', '']
        # ou seja, nesse caso retorna o número 3.
        consulta_pk = request.path.split('/')[-2]
        consulta = Consulta.objects.filter(pk=consulta_pk)
        self.fields['consulta'].queryset = consulta

        acompanhante_responsavel = consulta.first().acompanhante_responsavel
        queryset = Responsavel.objects.filter(pk=acompanhante_responsavel.pk)  # noqa E501
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

        # self.fields['data_inicio'].widget.attrs.update({'class': 'mask-date'})
        # self.fields['data_fim'].widget.attrs.update({'class': 'mask-date'})


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

    def calcula_taxa_media_de_glicose(self, instance):
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
            instance.media_diaria = self.calcula_taxa_media_de_glicose(instance)  # noqa E501
            instance.save()
        return instance


class EscalaRespForm(forms.ModelForm):
    required_css_class = 'required'

    data_inicial = forms.DateField(
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
    hora_inicio = forms.TimeField(
        label='Hora Combinada',
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control'
            }),
    )

    class Meta:
        model = EscalaResponsaveis
        fields = '__all__'

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        usuario = Usuario.objects.filter(user=user).first()
        familia = usuario.familia
        queryset_responsavel = Responsavel.objects.filter(familia=familia)
        self.fields['responsavel'].queryset = queryset_responsavel
