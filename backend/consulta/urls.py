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
    path('<int:pk>/edit/', v.PosConsultaUpdateView.as_view(), name='posconsulta_edit'),  # noqa E501
    path('<int:pk>/delete/', v.posconsulta_delete, name='posconsulta_delete'),  # noqa E501
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
    path('', v.EscalaRespListView.as_view(), name='escalaresp_list'),  # noqa E501
    path('<int:pk>/', v.EscalaRespDetailView.as_view(), name='escalaresp_detail'),  # noqa E501
    path('add/', v.EscalaRespCreateView.as_view(), name='escalaresp_add'),  # noqa E501
    path('<int:pk>/edit/', v.EscalaRespUpdateView.as_view(), name='escalaresp_edit'),  # noqa E501
    path('<int:pk>/delete/', v.escalaresp_delete, name='escalaresp_delete'),  # noqa E501

]

urlpatterns = [
    path('consulta/', include(consulta_urlpatterns)),
    path('posconsulta/', include(posconsulta_urlpatterns)),
    path('medicamento/', include(medicamento_urlpatterns)),
    path('glicose/', include(glicose_urlpatterns)),
    path('escalaresp/', include(escalaresp_urlpatterns)),
]
