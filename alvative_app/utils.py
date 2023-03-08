
import datetime
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Transaction


class Helper:

    @staticmethod
    def reference_generator():
        return "rr_" + datetime.datetime.now().strftime("%m%d%y%H%M%S") + User.objects.make_random_password(length=10, allowed_chars="abcdefghijklmnopqrstuvwxyz1234567890")
   
class PayStackRequestHelper:
    AUTHORIZED_HEADER = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + settings.PAYSTACK_SECRET_KEY
    }
    BASE_URL = "https://api.paystack.co/"
    INITIALIZE_TRANSACTION_URL = BASE_URL + "transaction/initialize/"
    VERIFY_TRANSACTION_URL = BASE_URL + "transaction/verify/"
    RESOLVE_ACCOUNT_NUMBER = BASE_URL + "bank/resolve"
    BANKS = BASE_URL + "bank?currency=NGN"
    
    @staticmethod
    def send_payment(request, reference, email, amount_in_kobo, name, phone_number,):
        tx_data = {
            "reference": reference,
            "email": email,
            "amount": amount_in_kobo,
            "callback_url": request.build_absolute_uri(reverse('verify_payment', kwargs={'ref_code': reference})),
            "metadata": {
                "name": name,
                "phone_number": phone_number,
            }
        }
        res = requests.post(PayStackRequestHelper.INITIALIZE_TRANSACTION_URL,
                            headers=PayStackRequestHelper.AUTHORIZED_HEADER, json=tx_data)
        res_data = res.json()

        if res_data['status']:
            Transaction.objects.create(ref=reference, amount=amount_in_kobo, email=email, name=name)
            return res_data
        else:
            return None

    @staticmethod
    def get_bank_code(bank_name):

        res = requests.get(PayStackRequestHelper.BANKS, headers=PayStackRequestHelper.AUTHORIZED_HEADER)
        result = res.json()
        bank_code, found = None, False
        for bank in result.get("data"):
            if bank["name"] == bank_name.title():
                bank_code = bank["code"]
                found = True
                break
            else:
                found = False
                bank_code = None
        return {
            "found": found,
            "bank_code": bank_code
        }

    @staticmethod
    def resolve_account_number(account_number, bank_code):
        url = f"{PayStackRequestHelper.RESOLVE_ACCOUNT_NUMBER}?account_number={account_number}&bank_code={bank_code}"
        res = requests.get(url, headers=PayStackRequestHelper.AUTHORIZED_HEADER)
        result = res.json()
        return result

    @staticmethod
    def get_bank_list():
        url = f"{PayStackRequestHelper.BANKS}"
        res = requests.get(url, headers=PayStackRequestHelper.AUTHORIZED_HEADER)
        result = res.json()
        return result
