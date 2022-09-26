from django.urls import include, path

from backend.financeiro import views as v


contasbancarias_urlpatterns = [
    path('', v.ContasBancariasListView.as_view(), name='contasbancarias_list'),  # noqa E501
    path('<int:pk>/', v.ContasBancariasDetailView.as_view(), name='contasbancarias_detail'),  # noqa E501
    path('add/', v.ContasBancariasCreateView.as_view(), name='contasbancarias_add'),  # noqa E501
    path('<int:pk>/edit/', v.ContasBancariasUpdateView.as_view(), name='contasbancarias_edit'),  # noqa E501
    path('<int:pk>/delete/', v.contas_bancarias_delete, name='contas_bancarias_delete'),  # noqa E501

]

credito_urlpatterns = [
    path('', v.CreditoListView.as_view(), name='credito_list'),  # noqa E501
    path('<int:pk>/', v.CreditoDetailView.as_view(), name='credito_detail'),  # noqa E501
    path('add/', v.CreditoCreateView.as_view(), name='credito_add'),  # noqa E501
    path('<int:pk>/edit/', v.CreditoUpdateView.as_view(), name='credito_edit'),  # noqa E501
    path('<int:pk>/delete/', v.credito_delete, name='credito_delete'),  # noqa E501

]

urlpatterns = [
    path('contasbancarias/', include(contasbancarias_urlpatterns)),
    path('credito/', include(credito_urlpatterns)),

]