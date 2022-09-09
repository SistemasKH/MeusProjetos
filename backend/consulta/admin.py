from django.contrib import admin

from .models import (
    Consulta,
    EscalaResponsavel,
    Glicose,
    Medicamento,
    PosConsulta
)


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'dependente',
        'data_consulta',
        'hora',
        'especialidade',
    )
    # list_display_links = ('dependente',)
    # search_fields = ('name',)
    # list_filter = ('type',)
    # date_hierarchy = 'created'


@admin.register(PosConsulta)
class PosConsultaAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'consulta',
    )
    # list_display_links = ('dependente',)
    # search_fields = ('name',)
    # list_filter = ('type',)
    # date_hierarchy = 'created'


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )
    # list_display_links = ('dependente',)
    search_fields = ('medicamento_prescrito',)
    # list_filter = ('type',)
    # date_hierarchy = 'created'


@admin.register(Glicose)
class GlicoseAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'data_medicao',
        'hora',
        'taxa_glicose',
        'estado_alimentar',
        'tipo_insulina',
        'qt_insulina',
    )
    # list_display_links = ('dependente',)
    search_fields = ('hora',)
    # list_filter = ('type',)
    # date_hierarchy = 'created'


@admin.register(EscalaResponsavel)
class EscalaResponsavelAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'responsavel_presencial',
        'data_inicio',
        'hora_inicio',
        'data_saida_presencial',
        'qt_dias_presenciais',
        'hora_saida_presencial',
        'qt_horas_presentes',
        'responsavel_monitoramento',
        'data_fim',
    )
