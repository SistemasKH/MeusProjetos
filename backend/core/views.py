from urllib import request

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import render

from backend.crm.models import Usuario


@login_required
def home(request):
    user = request.user
    usuario = Usuario.objects.filter(user=user).first()
    context = {}

    if usuario:
        #messages.add_message(request, constants.SUCCESS, 'Você entrou no sistema!')
        context = {'familia': usuario.familia}

        if usuario.familia == None:
            messages.add_message(request, constants.WARNING, 'Cadastre sua familia')

    return render(request, 'home.html', context)


def tables(request):
    template_name = 'quem_somos.html'
    return render(request, template_name)
