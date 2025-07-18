from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    ntn = models.CharField(max_length=50, null=True, blank=True)
    strn = models.CharField(max_length=50, null=True, blank=True)
    logo = models.BinaryField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Bank(models.Model):
    id = models.DecimalField(max_digits=18, decimal_places=0, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    bank_code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=25)
    branch_name = models.CharField(max_length=150)
    is_active = models.BooleanField()
    created_date = models.DateTimeField(null=True, blank=True)

class CompAccount(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account_no = models.CharField(max_length=25)
    account_title = models.CharField(max_length=255, default='')
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    opening_balance = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    is_active = models.BooleanField()
    is_default = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)

class FiscalYear(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class LiabilityName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

class LiabilityDisposePriority(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class LiabilityType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

class MainLiability(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    datetime = models.DateTimeField(auto_now_add=True)
    liability_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    liability_type = models.CharField(max_length=100)
    dispose_priority = models.CharField(max_length=100)
    remarks = models.CharField(max_length=250, null=True, blank=True)
    fiscal_year = models.CharField(max_length=15, default='2025-2026')
    is_active = models.BooleanField(default=True)

class CreditorDebitor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    account_title = models.CharField(max_length=255)
    account_no = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Transaction(models.Model):
    MODE_CHOICES = [
        ('online', 'Online'),
        ('atm', 'ATM'),
        ('cheque', 'Cheque'),
        ('cash', 'Cash'),
    ]

    TYPE_CHOICES = [
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    ]

    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_no = models.CharField(max_length=25)
    account_title = models.CharField(max_length=255)
    transaction_date = models.DateTimeField(default=timezone.now)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    mode_of_payment = models.CharField(max_length=10, choices=MODE_CHOICES, default='online')
    transaction_no = models.CharField(max_length=50)
    transaction_remarks = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    fiscal_year = models.CharField(max_length=15, default='2025-2026')
    creditor_debitor = models.ForeignKey(CreditorDebitor, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
