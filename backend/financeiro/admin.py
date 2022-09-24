from django.contrib import admin
from .models import ContasBancarias

@admin.register(ContasBancarias)
class ContasBancariasAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',

    )
    # list_display_links = ('dependente',)
    search_fields = ('nome_banco',)
    # list_filter = ('type',)
    # date_hierarchy = 'created'