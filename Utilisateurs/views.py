from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message, Notification
import re

def Creation_Compte(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')  # ✅ Récupération de l'adresse e-mail
        password = request.POST.get('password1')
        password_confirm = request.POST.get('password2')

        # ✅ Vérif mots de passe identiques
        if password != password_confirm:
            messages.error(request, "Les mots de passe ne sont pas identiques. Veuillez réessayer.")
            return redirect("creation")

        # ✅ Vérif complexité du mot de passe
        if (
            len(password) < 8
            or not re.search(r'[A-Za-z]', password)
            or not re.search(r'\d', password)
            or not re.search(r'[!@#$%(),.?":{}|<>]', password)
        ):
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères, incluant des lettres, des chiffres et des caractères spéciaux.")
            return redirect("creation")

        # ✅ Vérif utilisateur existant
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà. Veuillez réessayer.")
            return redirect("creation")

        # ✅ Vérif si l’adresse e-mail existe déjà
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse e-mail est déjà utilisée. Veuillez en choisir une autre.")
            return redirect("creation")

        # ✅ Vérif email valide
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Veuillez entrer une adresse e-mail valide.")
            return redirect("creation")

        # ✅ Création du compte
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Compte créé avec succès. Connectez-vous maintenant.")
        return redirect("login")

    # Cas GET → on affiche le formulaire
    return render(request, "creation.html")




def Connecter_Compte(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('acc')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return redirect("login")
    
    # Si c’est un GET, on affiche simplement le formulaire de connexion
    return render(request, 'login.html')


def Deconnection(request):

    logout(request)
    return redirect("login")

def notifications_view(request):
    notifications = Notification.objects.all().order_by('-date')  # dernières en premier
    return render(request, 'Utilisateurs/notifications.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('notifications')

@login_required
def notify_user(request):
    Notification.objects.create(
        user=request.user,
        message="Action réussie !",
        is_read=False
    )
    return redirect("notifications")

def Acc(request):
    unread_count = 0
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    return render(request, "zone_gauche.html", {
        "unread_count": unread_count
    })





@login_required
def send_message(request):
    if request.method == "POST":
        destinataire = request.POST.get("recipient")
        subject = request.POST.get("subject")
        content = request.POST.get("body")

        Message.objects.create(
            sender=request.user,
            destinataire=destinataire,
            subject=subject,
            content=content
        )

        messages.success(request, "Message envoyé !")
        return redirect('inbox')

    return render(request, "send_message.html")








@login_required
def inbox(request):
    user = request.user.username  # récupère le username de l'utilisateur connecté

    # Messages reçus : où le destinataire est l'utilisateur connecté
    messages_recus = Message.objects.filter(destinataire=user).order_by('-timestamp')

    # Messages envoyés : où l'expéditeur est l'utilisateur connecté
    messages_envoyes = Message.objects.filter(sender=request.user).order_by('-timestamp')

    return render(request, 'inbox.html', {
        'messages_recus': messages_recus,
        'messages_envoyes': messages_envoyes
    })




@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    # Autoriser la suppression si l’utilisateur est l’expéditeur ou le destinataire
    if request.user == message.sender or request.user.username == message.destinataire:
        message.delete()
        messages.success(request, "Message supprimé avec succès.")
    else:
        messages.error(request, "Vous n'avez pas l'autorisation de supprimer ce message.")

    return redirect('inbox')








@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.is_read = True
    message.save()
    return render(request, 'view_message.html', {'message': message})



@login_required
def read_message(request, message_id):
    try:
        # Chercher le message par id, et vérifier que l'utilisateur est soit le destinataire soit l'expéditeur
        msg = Message.objects.get(id=message_id)
        if msg.destinataire != request.user.username and msg.sender.username != request.user.username:
            raise Message.DoesNotExist
    except Message.DoesNotExist:
        # Retourne un 404 si l'utilisateur n'a pas le droit de voir ce message
        raise Http404("Ce message n'existe pas ou vous n'avez pas accès.")
    
    # Marquer comme lu si l'utilisateur est le destinataire
    if msg.destinataire == request.user.username and not msg.is_read:
        msg.is_read = True
        msg.save()

    return render(request, 'read_message.html', {'msg': msg})





   

