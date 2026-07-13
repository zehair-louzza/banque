# Partie 1 — Questions de cours

## 1. Différence entre programmation procédurale et programmation orientée objet

La **programmation procédurale** organise le code autour de fonctions et de procédures qui manipulent des données passées en arguments : les données et les traitements sont séparés. La **programmation orientée objet (POO)** regroupe au contraire les données (attributs) et les comportements (méthodes) au sein d'objets. La POO favorise l'encapsulation, la réutilisation (héritage) et le polymorphisme, ce qui facilite la maintenance des projets complexes.

## 2. Différence entre une classe et un objet

Une **classe** est un modèle (un plan) qui décrit la structure et le comportement d'un type d'entité : elle définit les attributs et les méthodes. Un **objet** (ou instance) est une réalisation concrète de cette classe en mémoire, avec ses propres valeurs d'attributs. Exemple : `CompteBancaire` est la classe, `compte = CompteBancaire("Louzza", 100)` est un objet.

## 3. Différence entre un attribut et une méthode

Un **attribut** est une variable rattachée à un objet ou à une classe ; il représente un état ou une donnée (ex. `solde`, `titulaire`). Une **méthode** est une fonction définie dans une classe ; elle représente un comportement ou une action agissant sur l'objet (ex. `deposer()`, `retirer()`).

## 4. Rôle de `__init__` et `self`

`__init__` est le **constructeur** : c'est la méthode appelée automatiquement à la création d'une instance pour initialiser ses attributs. `self` est la **référence à l'instance courante** ; il est passé implicitement en premier paramètre de chaque méthode et permet d'accéder aux attributs et méthodes de l'objet (ex. `self.solde = solde`).

## 5. Différence entre un module et un package Python

Un **module** est un simple fichier `.py` contenant du code réutilisable (fonctions, classes, variables). Un **package** est un répertoire regroupant plusieurs modules ; il contient généralement un fichier `__init__.py` qui signale à Python qu'il s'agit d'un package importable. Un package permet donc d'organiser hiérarchiquement plusieurs modules.

## 6. Les quatre opérations CRUD et leur méthode HTTP

| Opération | Signification | Méthode HTTP |
|-----------|---------------|--------------|
| **C**reate | Créer une ressource | `POST` |
| **R**ead | Lire / consulter | `GET` |
| **U**pdate | Modifier | `PUT` (ou `PATCH`) |
| **D**elete | Supprimer | `DELETE` |

## 7. Rôle de `schemas.py`, `services.py` et `models.py` dans une API structurée

- **`models.py`** : définit les modèles de données de la base (tables SQLAlchemy). Il décrit la structure persistée en base de données.
- **`schemas.py`** : définit les schémas Pydantic de validation et de sérialisation. Il contrôle les données entrantes (requêtes) et sortantes (réponses) de l'API, indépendamment du stockage.
- **`services.py`** : contient la logique métier et les accès à la base (CRUD). Il fait le lien entre les routes et les modèles, en isolant les règles métier des couches HTTP et base de données.

Cette séparation respecte le principe de responsabilité unique : les routes gèrent le HTTP, les schemas la validation, les services le métier, les models la persistance.

## 8. Test unitaire et régression

Un **test unitaire** vérifie de manière isolée le bon fonctionnement d'une unité de code (une fonction, une méthode) pour un cas donné, en comparant le résultat obtenu au résultat attendu. Il doit être indépendant, reproductible et rapide.

Une **régression** est la réapparition d'un bug ou la rupture d'un comportement qui fonctionnait auparavant, généralement provoquée par une modification du code. Les tests unitaires servent justement à détecter les régressions automatiquement.
