from django.db import models
from django.utils import timezone  # ← Ajoute cette ligne
from django.contrib.auth.models import User
from django.conf import settings  # <-- ajouter ceci


class Categories(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


# class pour les produits
class Produits(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantite = models.PositiveIntegerField(default=0)
    description = models.TextField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateField()
    image = models.ImageField(null=True, blank=True, upload_to='media/')

    class Meta:
        ordering = ['-date_ajout']

    def statut_quantite(self):
        # si la quantité est égale à 0 affiche rouge
        if self.quantite == 0:
            return 'red'
        # si la quantité est inférieure ou égale à 10 affiche orange
        elif self.quantite <= 10:
            return 'orange'
        # sinon vert
        else:
            return 'green'

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def heure_actuelle():
    return timezone.localtime().time()

class Vente(models.Model):
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE)  # <-- lien correct
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_vente = models.DateField(default=timezone.now)
    heure_vente = models.TimeField(default=heure_actuelle)

    def __str__(self):
        return f"{self.produit.name} - {self.customer.name}"

   
    
def facture(request, vente_id):
    vente = get_object_or_404(Vente, id=vente_id)
    produit = vente.produit
    client = vente.customer
    quantite = vente.quantite
    prix_unitaire = produit.price
    total_amount = vente.total_amount
    date_facture = vente.date_vente

    return render(request, 'facture.html', {
        'produit': produit,
        'client': client,
        'quantite': quantite,
        'prix_unitaire': prix_unitaire,
        'total_amount': total_amount,
        'date_facture': date_vente,
        'facture_id': vente.id
    })


class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Produit(models.Model):
    name = models.CharField(max_length=100)
    prix = models.IntegerField()
    stock = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='media/')

    def __str__(self):
        return self.name












