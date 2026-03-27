from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Subscription, Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ['id', 'initiated_at', 'completed_at', 'momo_transaction_id']
    fields = ['payment_type', 'payment_method', 'amount', 'status', 'momo_number', 'initiated_at']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_type', 'bin', 'monthly_fee', 'bin_contribution', 'total_monthly_charge', 'status', 'next_billing_date']
    list_filter = ['status', 'customer_type', 'billing_day']
    search_fields = ['customer_name', 'phone_number', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [PaymentInline]

    fieldsets = (
        ('Customer Info', {
            'fields': ('id', 'customer_name', 'customer_type', 'phone_number', 'email', 'address')
        }),
        ('Bin', {
            'fields': ('bin',)
        }),
        ('Pricing', {
            'fields': ('monthly_fee', 'bin_contribution')
        }),
        ('Billing', {
            'fields': ('status', 'billing_day', 'next_billing_date', 'started_at', 'cancelled_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['subscription', 'payment_type', 'payment_method', 'amount', 'status', 'initiated_at', 'completed_at']
    list_filter = ['status', 'payment_type', 'payment_method']
    search_fields = ['subscription__customer_name', 'momo_transaction_id', 'momo_number']
    readonly_fields = ['id', 'initiated_at', 'completed_at']

    fieldsets = (
        ('Payment Info', {
            'fields': ('id', 'subscription', 'payment_type', 'payment_method', 'amount')
        }),
        ('Mobile Money', {
            'fields': ('momo_number', 'momo_transaction_id', 'momo_network'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'failure_reason')
        }),
        ('Billing Period', {
            'fields': ('billing_period_start', 'billing_period_end')
        }),
        ('Timestamps', {
            'fields': ('initiated_at', 'completed_at'),
        }),
    )