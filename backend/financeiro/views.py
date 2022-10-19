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
    ComprovanteDespesaAddForm,
    ComprovantesDespesaFormset,
    ComprovantesFormset,
    ContaBancariaForm,
    CreditoForm,
    CreditoUpdateForm,
    DespesaForm,
    DespesaUpdateForm
)
from .models import Comprovante, ContaBancaria, Credito, Despesa, ComprovanteDespesa


class ContaBancariaListView(LRM, PermissaoFamiliaMixin, ListView):
    model = ContaBancaria

    def get_queryset(self):
        dependente = self.request.GET.get('titular_dependente')

        if dependente:
            queryset = ContaBancaria.objects.filter(titular_dependente=dependente)  # noqa E501
            return queryset

        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        queryset = ContaBancaria.objects.filter(titular_dependente__familia__nome=familia)  # noqa E501
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
            'Saldo Inicial RS',
            'Saldo Atual RS',

        )
        return context


class ContaBancariaDetailView(LRM, PermissaoFamiliaMixin, DetailView):
    model = ContaBancaria


class ContaBancariaCreateView(LRM, CreateView):
    model = ContaBancaria
    form_class = ContaBancariaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ContaBancariaUpdateView(LRM, UpdateView):
    model = ContaBancaria
    form_class = ContaBancariaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


def conta_bancaria_delete(request, pk):
    obj = get_object_or_404(ContaBancaria, pk=pk)
    obj.delete()
    msg = 'Excluído com sucesso!'
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('contabancaria_list')


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
            'Dta Entrada',
            'Conta',
            'Referência',
            'Depositante',
            'Valor R$',
            'Saldo Atual R$',
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

        # Salva os comprovantes
        for comprovante in comprovantes:
            Comprovante.objects.create(
                credito=credito,
                comprovante=comprovante
            )

        # Atualiza o saldo atual
        conta_bancaria = ContaBancaria.objects.get(pk=self.object.conta_credito.pk)
        if conta_bancaria.saldo_atual == 0:
            self.object.saldo_atual = conta_bancaria.saldo_inicial + self.object.valor
            conta_bancaria.saldo_atual = self.object.saldo_atual
            conta_bancaria.save()
        else:
            self.object.saldo_atual = conta_bancaria.saldo_atual + self.object.valor
            conta_bancaria.saldo_atual = self.object.saldo_atual
            conta_bancaria.save()
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


class DespesaListView(LRM, PermissaoFamiliaMixin, ListView):
    model = Despesa

    def get_queryset(self):
        conta_bancaria = self.request.GET.get('conta_bancária')

        if conta_bancaria:
            queryset = ContasBancarias.objects.filter(conta=conta_bancaria)  # noqa E501
            return queryset

        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        queryset = Despesa.objects.filter(responsavel_lancamento__familia__nome=familia)  # noqa E501
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = (
            'Conta',
            'Dta Saída',
            'Forma de Pagamento',
            'Referência',
            'Credor',
            'Valor R$',
            'Saldo Atual R$',
            'Responsavel'

        )
        return context


class DespesaDetailView(LRM, PermissaoFamiliaMixin, DetailView):
    model = Despesa


class DespesaCreateView(LRM, CreateView):
    model = Despesa
    form_class = DespesaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        despesa = self.object
        comprovantes = self.request.FILES.getlist('comprovante')

        for comprovante in comprovantes:
            ComprovanteDespesa.objects.create(
                despesa=despesa,
                comprovante=comprovante
            )
       # Atualiza o saldo atual
        conta_bancaria = ContaBancaria.objects.get(pk=self.object.conta_bancaria.pk)
        if conta_bancaria.saldo_atual == 0:
           self.object.saldo_atual = conta_bancaria.saldo_inicial - self.object.valor
           conta_bancaria.saldo_atual = self.object.saldo_atual
           conta_bancaria.save()
        else:
           self.object.saldo_atual = conta_bancaria.saldo_atual - self.object.valor
           conta_bancaria.saldo_atual = self.object.saldo_atual
           conta_bancaria.save()
        return super().form_valid(form)


@login_required
def despesa_update(request, pk):
    '''
    Edita os dados da Despesa.
    '''
    template_name = 'financeiro/despesa_update_form.html'
    instance = get_object_or_404(Despesa, pk=pk)

    # Edita os dados da despesa.
    form = DespesaUpdateForm(request.POST or None, instance=instance, prefix='main')
    # Edita as imagens dos Comprovantes.
    formset_comprovante_despesa = ComprovantesDespesaFormset(request.POST or None, instance=instance, prefix='items')

    if request.method == 'POST':
        if form.is_valid() and formset_comprovante_despesa.is_valid():
            form.save()

            # Salva os Comprovantes
            novos_comprovantes = [item[1] for item in request.FILES.items()]

            dados_do_formset_comprovante_despesa = formset_comprovante_despesa.cleaned_data

            for item in zip(novos_comprovantes, dados_do_formset_comprovante_despesa):
                comprovante_antigo = item[1]['id']
                comprovante_novo = item[0]
                comprovante_antigo.comprovante = comprovante_novo
                comprovante_antigo.save()  # O comprovante antigo é atualizado para o novo.

            return redirect('despesa_detail', pk=instance.pk)

    context = {
        'object': instance,
        'form': form,
        'formset_comprovante_despesa': formset_comprovante_despesa,
    }
    return render(request, template_name, context)


@login_required
def despesa_delete(request, pk):
    obj = get_object_or_404(Despesa, pk=pk)
    obj.delete()
    msg = 'Excluído com sucesso!'
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('despesa_list')


def comprovante_despesa_add_form(request, despesa_pk):
    '''
    Adiciona um formulário de Comprovantes no modal para inserir Comprovantes em Despesa.
    Método acionado via hx-get em debito_update_form.html para alimentar comprovanteAddModal.
    '''
    template_name = 'financeiro/hx/comprovante_despesa_form_hx.html'
    form = ComprovanteDespesaAddForm(despesa_pk, request.POST or None)

    if request.method == 'POST':
        despesa = Despesa.objects.get(pk=despesa_pk)
        comprovantes = request.FILES.getlist('comprovante')

        for comprovante in comprovantes:
            ComprovanteDespesa.objects.create(
                despesa=despesa,
                comprovante=comprovante
            )

        return redirect('despesa_edit', pk=despesa.pk)

    context = {'form': form}
    return render(request, template_name, context)


@login_required
def comprovante_despesa_delete(request, pk):
    obj = get_object_or_404(ComprovanteDespesa, pk=pk)
    obj.delete()
    msg = 'Excluído com sucesso!'
    messages.add_message(request, messages.SUCCESS, msg)
    return HttpResponse('')
