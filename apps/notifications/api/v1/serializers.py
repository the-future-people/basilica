from rest_framework import serializers
from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'priority', 'channel',
            'title', 'message',
            'bin', 'trip', 'payment',
            'is_read', 'read_at', 'is_sent', 'sent_at',
            'created_at'
        ]
        read_only_fields = ['id', 'is_sent', 'sent_at', 'created_at']