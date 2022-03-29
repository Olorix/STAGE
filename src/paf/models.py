from django.db import models

# Type de candidature
class TypeCandidature(models.Model):
    code = models.CharField('Code', primary_key=True, max_length=1)
    libelle = models.CharField('Libellé', max_length=250)
    instructions = models.TextField('Instructions', max_length=1500, blank=True, null=True)
    def __str__(self):
        return self.libelle

# Type de plan
class TypePlan(models.Model):
    code = models.CharField('Code', primary_key=True, max_length=1)
    libelle = models.CharField('Libellé', max_length=250)

    def __str__(self):
        return self.libelle

# Dispositif
class Dispositif(models.Model):
    code = models.CharField('Code', primary_key=True, max_length=10)
    libelle = models.CharField('Libellé', max_length=250)
    type_candidature = models.ForeignKey(TypeCandidature, on_delete=models.CASCADE)
    type_plan = models.ForeignKey(TypePlan, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.code} {self.libelle}'


# Modalité
class Modalite(models.Model):
    code = models.CharField('Code', primary_key=True, max_length=1)
    libelle = models.CharField('Libellé', max_length=250)

    def __str__(self):
        return self.libelle

# Public-cible
class PublicCible(models.Model):
    code = models.CharField('Code', primary_key=True, max_length=2)
    libelle = models.CharField('Libellé', max_length=250)

    def __str__(self):
        return self.libelle

# Thème (Nomenclature budgétaire)
class Theme(models.Model):
    code = models.CharField('Code', max_length=4)
    libelle = models.CharField('Libellé', max_length=250)
    code_origine = models.CharField('Code d\'origine', max_length=3)

    def __str__(self):
        return f'{self.code_origine} - {self.libelle}'

# Période
class Periode(models.Model):
    code = models.CharField('Code', primary_key=True, max_length=3)
    libelle = models.CharField('Libellé', max_length=50)

    def __str__(self):
        return self.libelle


# Module
class Module(models.Model):
    code = models.IntegerField('Code', default=0)
    dispositif = models.ForeignKey(Dispositif, on_delete=models.CASCADE)
    libelle = models.CharField('Libellé', max_length=250)
    modalite = models.ForeignKey(Modalite, on_delete=models.CASCADE)
    public_cible = models.ForeignKey(PublicCible, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    # periode = models.CharField('Période', max_length=250)
    periode = models.ForeignKey(Periode, on_delete=models.CASCADE)
    duree = models.SmallIntegerField('Durée (heure)', default=0)
    contenu = models.TextField('Contenu', max_length=1000)
    objectifs = models.TextField('Objectifs pédagogique', max_length=1000)

    def __str__(self):
        return self.libelle

    class Meta:

        # La combinaision du code de module et du code de dispositif est
        # unique pour chaque module
        constraints = [
            models.UniqueConstraint(
                fields = ['code', 'dispositif_id'],
                name = 'unique_id',
            ),
        ]

# Profils
class Profil(models.Model):
    code = models.CharField('Code', primary_key=True, max_length=4)
    libelle = models.CharField('Libellé', max_length=250)

    def __str__(self):
        return self.libelle

# Métiers
class Metier(models.Model):
    libelle = models.CharField('Libellé', max_length=250)
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
    public_associe = models.ManyToManyField(PublicCible)
    related_themes = models.ManyToManyField(Theme, through='Metier2Theme')

    def __str__(self):
        return self.libelle

# Table de liaison
class Metier2Theme(models.Model):
    metier = models.ForeignKey(Metier, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Relation Métier/Thème"

    def __str__(self):
        return f'{self.metier} => {self.theme} : {self.weight}'
