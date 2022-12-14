from django.contrib import admin

from .models import (
    Comprovante,
    ComprovanteDespesa,
    ContaBancaria,
    Credito,
    Despesa
)


@admin.register(ContaBancaria)
class ContaBancariaAdmin(admin.ModelAdmin):
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


@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',

    )
    # list_display_links = ('dependente',)
    search_fields = ('referencia',)
    # list_filter = ('type',)
    # date_hierarchy = 'created'


class ComprovanteDespesaInline(admin.TabularInline):
    model = ComprovanteDespesa
    extra = 0
