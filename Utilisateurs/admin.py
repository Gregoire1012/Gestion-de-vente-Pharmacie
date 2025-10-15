from django.contrib import admin
from .models import Message, Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'date', 'is_read')  # utilise le vrai champ
    list_filter = ('is_read',)  # pareil
    search_fields = ('message', 'user__username')  # facultatif, pour rechercher
    ordering = ('-date',)



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'destinataire', 'subject', 'content', 'timestamp', 'is_read')
    list_filter = ('timestamp', 'is_read')
    search_fields = ('content', 'subject', 'destinataire', 'sender__username')