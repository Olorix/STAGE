from math import ceil

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.views import generic
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.urls import resolve, Resolver404

from paf.models import Profil, Metier, Metier2Theme
from paf.models import Theme, Module, TypeCandidature
from paf.forms import SearchForm

NUMBER_OF_RESULTS_BY_PAGE = 48
PAGE_OFFSET = 2

def index(request):
    context = {
        'profil_list': Profil.objects.all(),
        'form': SearchForm(
            initial = {
                'types_candidature': TypeCandidature.objects.filter(code=1),
            }
        ),
    }
    return render(request, 'paf/index.html', context)

def search(request):

    # Valeur par défaut
    modules = Module.objects.none()
    pages = [1]
    page = 1
    theme = None
    filters = {}

    form = SearchForm(request.GET)

    # Ajoute l'url de recherche à la session
    request.session['search_url'] = request.get_full_path()

    # Prend en compte les filtres
    if form.is_valid():

        # Récupère l'empreinte
        fields = ['profil', 'metier', 'searchbar', 'theme', 'types_candidature']
        get_data = []
        for field in fields :
            get_data += request.GET.getlist(field)
        get_data = tuple(get_data)

        _hash= hash(frozenset(get_data))

        # Récupère la page si aucun filtre n'a été changé
        if _hash == request.session.get('form_hash'):
            page = form.cleaned_data['page']

        # Écrit le nouveau hash (a bouger au besoin)
        request.session['form_hash'] = _hash

        # Filtre sur le métier
        metier = form.cleaned_data['metier']
        themes = metier.metier2theme_set.filter(
            weight__gt=0,
        ).values('theme')

        # Annote le poids du thème
        weight_subquery = Metier2Theme.objects.filter(
            theme=OuterRef('theme'),
            metier=metier,
        )

        modules = Module.objects.annotate(
            weight=Coalesce(
                Subquery(
                    weight_subquery.values('weight')[:1]
                ), 0,
            )
        )

        filters['theme__in'] = themes

        # Type de candidature
        filters['dispositif__type_candidature__in'] = form.cleaned_data['types_candidature']

        # Public-cible
        public_cibles = metier.public_associe.all()
        filters['public_cible__in'] = public_cibles

        # Thème (si différent du défaut: None)
        theme = form.cleaned_data['theme']
        if theme:
            filters['theme'] = theme

        # Applique les filtres
        modules = modules.filter(
            **filters
        ).order_by('weight', 'dispositif__code', 'code')

        number_of_pages = ceil(len(modules) / NUMBER_OF_RESULTS_BY_PAGE)
        page_max = min(page + PAGE_OFFSET, number_of_pages)
        page_min = max(page - PAGE_OFFSET, 1)
        pages = [*range(page_min, page_max+1)]
        page_start = (page-1)*NUMBER_OF_RESULTS_BY_PAGE
        page_end = page*NUMBER_OF_RESULTS_BY_PAGE

        themes = set([m.theme for m in modules])

        # Réduit les résultats
        modules = modules[page_start:page_end]

        # Mot clé (si différent du défaut: "")
        search = form.cleaned_data['searchbar']
        if search:
            # Créer le vecteur de recherche
            vector = SearchVector('theme__libelle', weight='A') + SearchVector('dispositif__libelle', weight='B') + SearchVector('libelle', weight='B') + SearchVector('contenu', weight='C')

            # Ajoute les mots-clés
            query = SearchQuery(search)

            # Applique la recherche
            modules = Module.objects.annotate(
                search_rank = SearchRank(vector, query)
            ).filter(
                **filters,
            ).order_by('-search_rank')



    # Récupère les modules sélectionnés
    selected_modules = request.session.get('selection')
    if selected_modules :
        selected_modules = list(map(int, selected_modules))
    else:
        selected_modules = []

    context = {
        'form': form,
        'modules': modules,
        'themes': themes,
        'pages': pages,
        'active_page': page,
        'selected_theme': theme,
        'selected_modules': selected_modules,
    }

    return render(request, 'paf/search.html', context)

def basket(request):

    types_candidature = []

    # Si une sélection existe
    if request.session.get('selection') :

        # Filtre les modules sélectionnés par Type de candidature
        for type_candidature in TypeCandidature.objects.all().order_by('code'):
            types_candidature.append({
                'title': type_candidature.libelle,
                'instructions': type_candidature.instructions,
                'modules': Module.objects.filter(
                    dispositif__type_candidature = type_candidature,
                    id__in = request.session.get('selection'),
                )
            })

    search_url = request.session.get("search_url") or '/mon-paf/search'

    context = {
        'types_candidature': types_candidature,
        'search_url': search_url,
    }

    return render(request, 'paf/basket.html', context)

class AjaxMetierLoad(generic.DetailView):
    model = Profil
    template_name = 'paf/ajax/metier.html'

class AjaxModuleDetail(generic.DetailView):
    model = Module
    template_name = 'paf/ajax/modal.html'

def ajax_add_to_selection(request):

    message = 'Ce module a bien été ajouté à votre sélection.'

    # Si l'utilisateur n'a pas de sélection
    if not request.session.get('selection'):
        request.session['selection'] = []

    # Ajoute le module
    module = request.GET.get('module')
    request.session['selection'] += [module] if module not in request.session['selection'] else []

    return render(request, 'paf/ajax/success-toast.html', {'message': message})

def ajax_remove_from_selection(request):

    message = 'Ce module a bien été supprimé de votre sélection.'

    try:

        # Retire le module de la sélection
        request.session['selection'].remove(request.GET.get('module'))
        request.session.modified = True

        return render(request, 'paf/ajax/success-toast.html', {'message': message})
    except:
        message = 'Désolé votre requête a échoué.'
        return render(request, 'paf/ajax/error-toast.html', {'message': message})
