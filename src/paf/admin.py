from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from import_export.results import RowResult

from paf.models import TypeCandidature, TypePlan, Dispositif
from paf.models import Modalite, PublicCible, Theme, Periode, Module
from paf.models import Profil, Metier, Metier2Theme

class ModelResource(resources.ModelResource):

    # Utilisé pour corriger les erreurs d'encodage
    # venant de GAIA.
    clean_dict = {
        '&#8217;':"'",
        '&#8211;':'à',
        '&#8226;':' ',
        r'\r':' ',
        r'\n':' ',
    }

    def get_field_names(self):
        names = []
        for field in self.get_fields():
            names.append(self.get_field_name(field))
        return names + ['Erreurs']

    def import_row(self, row, instance_loader, **kwargs):
        """
        Ignore les erreurs d'importation et empêche l'importation de planter
        si une ligne de donnée est incorrecte.
        """
        import_result = super(ModelResource, self).import_row(
            row, instance_loader, **kwargs
        )

        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            import_result.diff = [
                row.get(name, '') for name in self.get_field_names()
            ]

            # Ajoute une colonne avec les message d'erreurs
            import_result.diff.append(
                "Errors: {}".format(
                    [err.error for err in import_result.errors]
                )
            )
            # Reste les erreurs d'import et marque les lignes en "SKIP"
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP

        return import_result

    def before_import_row(self, row, row_number=None, **kwargs):
        """
        Corrige les erreurs d'encodage de GAIA en appliquant les 
        changements de clean_dict.
        """

        for field in self.text_fields:

            # Si le champs n'est pas vide
            if row.get(field):
                text = row.get(field)
                
                # Nettoie le texte
                for key, value in self.clean_dict.items():
                    text = text.replace(key, value)

                # Ré-écrit le texte sanifié
                row[field] = text.strip()


# Champs personnalisé
class LiaisonMetierThemesInline(admin.TabularInline):
    model = Metier2Theme
    extra = 0


# --- Type de candidature ---
class TypeCandidatureResource(ModelResource):
    """Ressource lié au modèle TypeCandidature."""
    
    imported_rows_pks = []
    text_fields = ['libelle']

    class Meta:
        model = TypeCandidature
        import_id_fields = ['code']
        skip_unchanged = True
        report_skipped = True

@admin.register(TypeCandidature)
class TypeCandidatureAdmin(ImportExportActionModelAdmin):
    """Modèle Admin lié au modèle TypeCandidature."""
    resource_class = TypeCandidatureResource


# --- Type de plan ---
class TypePlanResource(ModelResource):
    """Ressource lié au modèle TypePlan."""
    
    imported_rows_pks = []
    text_fields = ['libelle']

    class Meta:
        model = TypePlan
        import_id_fields = ['code']
        skip_unchanged = True

@admin.register(TypePlan)
class TypePlanAdmin(ImportExportActionModelAdmin):
    """Modèle Admin lié au modèle TypePlan."""
    resource_class = TypePlanResource


# --- Dispositif ---
class DispositifResource(ModelResource):
    """Ressource lié au modèle Dispositif."""
    
    imported_rows_pks = []
    text_fields = ['libelle']

    class Meta:
        model = Dispositif
        import_id_fields = ['code']
        skip_unchanged = True


@admin.register(Dispositif)
class DispositifAdmin(ImportExportActionModelAdmin):
    """Modèle Admin lié au modèle Dispositif."""
    resource_class = DispositifResource

    # Paramètres de l'interface
    search_fields = ['code', 'libelle']
    list_display = ('code', 'libelle', 'type_candidature', 'type_plan')
    list_filter = ['type_candidature', 'type_plan']


# --- Modalite ---
class ModaliteResource(ModelResource):
    """Ressource lié au modèle Modalite."""
    
    imported_rows_pks = []
    text_fields = ['libelle']

    class Meta:
        model = Modalite
        import_id_fields = ['code']
        skip_unchanged = True

@admin.register(Modalite)
class ModaliteAdmin(ImportExportActionModelAdmin):
    """Modèle Admin lié au modèle Modalite."""
    resource_class = ModaliteResource


# --- Public cible ---
class PublicCibleResource(ModelResource):
    """Ressource lié au modèle PublicCible."""
    
    imported_rows_pks = []
    text_fields = ['libelle']

    class Meta:
        model = PublicCible
        import_id_fields = ['code']
        skip_unchanged = True

@admin.register(PublicCible)
class PublicCibleAdmin(ImportExportActionModelAdmin):
    """Modèle Admin lié au modèle PublicCible."""
    resource_class = PublicCibleResource

    # Paramètres de l'interface
    search_fields = ['libelle']


