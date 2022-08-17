from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy


class PermissaoFamiliaMixin:

    def dispatch(self, request, *args, **kwargs):
        usuario = self.request.user.usuarios.first()
        familia = usuario.familia

        if not familia:
            message = 'Favor cadastrar a sua família!'
            messages.error(request, message)
            # return redirect('familia_list')
            return HttpResponseRedirect(reverse_lazy('familia_list'))
        return super().dispatch(request, *args, **kwargs)
