from rest_framework import serializers
from apps.billing.models import Subscription, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'subscription', 'amount', 'payment_type',
            'payment_method', 'momo_number', 'momo_transaction_id',
            'momo_network', 'status', 'failure_reason',
            'billing_period_start', 'billing_period_end',
            'initiated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'initiated_at', 'completed_at', 'momo_transaction_id']


class SubscriptionSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    total_monthly_charge = serializers.ReadOnlyField()
    bin_serial = serializers.CharField(source='bin.serial_number', read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id', 'customer_name', 'customer_type',
            'phone_number', 'email', 'address',
            'bin', 'bin_serial',
            'monthly_fee', 'bin_contribution', 'total_monthly_charge',
            'status', 'billing_day', 'next_billing_date',
            'started_at', 'cancelled_at',
            'payments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SubscriptionListSerializer(serializers.ModelSerializer):
    total_monthly_charge = serializers.ReadOnlyField()
    bin_serial = serializers.CharField(source='bin.serial_number', read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id', 'customer_name', 'customer_type',
            'phone_number', 'bin_serial', 'status',
            'total_monthly_charge', 'next_billing_date'
        ]