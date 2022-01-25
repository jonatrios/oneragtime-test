from django.contrib import admin
from .models import Upfront, Membership, YearlyFees

# Register your models here.
class UpfrontAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'investment',
        'upfront_fee_amount',
        'created_at',
        'updated_at',
    )
    ordering = ['id']


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'investor', 'membership_amount', 'year_of_membership')
    ordering = ['id']


class YearlyFeesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'investment',
        'description',
        'fee_amount',
        'invoice_expire_date',
        'created_at',
        'updated_at',
    )
    ordering = ['id']


admin.site.register(Upfront, UpfrontAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(YearlyFees, YearlyFeesAdmin)
