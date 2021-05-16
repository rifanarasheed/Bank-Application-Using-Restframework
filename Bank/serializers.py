from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from Bank.models import  TransactionHistory,AccountDetails

class UserCreationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name","last_name","username","password"]

class BankAccountCreationSerializer(ModelSerializer):
    class Meta:
        model = AccountDetails
        fields = "__all__"

class WithdrawSerializer(serializers.Serializer):
    amount = serializers.IntegerField()

class DepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField()

class TransactionSerializer(serializers.Serializer):
    account_num = serializers.CharField()
    to_acno = serializers.IntegerField()
    amount = serializers.IntegerField()
    date = serializers.DateField()
    def create(self, validated_data):
        account_num = validated_data["account_num"]
        acnt_obj = AccountDetails.objects.get(account_num = account_num)
        validated_data["account_num"] = acnt_obj
        return TransactionHistory.objects.create(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
