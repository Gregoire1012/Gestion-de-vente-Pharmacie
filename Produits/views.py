from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AjoutVente, AjoutProduit 
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Func, IntegerField

from django.views.generic import ListView
from django.contrib import messages
from datetime import datetime
from .models import *

from .forms import AjoutProduit, AjoutVente
from .models import Vente
from django.utils import timezone
from .models import Produit, Vente, Customer  # bien importer le modèle correct


from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
import json


from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User





# Classe d’affichage
class Affichage(ListView):
    template_name = 'home.html'
    queryset = Produits.objects.all()

# Fonction d’ajout des données
def ajout_donnees(request):
    errors = {}

    if request.method == 'POST':
        name = request.POST.get('name')
        price_str = request.POST.get('price')
        quantite = request.POST.get('quantite')
        date_expiration_str = request.POST.get('date_expiration')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # Validation de la date
        try: 
            date_expiration = datetime.strptime(date_expiration_str, '%Y-%m-%d')
        except (ValueError, TypeError):
            errors['date_expiration'] = "Le format de la date n'est pas bon (AAAA-MM-JJ)."

        # Validation du prix
        try:
            price = float(price_str)
            if price < 0:
                errors['price'] = "Le prix ne peut pas être négatif."
        except (ValueError, TypeError):
            errors['price'] = "Entrez un prix valide svp."

        # Si aucune erreur
        if not errors:
            try:
                category = Categories.objects.get(pk=request.POST.get('category'))
                savedonnes = Produits(
                    name=name,
                    price=price,
                    quantite=quantite,
                    description=description,
                    date_expiration=date_expiration,
                    category=category,
                    image=image
                )
                savedonnes.save()
                messages.success(request, "✅ Le produit a été ajouté avec succès.")
                return redirect('home')

            except Categories.DoesNotExist:
                errors['category'] = "La catégorie spécifiée est introuvable."
            except KeyError as e:
                errors[str(e)] = f"Le champ {e} est manquant dans la requête."
            except Exception as e:
                messages.error(request, f"❌ Une erreur est survenue: {e}")
                return redirect('home')

    else:  # Si GET
        category = Categories.objects.all()
        return render(request, "ajout-donnees.html", {"category": category})

    # Si erreurs, renvoyer le formulaire avec messages
    category = Categories.objects.all()
    return render(request, "ajout-donnees.html", {"category": category, "errors": errors})

