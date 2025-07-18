from django.contrib import admin
from .models import (
    Company, Bank, CompAccount, FiscalYear,
    LiabilityName, LiabilityDisposePriority,
    LiabilityType, MainLiability,
    CreditorDebitor, Transaction, MyUser
)


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_admin')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_admin')
    list_per_page = 25
    ordering = ('email',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner_name", "phone_number", "email", "is_active")
    search_fields = ("name", "owner_name")
    list_filter = ("is_active",)

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "branch_name", "bank_code", "branch_code", "is_active")
    search_fields = ("name", "branch_name")
    list_filter = ("is_active",)

@admin.register(CompAccount)
class CompAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "account_no", "bank", "is_active", "is_default")
    search_fields = ("account_no",)
    list_filter = ("is_active", "is_default")

@admin.register(FiscalYear)
class FiscalYearAdmin(admin.ModelAdmin):
    list_display = ("id", "year", "is_active")
    list_filter = ("is_active",)

@admin.register(LiabilityName)
class LiabilityNameAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")
    list_filter = ("is_active",)

@admin.register(LiabilityDisposePriority)
class LiabilityDisposePriorityAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)

@admin.register(LiabilityType)
class LiabilityTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")
    list_filter = ("is_active",)

@admin.register(MainLiability)
class MainLiabilityAdmin(admin.ModelAdmin):
    list_display = ("id", "company_name", "liability_name", "amount", "fiscal_year", "date", "is_active")
    list_filter = ("fiscal_year", "liability_type", "dispose_priority", "is_active")
    search_fields = ("company_name", "liability_name")

@admin.register(CreditorDebitor)
class CreditorDebitorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "account_title", "account_no", "bank_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "account_no")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "account_title", "transaction_type", "mode_of_payment", "amount", "fiscal_year", "transaction_date", "is_active")
    list_filter = ("transaction_type", "mode_of_payment", "fiscal_year", "is_active")
    search_fields = ("account_no", "transaction_no")
