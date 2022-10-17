from django.urls import include, path

from backend.financeiro import views as v

contabancaria_urlpatterns = [
    path('', v.ContaBancariaListView.as_view(), name='contabancaria_list'),  # noqa E501
    path('<int:pk>/', v.ContaBancariaDetailView.as_view(), name='contabancaria_detail'),  # noqa E501
    path('add/', v.ContaBancariaCreateView.as_view(), name='contabancaria_add'),  # noqa E501
    path('<int:pk>/edit/', v.ContaBancariaUpdateView.as_view(), name='contabancaria_edit'),  # noqa E501
    path('<int:pk>/delete/', v.conta_bancaria_delete, name='conta_bancaria_delete'),  # noqa E501
]

credito_urlpatterns = [
    path('', v.CreditoListView.as_view(), name='credito_list'),  # noqa E501
    path('<int:pk>/', v.CreditoDetailView.as_view(), name='credito_detail'),  # noqa E501
    path('add/', v.CreditoCreateView.as_view(), name='credito_add'),  # noqa E501
    path('<int:pk>/edit/', v.credito_update, name='credito_edit'),  # noqa E501
    path('<int:pk>/delete/', v.credito_delete, name='credito_delete'),  # noqa E501
    path('<int:credito_pk>/comprovante-add/', v.comprovante_add_form, name='comprovante_add_form'),  # noqa E501
]

comprovante_urlpatterns = [
    path('<int:pk>/delete/', v.comprovante_delete, name='comprovante_delete'),  # noqa E501
]

despesa_urlpatterns = [
    path('', v.DespesaListView.as_view(), name='despesa_list'),  # noqa E501
    path('<int:pk>/', v.DespesaDetailView.as_view(), name='despesa_detail'),  # noqa E501
    path('add/', v.DespesaCreateView.as_view(), name='despesa_add'),  # noqa E501
    path('<int:pk>/edit/', v.despesa_update, name='despesa_edit'),  # noqa E501
    path('<int:pk>/delete/', v.despesa_delete, name='despesa_delete'),  # noqa E501
    path('<int:despesa_pk>/comprovante_despesa-add/', v.comprovante_despesa_add_form, name='comprovante_despesa_add_form'),  # noqa E501
]
comprovante_despesa_urlpatterns = [
    path('<int:pk>/delete/', v.comprovante_despesa_delete, name='comprovante_despesa_delete'),  # noqa E501
]


urlpatterns = [
    path('contabancaria/', include(contabancaria_urlpatterns)),
    path('credito/', include(credito_urlpatterns)),
    path('comprovante/', include(comprovante_urlpatterns)),
    path('despesa/', include(despesa_urlpatterns)),
    path('comprovante_despesa/', include(comprovante_despesa_urlpatterns)),

]
