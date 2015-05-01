from django.contrib import admin
from models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Transaction, TransactionAdmin)


# Register your models here.
