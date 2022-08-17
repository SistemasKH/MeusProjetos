from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from backend.accounts.services import send_mail_to_user
from backend.core.services import has_group

from .forms import (
    CuidadorAddForm,
    CuidadorUpdateForm,
    DependenteAddForm,
    DependenteUpdateForm,
    FamiliaForm,
    ResponsavelAddForm,
    ResponsavelUpdateForm
)
from .models import Cuidador, Dependente, Familia, Responsavel
from .services import (
    add_to_group_cuidador,
    add_to_group_dependente,
    add_to_group_responsavel,
    user_create
)


def financeiro(request):
    return render(request, 'crm/financeiro.html')


class DependenteListView(LRM, ListView):
    model = Dependente

    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user.usuarios.first()
        familia = usuario.familia

        if not familia:
            message = 'Favor cadastrar a sua família!'
            messages.error(request, message)
            return redirect('familia_list')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        queryset = Dependente.objects.filter(familia__nome=familia, active=True)  # noqa E501
        return queryset

    def get_context_data(self, **kwargs):
        '''
        Verifica se já existe uma família.
        '''
        context = super().get_context_data(**kwargs)
        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        if familia:
            context['minha_familia'] = True
        else:
            context['minha_familia'] = False

        context['labels'] = (
            'Nome',
            'Data nascimento',
            'Cidade',
            'Telefone',
            'Nome do Convênio',
            'Contato do Convênio',
            'Ativo',
        )
        return context


class DependenteDetailView(LRM, DetailView):
    model = Dependente


class DependenteCreateView(LRM, CreateView):
    model = Dependente
    form_class = DependenteAddForm

    def form_valid(self, form):
        # # Cria o User.
        # user = user_create(form)

        self.object = form.save(commit=False)

        # # Associa o User ao Dependente
        # self.object.user = user

        # Adiciona o Dependente ao grupo 'dependente'.
        # add_to_group_dependente(form, user)

        # Associa a Familia.
        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        self.object.familia = familia
        self.object.save()

        return super().form_valid(form)


class DependenteUpdateView(LRM, UpdateView):
    model = Dependente
    form_class = DependenteUpdateForm


@login_required
def dependente_delete(request, pk):
    obj = get_object_or_404(Dependente, pk=pk)
    obj.active = False
    obj.save()
    return redirect('dependente_list')


class FamiliaListView(LRM, ListView):
    model = Familia

    def get_queryset(self):
        queryset = super().get_queryset()
        usuario = self.request.user.usuarios.first()
        if usuario:
            familia = usuario.familia
            queryset = Familia.objects.filter(nome=familia, active=True)

        return queryset

    def get_context_data(self, **kwargs):
        '''
        Verifica se já existe uma família.
        '''
        context = super().get_context_data(**kwargs)
        usuario = self.request.user.usuarios.first()
        if usuario:
            familia = usuario.familia
            if familia:
                context['minha_familia'] = True
            else:
                context['minha_familia'] = False

        context['labels'] = (
            'Nome',
            'Endereço',
            'Bairro',
            'Cidade',
            'UF',
            'Ativo',
        )
        return context


class FamiliaDetailView(LRM, DetailView):
    model = Familia


class FamiliaCreateView(LRM, CreateView):
    model = Familia
    form_class = FamiliaForm

    def form_valid(self, form):
        # Pega o objeto Responsavel.
        user = self.request.user
        responsavel = Responsavel.objects.get(user=user)

        # Verifica se já existe uma família.
        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        if familia:
            return redirect('familia_list')

        self.object = form.save()

        # Associa o Responsavel a Família.
        responsavel.familia = self.object
        responsavel.save()
        return super().form_valid(form)


class FamiliaUpdateView(LRM, UpdateView):
    model = Familia
    form_class = FamiliaForm


@login_required
def familia_delete(request, pk):
    obj = get_object_or_404(Familia, pk=pk)
    obj.active = False
    obj.save()
    return redirect('familia_list')


class ResponsavelListView(LRM, ListView):
    model = Responsavel

    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user.usuarios.first()
        familia = usuario.familia

        if not familia:
            message = 'Favor cadastrar a sua família!'
            messages.error(request, message)
            return redirect('familia_list')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        usuario = self.request.user.usuarios.first()
        if usuario:
            familia = usuario.familia
            queryset = Responsavel.objects.filter(familia__nome=familia, active=True)  # noqa E501
        else:
            queryset = Responsavel.objects.filter(active=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = (
            'Nome',
            'Dta_Nasc.',
            'Cidade',
            'Cel_Whats',
            'Parentesco',
            'Ativo',
        )
        return context


class ResponsavelDetailView(LRM, DetailView):
    model = Responsavel


class ResponsavelCreateView(LRM, CreateView):
    model = Responsavel
    form_class = ResponsavelAddForm

    def form_valid(self, form):
        # Cria o User.
        user = user_create(form)

        self.object = form.save(commit=False)

        # Associa o User ao Responsavel
        self.object.user = user

        # Adiciona o Responsavel ao grupo 'responsavel'.
        add_to_group_responsavel(form, user)

        # Associa a Familia.
        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        self.object.familia = familia
        self.object.save()

        # Envia e-mail para o Responsável.
        send_mail_to_user(request=self.request, user=user)

        return super().form_valid(form)


class ResponsavelUpdateView(LRM, UpdateView):
    model = Responsavel
    form_class = ResponsavelUpdateForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not has_group(request.user, 'responsavel_principal') and request.user.email != obj.user.email:  # noqa E501
            message = 'Você não tem permissão para editar este registro.'
            messages.error(request, message)
            return redirect('responsavel_list')
        return super(ResponsavelUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


@login_required
def responsavel_delete(request, pk):
    obj = get_object_or_404(Responsavel, pk=pk)
    obj.active = False
    obj.save()
    return redirect('responsavel_list')


class CuidadorListView(LRM, ListView):
    model = Cuidador

    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user.usuarios.first()
        familia = usuario.familia

        if not familia:
            message = 'Favor cadastrar a sua família!'
            messages.error(request, message)
            return redirect('familia_list')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        queryset = Cuidador.objects.filter(familia__nome=familia, active=True)  # noqa E501
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = (
            'Nome',
            'Dta_Nasc.',
            'Cidade',
            'Cel_Whats',
            'Carga_Hr',
            'Turno',
            'Dta_Pag.',
            'Ativo',
        )
        return context


class CuidadorDetailView(LRM, DetailView):
    model = Cuidador


class CuidadorCreateView(LRM, CreateView):
    model = Cuidador
    form_class = CuidadorAddForm

    def form_valid(self, form):
        # Cria o User.
        user = user_create(form)

        self.object = form.save(commit=False)

        # Associa o User ao Cuidador
        self.object.user = user

        # Adiciona o Cuidador ao grupo 'cuidador'.
        add_to_group_cuidador(form, user)

        # Associa a Familia.
        usuario = self.request.user.usuarios.first()
        familia = usuario.familia
        self.object.familia = familia
        self.object.save()

        # Envia e-mail para o Cuidador.
        send_mail_to_user(request=self.request, user=user)

        return super().form_valid(form)


class CuidadorUpdateView(LRM, UpdateView):
    model = Cuidador
    form_class = CuidadorUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


@login_required
def cuidador_delete(request, pk):
    obj = get_object_or_404(Cuidador, pk=pk)
    obj.active = False
    obj.save()
    return redirect('cuidador_list')
