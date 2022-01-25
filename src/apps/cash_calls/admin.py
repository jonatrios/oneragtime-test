from django.contrib import admin
from .models import Bills

# Register your models here.
class BillsAdmin(admin.ModelAdmin):
    ordering = ['id']


admin.site.register(Bills, BillsAdmin)
