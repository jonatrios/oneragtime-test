from django.contrib import admin
from .models import Investor, Investment, FeePercentage

# Register your models here.
class InvestorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'company_name',
        'created_at',
        'updated_at',
        'is_active',
        'email',
    )
    ordering = ['id']


class InvestmetAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'investment_amount',
        'date_of_investment',
        'invoice_expiring_date',
        'investor',
        'fee_percentage',
        'in_years',
        'pay_upfront'
    )
    ordering = ['id']

class FeePercentageAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'fee_value', 'created_at', 'updated_at')
    ordering = ['id']

admin.site.register(Investor, InvestorAdmin)
admin.site.register(Investment, InvestmetAdmin)
admin.site.register(FeePercentage, FeePercentageAdmin)