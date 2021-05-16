from django.urls import path
from Bank.views import UserLoginApi,UserRegisterMixin,UserLogoutApi,AccountCreationApi,BalanceApi,WithdrawApi,DepositApi,TransactionApi

urlpatterns = [
    path("register",UserRegisterMixin.as_view()),
    path("login",UserLoginApi.as_view()),
    path("logout",UserLogoutApi.as_view()),
    path("create_account",AccountCreationApi.as_view()),
    path("balance/<int:account_num>",BalanceApi.as_view()),
    path("withdraw/<int:account_num>",WithdrawApi.as_view()),
    path("deposit/<int:account_num>",DepositApi.as_view()),
    path("sendmoney",TransactionApi.as_view()),
    path("transaction/<int:account_num>",TransactionApi.as_view())
]
