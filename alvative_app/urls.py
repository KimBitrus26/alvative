from django.urls import path

from .views import (InitiateSendPaymentView, VerifyPaymentView, ResolveBankAccountView, GetBankListView,
                    BankAaccountView, WebhookView)

urlpatterns = [
    path("", InitiateSendPaymentView.as_view(), name="send_payment"),
    path("api/v1/verify-payment/<str:ref_code>/", VerifyPaymentView.as_view(), name="verify_payment"),
    path("api/v1/get-bank-list/", GetBankListView.as_view(), name="get_bank_list"),
    path("api/v1/resolve-bank-account/", ResolveBankAccountView.as_view(), name="resolve_bank_account"),
    path("api/v1/create-bank/", BankAaccountView.as_view(), name="create_bank"),
    path('webhook/', WebhookView.as_view(), name='process_webhook'),
   
]
