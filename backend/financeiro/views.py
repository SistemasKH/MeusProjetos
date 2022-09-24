from .forms import ContasBancariasForm
from .models import ContasBancarias
from backend.consulta.forms import DependentesDaFamiliaForm
from backend.crm.models import Dependente, Responsavel
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect, render, resolve_url
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.shortcuts import get_object_or_404, redirect, render
from backend.core.mixins import PermissaoFamiliaMixin



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
    obj.active = False
    obj.save()
    msg = 'Excluído com sucesso!'
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('contasbancarias_list')

