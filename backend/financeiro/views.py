from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from backend.consulta.forms import DependentesDaFamiliaForm
from backend.core.mixins import PermissaoFamiliaMixin

from .forms import (
    ComprovanteAddForm,
    ComprovantesFormset,
    ContasBancariasForm,
    CreditoForm,
    CreditoUpdateForm
)
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


@login_required
def credito_update(request, pk):
    '''
    Edita os dados de crédito.
    '''
    template_name = 'financeiro/credito_update_form.html'
    instance = get_object_or_404(Credito, pk=pk)

    # Edita os dados de crédito.
    form = CreditoUpdateForm(request.POST or None, instance=instance, prefix='main')
    # Edita as imagens dos Comprovantes.
    formset_comprovante = ComprovantesFormset(request.POST or None, instance=instance, prefix='items')

    if request.method == 'POST':
        if form.is_valid() and formset_comprovante.is_valid():
            form.save()

            # Salva os Comprovantes
            novos_comprovantes = [item[1] for item in request.FILES.items()]

            dados_do_formset_comprovante = formset_comprovante.cleaned_data

            for item in zip(novos_comprovantes, dados_do_formset_comprovante):
                comprovante_antigo = item[1]['id']
                comprovante_novo = item[0]
                comprovante_antigo.comprovante = comprovante_novo
                comprovante_antigo.save()  # O comprovante antigo é atualizado para o novo.

            return redirect('credito_detail', pk=instance.pk)

    context = {
        'object': instance,
        'form': form,
        'formset_comprovante': formset_comprovante,
    }
    return render(request, template_name, context)


@login_required
def credito_delete(request, pk):
    obj = get_object_or_404(Credito, pk=pk)
    obj.delete()

    msg = 'Excluído com sucesso!'
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('credito_list')


def comprovante_add_form(request, credito_pk):
    '''
    Adiciona um formulário de Comprovantes no modal para inserir Comprovantes em Credito.
    Método acionado via hx-get em credito_update_form.html para alimentar comprovanteAddModal.
    '''
    template_name = 'financeiro/hx/comprovante_form_hx.html'
    form = ComprovanteAddForm(credito_pk, request.POST or None)

    if request.method == 'POST':
        credito = Credito.objects.get(pk=credito_pk)
        comprovantes = request.FILES.getlist('comprovante')

        for comprovante in comprovantes:
            Comprovante.objects.create(
                credito=credito,
                comprovante=comprovante
            )

        return redirect('credito_edit', pk=credito.pk)

    context = {'form': form}
    return render(request, template_name, context)


@login_required
def comprovante_delete(request, pk):
    obj = get_object_or_404(Comprovante, pk=pk)
    obj.delete()
    msg = 'Excluído com sucesso!'
    messages.add_message(request, messages.SUCCESS, msg)
    return HttpResponse('')
