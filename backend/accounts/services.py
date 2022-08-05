from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from backend.core.services import add_permissions
from backend.crm.models import Responsavel

from .tokens import account_activation_token


def responsavel_principal_create(form, user):
    # Define username igual email.
    email = form.cleaned_data.pop('email')
    user.username = email

    user.save()

    # Adiciona ao grupo 'responsavel_principal'.
    group = Group.objects.get(name='responsavel_principal')
    user.groups.add(group)

    # Cria o Responsavel.
    Responsavel.objects.create(user=user)

    # Como é o Responsavel principal,
    # adiciona a permissão can_add_familia.
    add_permissions('responsavel_principal', ['add_familia'])


def send_mail_to_user(request, user):
    current_site = get_current_site(request)
    use_https = request.is_secure()
    subject = 'Ative sua conta.'
    message = render_to_string('email/account_activation_email.html', {
        'user': user,
        'protocol': 'https' if use_https else 'http',
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)
