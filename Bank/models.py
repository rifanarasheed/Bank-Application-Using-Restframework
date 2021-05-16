from django.db import models

# Create your models here.
class AccountDetails(models.Model):
    account_num = models.IntegerField(unique=True)
    user_name = models.CharField(max_length=120,unique=True)
    balance = models.IntegerField(default=0)
    account_type = models.CharField(max_length=100)
    def __str__(self):
        return str(self.account_num)

class TransactionHistory(models.Model):
    account_num = models.ForeignKey(AccountDetails,on_delete=models.CASCADE)
    to_acno = models.IntegerField()
    amount = models.IntegerField()
    date = models.DateField(auto_now=True)
    def __str__(self):
        return str(self.account_num)