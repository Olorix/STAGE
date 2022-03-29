from django import forms

from paf.models import Profil, Metier
from paf.models import Theme, TypeCandidature

class SearchForm(forms.Form):
    """
    Formulaire de recherche, qui permet à l'utilisateur
    de faire une recherche dans son offre de formation.
    """
    
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        # Si formulaire est pré-rempli
        if self.is_bound:

            # Si le formulaire est valide
            if self.is_valid():

                # Ajuste le queryset
                profil = self.cleaned_data['profil']
                self.fields['metier'].queryset = profil.metier_set.all().order_by("libelle")

    # Profil de l'utilisateur
    profil = forms.ModelChoiceField(
        queryset = Profil.objects.all(),
        widget = forms.Select(
            attrs = {
                'class': 'form-select',
            }
        )
    )

    # Métier de l'utilisateur
    metier = forms.ModelChoiceField(
        queryset = Metier.objects.all().order_by('libelle'),
        widget = forms.Select(
            attrs = {
                'class': 'form-select',
            }
        )
    )

    # Barre de recherche
    searchbar = forms.CharField(
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'type':'search',
                'placeholder':'Mots-clés...',
            }
        )
    )

    # Sélection du thème
    theme = forms.ModelChoiceField(
        queryset = Theme.objects.all(),
        required = False,
        widget = forms.Select(
            attrs = {
                'class': 'form-select',
            }
        )
    )

    # Sélection du type de candidature
    types_candidature = forms.ModelMultipleChoiceField(
        queryset = TypeCandidature.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple(
            attrs = {
                'class': 'form-check-input',
            }
        ),

        # Par défaut tout les types de candidatures
        # sont sélectionnées
        initial = TypeCandidature.objects.all(),
    )

    # Page courante
    page = forms.IntegerField(
        min_value = 1,
    )