# --- Theme ---
class ThemeResource(ModelResource):
    """Ressource lié au modèle Theme."""
    
    imported_rows_pks = []
    text_fields = ['libelle']

    class Meta:
        model = Theme
        import_id_fields = ['code', 'code_origine']
        exclude = ['id']
        skip_unchanged = True

@admin.register(Theme)
class ThemeAdmin(ImportExportActionModelAdmin):
    """Modèle Admin lié au modèle Theme."""
    resource_class = ThemeResource
    inlines = (LiaisonMetierThemesInline,)

    # Paramètres de l'interface
    fields = ["code", "libelle", "code_origine"]
    search_fields = ['code', 'libelle']
    list_display = ('code', 'libelle', 'code_origine')
    list_filter = ['code_origine']
    ordering = ('code_origine', 'libelle')

class ThemeForeignKeyWidget(ForeignKeyWidget):
    """Widget personnalisé permettant de charger une relation de clé étrangère
    à partir d'une double clé primaire (code && code_origine)."""

    def get_queryset(self, value, row):
        return self.model.objects.filter(
            code__iexact=row["theme_code"],
            code_origine__iexact=row["theme_origine"]
        )


# --- Période ---
class PeriodeResource(ModelResource):
    """Ressource lié au modèle Periode."""
    
    imported_rows_pks = []
    text_fields = ['libelle']

    class Meta:
        model = Periode
        import_id_fields = ['code']
        skip_unchanged = True

@admin.register(Periode)
class PeriodeAdmin(ImportExportActionModelAdmin):
    """Modèle Admin lié au modèle Periode."""
    resource_class = PeriodeResource


# --- Module ---
class ModuleResource(ModelResource):
    """Ressource lié au modèle Module."""
    
    imported_rows_pks = []
    text_fields = ['libelle', 'objectifs', 'contenu']

    theme = Field(
        column_name='theme_code',
        attribute='theme',
        widget=ThemeForeignKeyWidget(Theme, 'code'))

    class Meta:
        model = Module
        import_id_fields = ['code', 'dispositif']
        exclude = ['id']
        skip_unchanged = True

@admin.register(Module)
class ModuleAdmin(ImportExportActionModelAdmin):
    """Modèle Admin lié au modèle Module."""
    resource_class = ModuleResource

    # Paramètres de l'interface
    search_fields = ['code', 'libelle']
    list_display = ('code', 'libelle', 'dispositif')
    list_filter = ['modalite']

# --- Profil ---
class ProfilResource(ModelResource):
    """Ressource lié au modèle PublicCible."""
    
    imported_rows_pks = []
    text_fields = ['libelle']

    class Meta:
        model = Profil
        import_id_fields = ['code']
        skip_unchanged = True

@admin.register(Profil)
class ProfilAdmin(ImportExportActionModelAdmin):
    """Modèle Admin lié au modèle Profil."""
    resource_class = ProfilResource


# --- Métier ---
class MetierResource(ModelResource):
    """Ressource lié au modèle Metier."""
    
    imported_rows_pks = []
    text_fields = ['libelle']

    class Meta:
        model = Metier
        import_id_fields = ['id']
        skip_unchanged = True

@admin.register(Metier)
class MetierAdmin(ImportExportActionModelAdmin):
    """Modèle Admin lié au modèle Metier."""
    resource_class = MetierResource
    inlines = (LiaisonMetierThemesInline,)
    filter_horizontal = ('public_associe',)

    # Paramètres de l'interface
    list_display = ('libelle', 'profil')
    search_fields = ['libelle']
    list_filter = ['profil']

class Metier2ThemeResource(ModelResource):
    """Ressource lié au modèle PublicCible."""
    
    imported_rows_pks = []
    text_fields = ['libelle']

    theme = Field(
        column_name='theme_code',
        attribute='theme',
        widget=ThemeForeignKeyWidget(Theme, 'code'))

    theme_origine = Field(
        column_name = 'theme_origine',
        attribute = 'theme__code_origine'
    )

    class Meta:
        model = Metier2Theme
        import_id_fields = ['metier', 'theme']
        fields = ["theme_code", "theme_origine", "metier", "weight"]
        exclude = ['id']
        skip_unchanged = True

@admin.register(Metier2Theme)
class Metier2ThemeAdmin(ImportExportActionModelAdmin):
    """Modèle Admin lié au modèle Metier2Theme."""
    resource_class = Metier2ThemeResource

    # Paramètres de l'interface
    list_display = ('metier', 'theme', 'weight')
    search_fields = ['metier__libelle']
