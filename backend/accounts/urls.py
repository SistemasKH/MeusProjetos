from django.contrib.auth.views import LogoutView
from django.urls import path

from backend.accounts import views as v

urlpatterns = [
    # path('login/', v.CustomLoginView.as_view(), name='login'),  # noqa E501
    path('login/', v.custom_login, name='login'),  # noqa E501
    path('logout/', LogoutView.as_view(), name='logout'),  # noqa E501
    path('responsavel/principal/add/', v.responsavel_principal_add, name='responsavel_principal_add'),   # noqa E501
    path('reset/<uidb64>/<token>/', v.MyPasswordResetConfirm.as_view(), name='password_reset_confirm'),  # noqa E501
    path('reset/done/', v.MyPasswordResetComplete.as_view(), name='password_reset_complete'),  # noqa E501
]
