from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from backend.consulta.forms import DependentesDaFamiliaForm
from backend.core.mixins import PermissaoFamiliaMixin

from .forms import ContasBancariasForm, CreditoForm
from .models import Comprovante, ContasBancarias, Credito


class ContasBancariasListView(LRM, PermissaoFamiliaMixin, ListView):
    model = ContasBancarias

    def get_queryset(self):
        dependente = self.request.GET.get('titular_dependente')

        if dependente:
            queryset = ContasBancarias.objects.filter(titular_dependente=dependente)  # noqa E501
            return queryset

        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        queryset = ContasBancarias.objects.filter(titular_dependente__familia__nome=familia)  # noqa E501
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['form'] = DependentesDaFamiliaForm(user)
        context['labels'] = (
            'Abertura',
            'Banco',
            'Nome',
            'Agência',
            'Cidade',
            'Tipo',
            'Conta',
            'Titular',
            'Conjunta',
            'Inicial',
            'Atual',
            'Encerramento',
        )
        return context


class ContasBancariasDetailView(LRM, PermissaoFamiliaMixin, DetailView):
    model = ContasBancarias


class ContasBancariasCreateView(LRM, CreateView):
    model = ContasBancarias
    form_class = ContasBancariasForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ContasBancariasUpdateView(LRM, UpdateView):
    model = ContasBancarias
    form_class = ContasBancariasForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


def contas_bancarias_delete(request, pk):
    obj = get_object_or_404(ContasBancarias, pk=pk)
    obj.delete()
    msg = 'Excluído com sucesso!'
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('contasbancarias_list')


class CreditoListView(LRM, PermissaoFamiliaMixin, ListView):
    model = Credito

    def get_queryset(self):
        conta_credito = self.request.GET.get('conta_credito')

        if conta_credito:
            queryset = ContasBancarias.objects.filter(conta=conta_credito)  # noqa E501
            return queryset

        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        queryset = Credito.objects.filter(responsavel_lancamento__familia__nome=familia)  # noqa E501
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['labels'] = (
            'Entrada',
            'Referência',
            'Depositante',
            'Valor',
            'Conta',
            'Responsavel',

        )
        return context


class CreditoDetailView(LRM, PermissaoFamiliaMixin, DetailView):
    model = Credito


class CreditoCreateView(LRM, CreateView):
    model = Credito
    form_class = CreditoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        credito = self.object
        comprovantes = self.request.FILES.getlist('comprovante')

        for comprovante in comprovantes:
            Comprovante.objects.create(
                credito=credito,
                comprovante=comprovante
            )

        return super().form_valid(form)


class CreditoUpdateView(LRM, UpdateView):
    model = Credito
    form_class = CreditoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        credito = self.object
        comprovantes = self.request.FILES.getlist('comprovante')

        for comprovante in comprovantes:
            Comprovante.objects.update(
                credito=credito,
                comprovante=comprovante
            )

        return super().form_valid(form)


def credito_delete(request, pk):
    obj = get_object_or_404(Credito, pk=pk)
    obj.delete()

    msg = 'Excluído com sucesso!'
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('credito_list')