# Fonction de détail produit (attention, cette fonction est maintenant **hors** de ajout_donnees)
def product_detail(request, pk):
    product = get_object_or_404(Produits, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def edit_product(request, pk):
    product = get_object_or_404(Produits, pk=pk)

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.quantite = request.POST.get("quantite")
        product.description = request.POST.get("description")
        product.date_expiration = request.POST.get("date_expiration")
        if request.FILES.get("image"):
            product.image = request.FILES.get("image")
        product.save()
        messages.success(request, "✅ Produit modifié avec succès !")
        return redirect("home")

    return render(request, "edit_product.html", {"product": product}) 



def delete_product(request, pk):
    product = get_object_or_404(Produits, pk=pk)  # ⚠️ ici aussi, remplace Product → Produits
    if request.method == "POST":  # Confirmation suppression
        product.delete()
        return redirect('home')  # Retour à la liste après suppression
    return render(request, "delete_product.html", {"product": product})


def recherche(request):
    query = request.GET.get("produit", "").strip()  # récupération du texte saisi
    donnees = []

    if query:  # si on a tapé quelque chose
        donnees = Produits.objects.filter(name__icontains=query)

    context = {
        "donnees": donnees,
        "query": query,
    }
    return render(request, "resultat_recherche.html", context)

def Acc(request):
    return render(request, 'acc.html')


class Affichage(ListView):
    model = Produits
    template_name = 'home.html'
    context_object_name = 'produits'   # optionnel, mais plus clair








def ajoutvente(request, id):
    produit = get_object_or_404(Produits, id=id)  # <-- utilise le modèle correct
    message = None

    if request.method == 'POST':
        form = AjoutVente(request.POST)
        if form.is_valid():
            quantite = form.cleaned_data['quantite']
            nom_client = form.cleaned_data['customer']
            date_vente_form = form.cleaned_data['date_vente']

            if quantite > produit.quantite:  # <-- correspond au modèle Produits
                message = '❌ La quantité demandée est supérieure au stock disponible.'
            else:
                customer_instance, created = Customer.objects.get_or_create(name=nom_client)
                total_amount = produit.price * quantite  # <-- correspond au modèle Produits

                vente = Vente.objects.create(
                    produit=produit,
                    quantite=quantite,
                    customer=customer_instance,
                    total_amount=total_amount,
                    date_vente=date_vente_form,
                    heure_vente=timezone.localtime().time()
                )

                # Mise à jour du stock
                produit.quantite -= quantite  # <-- correspond au modèle Produits
                produit.save()

                return redirect('facture', vente_id=vente.id)
    else:
        form = AjoutVente(initial={'date_vente': timezone.localtime().date()})

    context = {
        'produit': produit,
        'form': form,
        'message': message
    }
    return render(request, 'ajoutvente.html', context)


def facture(request, vente_id):
    vente = get_object_or_404(Vente, id=vente_id)
    produit = vente.produit

    context = {
        'produit': produit,
        'quantite': vente.quantite,
        'prix_unitaire': produit.price,  # <-- correspond au modèle Produits
        'total_amount': vente.total_amount,
        'client': vente.customer,
        'date_facture': vente.date_vente,
        'heure_vente': vente.heure_vente,
        'facture_id': vente.id
    }

    return render(request, "facture.html", context)









def Saverecu(request, id):

    vente = get_object_or_404(Vente, id=id)
    customer = vente.customer,
    quantite = vente.quantite,
    total_amount = vente.total_amount,
    produit = vente.produit,

    recu = Facture_Client(
        customer = customer,
        quantite = quantite,
        total_amount = total_amount,
        produit = produit
    )

    recu.save()
    return redirect('facture', sale_id = id)









def liste_ventes(request):
    ventes = Vente.objects.select_related('customer', 'produit').all()

    # Calcul du total des ventes par mois pour le dashboard
    ventes_par_mois = (
        Vente.objects
        .annotate(mois=ExtractMonth('date_vente'))
        .values('mois')
        .annotate(total=Sum('total_amount'))
        .order_by('mois')
    )

    # Créer un tableau complet des 12 mois
    ventes_mensuelles = [0]*12
    for v in ventes_par_mois:
        index = v['mois'] - 1
        ventes_mensuelles[index] = float(v['total'])

    context = {
        'ventes': ventes,
        'ventes_mensuelles': ventes_mensuelles,
    }
    return render(request, 'liste_ventes.html', context)






# ✅ Fonctions personnalisées pour SQLite
class ExtractMonth(Func):
    function = 'strftime'
    template = "%(function)s('%%m', %(expressions)s)"
    output_field = IntegerField()

class ExtractYear(Func):
    function = 'strftime'
    template = "%(function)s('%%Y', %(expressions)s)"
    output_field = IntegerField()


def dashboard(request):
    # Récupérer toutes les ventes avec relations customer et produit
    ventes = Vente.objects.select_related('customer', 'produit').all()

    # Total des ventes par mois
    ventes_par_mois = (
        Vente.objects
        .annotate(mois=ExtractMonth('date_vente'))
        .values('mois')
        .annotate(total=Sum('total_amount'))
        .order_by('mois')
    )

    # Préparer un tableau complet des 12 mois
    ventes_mensuelles = [0]*12
    for v in ventes_par_mois:
        index = v['mois'] - 1
        ventes_mensuelles[index] = float(v['total'])

    # Répartition des ventes par produit pour le diagramme circulaire
    ventes_par_produit = (
        Vente.objects
        .values('produit__name')
        .annotate(total=Sum('total_amount'))
        .order_by('-total')
    )
    pie_labels = [v['produit__name'] for v in ventes_par_produit]
    pie_data = [float(v['total']) for v in ventes_par_produit]

    context = {
        'ventes': ventes,
        'ventes_mensuelles': ventes_mensuelles,
        'pie_labels': pie_labels,
        'pie_data': pie_data,
    }

    return render(request, 'dashboard.html', context)

















    