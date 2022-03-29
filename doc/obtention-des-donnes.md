# Importation des données
L'outil mon-paf repose sur sa propre base de données, celle-ci peut être
alimenter et/ou mise à jour avec des fichiers plats (e.g. csv).

## Architecture des données
L'outil utilise l'intitulé de chaque colonne pour identifier les données à importer.
Il est donc **obligatoire** que les intitulés présents dans les fichiers plats
soient parfaitement identiques à ceux attendus par le logiciel.

Vous trouverez ci-dessous une référence pour chaque table comportant: Ses champs,
leur représentation en base de données ainsi que les intitulés attendus.

> **Remarque**: Par soucis de lisibilité ce document ne montre aucun exemple de
fichier plats pouvant être utilisé pour l'importation. Si vous souhaitez consulter
des exemples de fichier de données, des fichiers `csv` d'exemple sont fournis
dans le répertoire `data/csv` du dépôt.

### Type de Plan
La table `TypePlan` contient l'ensemble des types de plan utilisés dans les
différents [dispositifs](#dispositif). Elle correspond à une version simplifiée
de la table `NTPLA` de GAIA.

| Champs  | Champs en base de données | Intitulés attendus | Contraintes |
|---------|---------------------------|--------------------|-------------|
| Code    | code                      | code               | 1 char (pk) |
| Libellé | libelle                   | libelle            | 250 char    |

### Type de candidature
La table `TypeCandidature` contient l'ensemble des types de candidature utilisés
dans les différents [dispositifs](#dispositif). Elle correspond à une version
simplifiée de la table `NTCAN` de GAIA.

| Champs       | Champs en base de données | Intitulés attendus | Contraintes     |
|--------------|---------------------------|--------------------|-----------------|
| Code         | code                      | code               | 1 char (pk)     |
| Libellé      | libelle                   | libelle            | 250 char        |
| Instructions | instructions              | instructions       | 1500 char (opt) |

> **Remarque**: Le champ `instructions` n'existe pas dans GAIA. Il s'agit d'un
champs optionnel qui permet d'afficher des indications concernants l'inscription
sur GAIA dans la page: "Ma sélection".

### Dispositif
La table `Dispositif` contient l'ensemble des dispositifs référencés par les
différents [modules](#modules). Elle corresponds à une version simplifíée de la
table `GDISP` de GAIA.

| Champs              | Champs en base de données | Intitulés attendus | Contraintes  |
|---------------------|---------------------------|--------------------|--------------|
| Code                | code                      | code               | 10 char (pk) |
| Libellé             | libelle                   | libelle            | 250 char     |
| Type de Candidature | type\_candidature         | type\_candidature  | 1 char (fk)  |
| Type de Plan        | type\_plan                | type\_plan         | 1 char (fk)  |

### Thème
La table `Theme` contient l'ensemble des thèmes utilisés dans les différents
[modules](#module). Elle correspond à une version simplifiée de la table `NBUDG` de GAIA.

| Champs       | Champs en base de données | Intitulés attendus | Contraintes |
|--------------|---------------------------|--------------------|-------------|
| Code         | code                      | code               | 4 char (pk) |
| Libellé      | libelle                   | libelle            | 250 char    |
| Code origine | code\_origine             | code\_origine      | 3 char (pk) |

> **Remarque**: Le champ `code_origine` n'est pas présent dans GAIA. Il doit
être ajouté à l'exportation afin de différencier les thèmes (nomenclature budgétaire)
de chaque région.

### Public cible
La table `PublicCible` contient l'ensemble des publics cible utilisés dans les
différents [modules](#module). Elle correspond à une version simplifiée de la
table `NCIBL` de GAIA.

| Champs       | Champs en base de données | Intitulés attendus | Contraintes |
|--------------|---------------------------|--------------------|-------------|
| Code         | code                      | code               | 2 char (pk) |
| Libellé      | libelle                   | libelle            | 250 char    |

### Période
Le contenu de la table `Periode` dépends de vos choix dans `src/paf/models.py`
(Voir: [Comment modifier la période ?](http://)). Si vous avez choisi d'utiliser
des périodes prédéfinies comme dans l'académie d'Amiens, cette table contient
l'ensemble des périodes utilisées dans les différents [modules](#module).
Dans le cas contraire cette table n'est pas utilisée et vous pouvez ignorer cette
section.

| Champs       | Champs en base de données | Intitulés attendus | Contraintes |
|--------------|---------------------------|--------------------|-------------|
| Code         | code                      | code               | 3 char (pk) |
| Libellé      | libelle                   | libelle            | 50 char     |

### Modalité
La table `Modalite` contient l'ensemble des modalités utilisés dans les
différents [modules](#module). Elle correspond à une version simplifiée de la
table `NMODA` de GAIA.

| Champs       | Champs en base de données | Intitulés attendus | Contraintes |
|--------------|---------------------------|--------------------|-------------|
| Code         | code                      | code               | 1 char (pk) |
| Libellé      | libelle                   | libelle            | 250 char    |

### Module
La table `Module` contient l'ensemble des modules qui compose le Plan Académique
de Formation. Elle correspond à une version simplifiée de la table `GMODU` de GAIA.

| Champs       | Champs en base de données | Intitulés attendus | Contraintes  |
|--------------|---------------------------|--------------------|--------------|
| Code         | code                      | code               | entier (pk)  |
| Libellé      | libelle                   | libelle            | 250 char     |
| Dispositif   | dispositif                | dispositif         | 10 char (fk) |
| Modalité     | modalite                  | modalite           | 1 char (fk)  |
| Public cible | public\_cible             | public\_cible      | 2 char (fk)  |
| Contenu      | contenu                   | contenu            | 1000 char    |
| Objectifs    | objectifs                 | objectifs          | 1000 char    |
| Période      | periode                   | periode            | 3 char (fk)  |
|              |                           |                    | ou 250 char  |
| Thème        | theme\_code               | theme\_code        | 4 char (fk)  |
|              | theme\_origine            | theme\_origine     | 3 char (fk)  |
| Durée        | duree                     | duree              | entier       |

### Profil
La table `Profil` contient l'ensemble des profils utilisés dans les différents
[métiers](#metier). Elle ne correspond à aucune table de GAIA.

| Champs       | Champs en base de données | Intitulés attendus | Contraintes |
|--------------|---------------------------|--------------------|-------------|
| Code         | code                      | code               | 4 char (pk) |
| Libellé      | libelle                   | libelle            | 250 char    |

### Métier
La table `Metier` contien l'ensemble des métiers utilisés par l'application pour
établir un profil de l'utilisateur. Elle ne correspond à aucune table de GAIA.

| Champs       | Champs en base de données | Intitulés attendus | Containtes  |
|--------------|---------------------------|--------------------|-------------|
| Code         | code                      | code               | entier (pk) |
| Libellé      | libelle                   | libelle            | 250         |
| Profil       | profil                    | profil             | 4 char (fk) |

## Obtenir les données avec SAP BusinessObject
Ces fichiers peuvent être obtenus à l'aide de [SAP BusinessObject]
(https://support.sap.com/en/index.html). 

Voir les [requêtes utilisées dans l'acadęmie d'Amiens](#annexes)

## Manipulation d'importation
### Tableaux relationnels
Certaines tables de la base sont liées entre-elle, cela contraint l'importation
des données à suivre le sens de ces relations. Les relations entre les différentes
tables sont représentées par les tableaux ci-dessous.

| Tables indépendantes |
|----------------------|
| Type de candidature  |
| Type de plan         |
| Thème                |
| Public cible         |
| Période (*)          |
| Modalité             |
| Profil               |

| Table      | Dépendances                                            |
|------------|--------------------------------------------------------|
| Dispositif | Type Candidature, Type de Plan                         |
| Module     | Dispositif, Thème, Public cible, Période (*), Modalité |
| Métier     | Profil                                                 |

\* La table `Période` n'est pas nécessaire si vous n'avez pas choisi d'utiliser
des périodes prédéfinies.

> **Précautions**: Lors de l'importation il est **impératif** de suivre le sens 
des relations. Avant d'importer une table il faut s'assurer d'avoir importer 
toutes ses dépendances.

### Importation d'une entité
L'importation des données se fait sur le site d'administration situé à l'adresse
`url-du-serveur/admin` (Si vous rencontrez des problèmes lors de la connexion
consulter la section "Se connecter" la page [Administration de base](administration-de-base.md)).
Une fois connecté à l'application vous pouvez choisir la table dont vous souhaiter
importer les donnéees (figure 1).

![Page d'accueil du site d'administration](doc/images/admin-accueil.png)

Une fois que vous avez choisi une table, vous pouvez ouvrir l'interface d'import
de celle-ci avec le bouton `IMPORTER` situé en haut à droite de la page (figure 2).

![Page de détail](doc/images/admin-details.png)

Une fois sur l'interface d'importation vous pouvez sélectionner le fichier à
importer ainsi que son format. Cliquer sur `SOUMETTRE` pour valider l'importation
(figure 3).

![Page d'import](doc/images/admin-import.png)

Une fois votre fichier importé, un résumé des actions à appliquer est affiché.
Prennez le temps de vérifier que ce résumé convient bien au imports et 
modifications que vous souhaitez appliquer. Si vous êtes sûr des changements à
appliquer, cliquer sur `CONFIRMER L IMPORTATION` (figure 4).

![Résumé de l'import](doc/images/admin-import-resume.png)

> **Remarque**: Quand vous importez un fichier de données, l'application vérifie
chaque enregistrement de manière individuelle. Cette étape peut donc prendre
quelques minutes, surtout si vous importer les `dispositifs` ou les `modules`
qui comporte généralement des milliers d'enregistrements.

## Erreurs connues

### Mes données sont incohérentes
L'outil se base sur les libellés du fichier pour identifier 
les données à importer. Cependant il arrive que 2 fichiers 
différents possède les même libellés. Cela peut mener à l'importation de données incohérentes.

### Mes données sont incomplètes
L'outil se base sur les libellés du fichier pour identifier 
les données à importer. S'il manque un libellé, ou que celui-ci
est incorrect les données ne seront pas reconnues et ne seront donc pas importées. Si le champs en question n'est pas un champs obligatoire, le logiciel n'affichera aucun message d'erreur et considérera le champs comme vide.

### Je ne vois aucun enregistrements
L'outil se base sur les libellés du fichier pour identifier les données à importer. Si la première ligne du fichier ne comporte aucun libellé, le logiciel ne détectera aucun enregistrements.

## Exporter les données avec BI
### Dans l'académie d'Amiens
La DAFPEN d'Amiens possède des rapports déjà prêt pour exporter
le *Plan Académique de Formation* du réplicat de GAIA. Pour y
accéder rendez-vous à l'adresse: [http://bisap.in.ac-amiens.fr:8080/BOE/BI]. Une fois connecté à BI, suivez le chemin `DAFPEN - Formation => DAFPEN => 2DAFPEN BASE2ND D + ATSS => Offre et PAF => iPAF`.

## Annexes
### Requêtes utilisées dans l'académie d'Amiens
```sql
SELECT
  GDISP.co_tpla,
  NTPLA_DISP.lib_long,
  GDISP.co_offreur,
  GDISP.id_disp,
  GDISP.libl,
  NTCAN.co_tcan,
  NTCAN.lib_long,
  GDISP.co_orie,
  NORIE.lib_long,
  GMODU.co_modu,
  GMODU.libl,
  NMODA.co_moda,
  NMODA.lib_long,
  NCIBL.co_cibl,
  NCIBL.lib_long,
  GMODU.lcont,
  GMODU.LPEDA,
  NBUDG.co_budg,
  NBUDG.lib_long,
  GMODU.LCOMM,
  GMODU.duree_prev,
  GMODU.co_prna,
  GMODU.lautre,
  GMODU.lform,
  GMODU.nb_place_prev,
  GMODU.PUBLIE
FROM
  GDISP LEFT OUTER JOIN NORIE ON GDISP.CO_ORIE=NORIE.CO_ORIE,
  NTPLA  NTPLA_DISP,
  NTCAN,
  GMODU,
  NMODA,
  NCIBL,
  NBUDG,
  NINIT
WHERE
  ( GDISP.CO_INIT=NINIT.CO_INIT  )
  AND  ( GDISP.CO_TCAN=NTCAN.CO_TCAN  )
  AND  ( NBUDG.CO_BUDG=GMODU.CO_BUDG  )
  AND  ( NCIBL.CO_CIBL=GMODU.CO_CIBL  )
  AND  ( NMODA.CO_MODA=GMODU.CO_MODA  )
  AND  ( GDISP.CO_DISP=GMODU.CO_DISP  )
  AND  ( GDISP.CO_TPLA=NTPLA_DISP.CO_TPLA  )
  AND
  (
   '20'||SUBSTR(GDISP.id_disp,1,2)  =  @prompt('Saisir une ou plusieurs valeurs pour Année de gestion','A','Dispositif de formation\Année de gestion',Mono,Free,Persistent,,User:0)
   AND
   GMODU.PUBLIE  =  'O'
   AND
   NINIT.lib_long  IN  ( 'ACADEMIQUE','DEPARTEMENTAL'  )
  )
```
