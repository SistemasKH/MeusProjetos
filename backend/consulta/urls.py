from django.urls import include, path

from backend.consulta import views as v

consulta_urlpatterns = [
    path('', v.ConsultaListView.as_view(), name='consulta_list'),  # noqa E501
    path('<int:pk>/', v.ConsultaDetailView.as_view(), name='consulta_detail'),  # noqa E501
    path('add/', v.ConsultaCreateView.as_view(), name='consulta_add'),  # noqa E501
    path('<int:pk>/edit/', v.ConsultaUpdateView.as_view(), name='consulta_edit'),  # noqa E501
    path('<int:pk>/delete/', v.consulta_delete, name='consulta_delete'),  # noqa E501
]

posconsulta_urlpatterns = [
    path('', v.PosConsultaListView.as_view(), name='posconsulta_list'),  # noqa E501
    path('<int:pk>/', v.PosConsultaDetailView.as_view(), name='posconsulta_detail'),  # noqa E501
    path('add/<int:consulta_pk>/', v.PosConsultaCreateView.as_view(), name='posconsulta_add'),  # noqa E501
    path('<int:pk>/edit/', v.pos_consulta_update, name='posconsulta_edit'),  # noqa E501
    path('<int:pk>/delete/', v.posconsulta_delete, name='posconsulta_delete'),  # noqa E501
    path('<int:pos_consulta_pk>/receita-add/', v.receita_add_form, name='receita_add_form')  # noqa E501
]

receita_urlpatterns = [
    path('<int:pk>/delete/', v.receita_delete, name='receita_delete')  # noqa E501
]

medicamento_urlpatterns = [
    path('', v.MedicamentoListView.as_view(), name='medicamento_list'),  # noqa E501
    path('<int:pk>/', v.MedicamentoDetailView.as_view(), name='medicamento_detail'),  # noqa E501
    path('add/', v.MedicamentoCreateView.as_view(), name='medicamento_add'),  # noqa E501
    path('<int:pk>/edit/', v.MedicamentoUpdateView.as_view(), name='medicamento_edit'),  # noqa E501
    path('<int:pk>/delete/', v.medicamento_delete, name='medicamento_delete'),  # noqa E501
]

glicose_urlpatterns = [
    path('', v.GlicoseListView.as_view(), name='glicose_list'),  # noqa E501
    path('<int:pk>/', v.GlicoseDetailView.as_view(), name='glicose_detail'),  # noqa E501
    path('add/', v.GlicoseCreateView.as_view(), name='glicose_add'),  # noqa E501
    path('<int:pk>/edit/', v.GlicoseUpdateView.as_view(), name='glicose_edit'),  # noqa E501
    path('<int:pk>/delete/', v.glicose_delete, name='glicose_delete'),  # noqa E501
]

escalaresp_urlpatterns = [
    path('', v.EscalaResponsavelListView.as_view(), name='escalaresponsavel_list'),  # noqa E501
    path('<int:pk>/', v.EscalaResponsavelDetailView.as_view(), name='escalaresponsavel_detail'),  # noqa E501
    path('add/', v.EscalaResponsavelCreateView.as_view(), name='escalaresponsavel_add'),  # noqa E501
    path('<int:pk>/edit/', v.EscalaResponsavelUpdateView.as_view(), name='escalaresponsavel_edit'),  # noqa E501
    path('<int:pk>/delete/', v.escalaresponsavel_delete, name='escalaresponsavel_delete'),  # noqa E501
]

jornadatrabalho_urlpatterns = [
    path('', v.JornadaTrabalhoListView.as_view(), name='jornadatrabalho_list'),  # noqa E501
    path('<int:pk>/', v.JornadaTrabalhoDetailView.as_view(), name='jornadatrabalho_detail'),  # noqa E501
    path('add/', v.JornadaTrabalhoCreateView.as_view(), name='jornadatrabalho_add'),  # noqa E501
    path('<int:pk>/edit/', v.JornadaTrabalhoUpdateView.as_view(), name='jornadatrabalho_edit'),  # noqa E501
    path('<int:pk>/delete/', v.jornadatrabalho_delete, name='jornadatrabalho_delete'),  # noqa E501
]

urlpatterns = [
    path('consulta/', include(consulta_urlpatterns)),
    path('posconsulta/', include(posconsulta_urlpatterns)),
    path('receita/', include(receita_urlpatterns)),
    path('medicamento/', include(medicamento_urlpatterns)),
    path('glicose/', include(glicose_urlpatterns)),
    path('escalaresp/', include(escalaresp_urlpatterns)),
    path('jornadatrabalho/', include(jornadatrabalho_urlpatterns)),
]
