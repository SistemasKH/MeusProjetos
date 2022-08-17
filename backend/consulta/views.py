from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from backend.core.mixins import PermissaoFamiliaMixin

from .forms import (
    ConsultaForm,
    DependentesDaFamiliaForm,
    EscalaResponsavelForm,
    GlicoseForm,
    MedicamentoForm,
    PosConsultaForm
)
from .models import (
    Consulta,
    EscalaResponsavel,
    Glicose,
    Medicamento,
    PosConsulta
)


class ConsultaListView(LRM, PermissaoFamiliaMixin, ListView):
    model = Consulta

    def get_queryset(self):
        dependente = self.request.GET.get('dependente')

        if dependente:
            queryset = Consulta.objects.filter(dependente=dependente)  # noqa E501
            return queryset

        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        queryset = Consulta.objects.filter(dependente__familia__nome=familia)  # noqa E501
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['form'] = DependentesDaFamiliaForm(user)
        context['labels'] = (
            'Data',
            'Hora',
            'Dependente',
            'Especialidade',
            'Médico(a)',
            'Acompanhante',
            'Cancelamento',
            'Pós_Consulta',
        )
        return context


class ConsultaDetailView(LRM, PermissaoFamiliaMixin, DetailView):
    model = Consulta


class ConsultaCreateView(LRM, CreateView):
    model = Consulta
    form_class = ConsultaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ConsultaUpdateView(LRM, UpdateView):
    model = Consulta
    form_class = ConsultaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


def consulta_delete(request):
    ...


class PosConsultaListView(LRM, PermissaoFamiliaMixin, ListView):
    model = PosConsulta

    def get_queryset(self):
        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        queryset = PosConsulta.objects.filter(acompanhante_responsavel__familia__nome=familia)  # noqa E501
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = (
            'Consulta',
            'Data',
            'Hora',
            'Especialidade',
            'Médico',
            'Acompanhante',
            'Diagnóstico',

        )
        return context


class PosConsultaDetailView(LRM, PermissaoFamiliaMixin, DetailView):
    model = PosConsulta


class PosConsultaCreateView(LRM, CreateView):
    model = PosConsulta
    form_class = PosConsultaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
            'request': self.request
        })
        return kwargs


class PosConsultaUpdateView(LRM, UpdateView):
    model = PosConsulta
    form_class = PosConsultaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
            'request': self.request
        })
        return kwargs


def posconsulta_delete(request):
    ...


class MedicamentoListView(LRM, PermissaoFamiliaMixin, ListView):
    model = Medicamento

    def get_queryset(self):
        dependente = self.request.GET.get('dependente')

        if dependente:
            queryset = Medicamento.objects.filter(dependente=dependente)  # noqa E501
            return queryset

        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        queryset = Medicamento.objects.filter(dependente__familia__nome=familia)  # noqa E501
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['form'] = DependentesDaFamiliaForm(user)
        context['labels'] = (
            'Dependente',
            'Medicamento',
            'Substância',
            'Indicações',
            'Dosagem',
            'Inicio',
            'Fim',
            'Medico',
            'Fornecedor',
        )
        return context


class MedicamentoDetailView(LRM, PermissaoFamiliaMixin, DetailView):
    model = Medicamento


class MedicamentoCreateView(LRM, CreateView):
    model = Medicamento
    form_class = MedicamentoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class MedicamentoUpdateView(LRM, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


@login_required
def medicamento_delete(request, pk):
    obj = get_object_or_404(Medicamento, pk=pk)
    obj.delete()
    return redirect('medicamento_list')


class GlicoseListView(LRM, PermissaoFamiliaMixin, ListView):
    model = Glicose

    def get_queryset(self):
        dependente = self.request.GET.get('dependente')

        if dependente:
            queryset = Glicose.objects.filter(dependente=dependente)  # noqa E501
            return queryset

        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        queryset = Glicose.objects.filter(dependente__familia__nome=familia)  # noqa E501
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['form'] = DependentesDaFamiliaForm(user)
        context['labels'] = (
            'Dependente',
            'Data',
            'Hora',
            'Período',
            'Taxa',
            'M_Diária',
            'Cuidador',
            'Responsável',
        )
        return context


class GlicoseDetailView(LRM, PermissaoFamiliaMixin, DetailView):
    model = Glicose


class GlicoseCreateView(LRM, CreateView):
    model = Glicose
    form_class = GlicoseForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class GlicoseUpdateView(LRM, UpdateView):
    model = Glicose
    form_class = GlicoseForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


@login_required
def glicose_delete(request, pk):
    obj = get_object_or_404(Glicose, pk=pk)
    obj.delete()
    return redirect('glicose_list')


class EscalaResponsavelListView(LRM, PermissaoFamiliaMixin, ListView):
    model = EscalaResponsavel

    def get_queryset(self):
        responsavel_presencial = self.request.GET.get('responsavel')
        responsavel_monitoramento = self.request.GET.get('responsavel')

        if responsavel_presencial:
            queryset = EscalaResponsavel.objects.filter(responsavel_presencial=responsavel)  # noqa E501
            return queryset

        if responsavel_monitoramento:
            queryset = EscalaResponsavel.objects.filter(responsavel_monitoramento=responsavel)  # noqa E501
            return queryset

        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        queryset = EscalaResponsavel.objects.filter(
            responsavel_presencial__familia__nome=familia,
            responsavel_monitoramento__familia__nome=familia
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = (
            'Dta+Início',
            'Hr_Início',
            'Resp_Presencial',
            'Dta_Saída ',
            'Hr_Saida',
            'Carga_hr',
            'Resp_Monit.',
            'Dta_Fim',
        )
        return context


class EscalaResponsavelDetailView(LRM, PermissaoFamiliaMixin, DetailView):
    model = EscalaResponsavel


class EscalaResponsavelCreateView(LRM, CreateView):
    model = EscalaResponsavel
    form_class = EscalaResponsavelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class EscalaResponsavelUpdateView(LRM, UpdateView):
    model = EscalaResponsavel
    form_class = EscalaResponsavelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


@login_required
def escalaresponsavel_delete(request, pk):
    obj = get_object_or_404(Glicose, pk=pk)
    obj.delete()
    return redirect('escalaresponsavel_list')
