from django.urls import path
from Utilisateurs import views as user_views
from . import views

urlpatterns = [
    # Authentification
    path("connecter/", user_views.Connecter_Compte, name="login"),
    path("creation/", user_views.Creation_Compte, name="creation"),
    path("deconnection/", user_views.Deconnection, name="deconnection"),

    # Messagerie
    path('send_message/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path("message/<int:message_id>/", user_views.read_message, name="read_message"),
    path("message/delete/<int:message_id>/", user_views.delete_message, name="delete_message"),

    # Notifications
    path('notifications/', user_views.notifications_view, name='notifications'),
    path('notifications/mark-as-read/<int:notif_id>/', user_views.mark_as_read, name='mark_as_read'),

    # Notification rapide
    path('notify/', user_views.notify_user, name='notify_user'),
]
