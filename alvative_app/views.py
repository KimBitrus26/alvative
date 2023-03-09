import hashlib
import hmac
import requests
import json

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .utils import Helper, PayStackRequestHelper
from .serializers import (InitiateSendPaymentSerializer, ResolveBankSerializer, BankAccountSerializer)
from .models import (Transaction, DumpPaystackData)


class InitiateSendPaymentView(APIView):
    """View to initiate paystack transaction"""

    serializer_class = InitiateSendPaymentSerializer

    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data

            reference = Helper.reference_generator()

            email = data["email"]
            name = data["name"]
            amount = data["amount"]
            phone_number = data["phone_number"]

            amount_in_kobo = int(amount) * 100
            
            res = PayStackRequestHelper.send_payment(request, reference, email, amount_in_kobo, name, phone_number, )
         
            return Response({"status": "success", "data": res}, status=status.HTTP_200_OK)


class VerifyPaymentView(APIView):
    """View to verify paystack transaction"""

    permission_classes = (AllowAny,)

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        transaction = get_object_or_404(Transaction, ref=kwargs["ref_code"])

        if not transaction.verified:
            res = requests.get(
                f"{PayStackRequestHelper.VERIFY_TRANSACTION_URL}{transaction.ref}",
                headers=PayStackRequestHelper.AUTHORIZED_HEADER
            ).json()

            if res["status"] and res["data"]["status"] == "success" \
                    and res["data"]["currency"] == "NGN" and res["data"]["amount"] == transaction.amount:
                transaction.verify()
                return Response({"status": "Payment verified successfully"},
                        status=status.HTTP_200_OK)
            else:
                return Response("Payment Failed", status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "Transaction already verified"},
                        status=status.HTTP_400_BAD_REQUEST)


class GetBankListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        banks = PayStackRequestHelper.get_bank_list()
        banks_names_and_codes = map(lambda bank: {
            "name": bank["name"],
            "code": bank["code"]
        }, banks["data"])
        return Response({"status": "Success", "data": banks_names_and_codes},
                        status=status.HTTP_200_OK)


class ResolveBankAccountView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResolveBankSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            bank_code = data["bank_code"]
            account_number = data["account_number"]

            res = PayStackRequestHelper.resolve_account_number(account_number, bank_code)
            if res["status"]:
                response = {
                    "status": "Account resolved successfully",
                    "data": res['data']
                }
            else:
                return Response({
                    "status": "Account not found",
                }, status=status.HTTP_404_NOT_FOUND)

            return Response(response, status=status.HTTP_200_OK)


class BankAaccountView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = BankAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "Success", "data":  serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"status": "Failde"}, status=status.HTTP_400_BAD_REQUEST)
    
class WebhookView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        json_body = json.loads(request.body)

        computed_hmac = hmac.new(
            bytes(settings.PAYSTACK_SEC_KEY, 'utf-8'),
            str.encode(request.body.decode('utf-8')),
            digestmod=hashlib.sha512
        ).hexdigest()

        if 'HTTP_X_PAYSTACK_SIGNATURE' in request.META:
            if request.META['HTTP_X_PAYSTACK_SIGNATURE'] == computed_hmac:
                if json_body['event'] == 'charge.success':
                    json_data = json_body['data']
                    DumpPaystackData.objects.create(dump_data=json_data)   
                    return Response(status=200)
            return Response(status=400)
        else:
            return Response(status=400)
