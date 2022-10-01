from django.contrib import admin

from .models import Comprovante, ContasBancarias, Credito


@admin.register(ContasBancarias)
class ContasBancariasAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',

    )
    # list_display_links = ('dependente',)
    search_fields = ('nome_banco',)
    # list_filter = ('type',)
    # date_hierarchy = 'created'


@admin.register(Credito)
class CreditoAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',

    )
    # list_display_links = ('dependente',)
    search_fields = ('referencia',)
    # list_filter = ('type',)
    # date_hierarchy = 'created'


class ComprovanteInline(admin.TabularInline):
    model = Comprovante
    extra = 0
