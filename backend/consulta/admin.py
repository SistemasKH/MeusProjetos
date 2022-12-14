from django.contrib import admin

from .models import (
    Consulta,
    EscalaResponsavel,
    Exame,
    Glicose,
    JornadaTrabalho,
    Medicamento,
    PosConsulta,
    Receita
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


class ReceitaInline(admin.TabularInline):
    model = Receita
    extra = 0


class ExameInline(admin.TabularInline):
    model = Exame
    extra = 0


@admin.register(PosConsulta)
class PosConsultaAdmin(admin.ModelAdmin):
    inlines = (ReceitaInline, ExameInline)
    list_display = (
        '__str__',
        'consulta',
    )


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',

    )
    search_fields = ('medicamento_prescrito',)


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


@admin.register(JornadaTrabalho)
class JornadaTrabalhoAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'cuidador',
        'dh_entrada',
        'dh_saida',
        'horas_trabalhadas_diaria',
        'soma_horas_semanal',
        'soma_horas_mensal',
    )
