from rest_framework import serializers
from django.core.validators import RegexValidator

from .models import *
from .utils import PayStackRequestHelper


class InitiateSendPaymentSerializer(serializers.Serializer):
    """Initiate payment serializer."""

    phone_regex = RegexValidator(regex=r'^\d{10,14}$',
                                 message="Phone number must be between 10 to 14 digits.")

    email = serializers.EmailField()
    name = serializers.CharField(max_length=30)
    amount = serializers.IntegerField(min_value=1000)
    phone_number = serializers.CharField(max_length=14, validators=[phone_regex])


class ResolveBankSerializer(serializers.Serializer):

    bank_code = serializers.CharField(max_length=6)
    account_number = serializers.CharField(max_length=10, min_length=10)


class BankAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, data):
        account_number = data.get("account_number")
        bank = data.get("bank_code")
        res = PayStackRequestHelper.resolve_account_number(account_number, bank)
        if not res['status']:
            raise serializers.ValidationError('Could not verify bank account')
        return data

