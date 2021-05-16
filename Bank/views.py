from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

from Bank.models import TransactionHistory,AccountDetails
from Bank.serializers import UserCreationSerializer,BankAccountCreationSerializer,DepositSerializer,WithdrawSerializer,TransactionSerializer,LoginSerializer

from rest_framework.views import APIView
from rest_framework import generics,status,mixins,permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

class UserRegisterMixin(generics.GenericAPIView,mixins.CreateModelMixin):
    serializer_class = UserCreationSerializer
    def post(self,request):
        return self.create(request)

class UserLoginApi(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            # user=authenticate(request,username=username,password=password
            user = User.objects.get(username=username)
            if(user.username==username)&(user.password==password):
                login(request,user)
                token,created = Token.objects.get_or_create(user=user)
                return Response({"token":token.key},status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class AccountCreationApi(generics.GenericAPIView,mixins.CreateModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BankAccountCreationSerializer
    def get(self,request):
        account_num = AccountDetails.objects.last()
        if account_num:
            account_num = account_num.account_num + 1
        else:
            account_num = 1000
        return Response({"account_num":account_num})
    def post(self,request):
        return self.create(request)

class BalanceApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BankAccountCreationSerializer
    def get(self, request, account_num):
        account_num = AccountDetails.objects.get(account_num=account_num)
        if account_num:
            return Response({"message":"Account Number :" + str(account_num.account_num) + "your Balance is" + str(account_num.balance)})
        else:
            return Response({"Warning : Invalid account Number" + str(account_num)})

class WithdrawApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,account_num):
        serializer = WithdrawSerializer(data=request.data)
        account_num = AccountDetails.objects.get(account_num=account_num)
        if serializer.is_valid():
            amount = serializer.validated_data.get("amount")
            if amount<account_num.balance:
                account_num.balance-=amount
                account_num.save()
                return Response({"message":"withdrawn successfully, Your account balance is "+ str(account_num.balance)})
            else:
                return Response({"message":"no sufficient balance"})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DepositApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,account_num):
        serializer = DepositSerializer(data=request.data)
        account_num = AccountDetails.objects.get(account_num=account_num)
        if serializer.is_valid():
            amount = serializer.validated_data.get("amount")
            account_num.balance+=amount
            account_num.save()
            return Response({"message":"Deposit successfull, Balance is"+str(account_num.balance)})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogoutApi(APIView):
    def get(self,request):
        logout(request)
        # request.user.auth_token.delete()
        return Response({"message":"user logged out"})

class TransactionApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,account_num):
        from_acno_obj= AccountDetails.objects.get(account_num=account_num)
        debit_transaction = TransactionHistory.objects.filter(account_num=from_acno_obj)
        # print(debit_transaction)
        credit_transaction = TransactionHistory.objects.filter(to_acno=account_num)
        # print(credit_transaction)
        serializer1 = TransactionSerializer(debit_transaction,many=True)
        serializer2 = TransactionSerializer(credit_transaction,many=True)
        return Response({"Debit Transaction":serializer1.data,"Credit Transaction":serializer2.data},status=status.HTTP_200_OK)
    def post(self,request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            from_acno = serializer.validated_data.get("account_num")
            to_acno = serializer.validated_data.get("to_acno")
            amount = serializer.validated_data.get("amount")
            from_acno_obj = AccountDetails.objects.get(account_num=from_acno)
            to_acno_obj = AccountDetails.objects.get(account_num=to_acno)
            if amount<=(from_acno_obj.balance):
                serializer.save()
                from_acno_obj.balance-=amount
                to_acno_obj.balance+=amount
                from_acno_obj.save()
                to_acno_obj.save()
                return Response({"message":str(amount) + "has been sent to account number" +str(to_acno)})
            else:
                return Response({"No Sufficient Balance"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




