from django import forms
from django.forms import ModelForm
from .models import Produits
from .models import Vente, Customer


# Formulaire pour ajouter/modifier un produit
class AjoutProduit(ModelForm):
    class Meta:
        model = Produits
        fields = [
            'name', 'category', 'price', 'quantite', 'description', 'date_expiration', 'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Entrez le nom du produit',
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Entrez le prix du produit',
                'class': 'form-control'
            }),
            'quantite': forms.NumberInput(attrs={
                'placeholder': 'Entrez la quantité',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Entrez la description',
                'class': 'form-control',
                'rows': 4
            }),
            'date_expiration': forms.DateInput(attrs={
                'placeholder': "Entrez la date d'expiration",
                'class': 'form-control',
                'type': 'date'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(AjoutProduit, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages = {
            'required': 'Le nom du produit est obligatoire',
            'invalid': 'Veuillez entrer un nom correct.',
        }
        self.fields['category'].error_messages = {
            'required': 'La catégorie est obligatoire',
            'invalid': 'Veuillez sélectionner une catégorie valide.',
        }
        self.fields['price'].error_messages = {
            'required': 'Le prix du produit est obligatoire',
            'invalid': 'Veuillez entrer un prix correct.',
        }
        self.fields['quantite'].error_messages = {
            'required': 'La quantité est obligatoire.',
            'invalid': 'Veuillez entrer une quantité valide.',
        }
        self.fields['description'].error_messages = {
            'required': 'La description est obligatoire.',
            'invalid': 'Veuillez entrer une description valide.',
        }
        self.fields['date_expiration'].error_messages = {
            'required': "La date d'expiration du produit est obligatoire.",
            'invalid': "Veuillez entrer une date d'expiration valide.",
        }


# Formulaire pour ajouter une vente


class AjoutVente(forms.Form):
    customer = forms.CharField(
        max_length=100,
        label="Nom du client",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du client'})
    )
    quantite = forms.IntegerField(
        min_value=1,
        label="Quantité",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité'})
    )
    date_vente = forms.DateField(
        label="Date de vente",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})  # ✅ date picker
    )


    


