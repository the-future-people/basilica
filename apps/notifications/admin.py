from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['notification_type', 'priority', 'channel', 'recipient', 'title', 'is_read', 'is_sent', 'created_at']
    list_filter = ['notification_type', 'priority', 'channel', 'is_read', 'is_sent']
    search_fields = ['recipient__username', 'title', 'message']
    readonly_fields = ['id', 'created_at', 'read_at', 'sent_at']

    fieldsets = (
        ('Recipient', {
            'fields': ('id', 'recipient')
        }),
        ('Notification', {
            'fields': ('notification_type', 'priority', 'channel', 'title', 'message')
        }),
        ('Linked Objects', {
            'fields': ('bin', 'trip', 'payment'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'read_at', 'is_sent', 'sent_at', 'failure_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )