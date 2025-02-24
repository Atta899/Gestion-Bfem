# README - Gestion BFEM

## Description du Projet

Ce projet vise à développer un prototype de logiciel destiné à la gestion des données et à la délibération des candidats lors de l'examen du **Brevet de Fin d'Études Moyennes (BFEM)** au Sénégal. Le logiciel intègre une interface graphique en Python utilisant **Tkinter** pour la gestion des candidats, des jurys, des délibérations, des statistiques, et bien plus encore. Le système est couplé à une base de données **SQLite** pour stocker et gérer les informations des candidats, des notes, et des résultats.

## Fonctionnalités Principales

Le logiciel propose les fonctionnalités suivantes :

1. **Gestion des Candidats** :
   - Ajout, modification, suppression et consultation des candidats.
   - Gestion des informations personnelles des candidats (nom, prénom, date de naissance, etc.).
   - Gestion des notes et des épreuves facultatives.

2. **Gestion du Jury** :
   - Configuration des informations du jury (région, département, centre d'examen, etc.).
   - Enregistrement des membres du jury et des responsables.

3. **Délibération** :
   - Calcul des points et des moyennes des candidats.
   - Délibération des résultats (admis, second tour, échoués, repêchables).
   - Gestion du second tour avec saisie des notes supplémentaires.

4. **Statistiques** :
   - Affichage des statistiques générales (nombre de candidats, moyenne des points, etc.).
   - Génération de graphiques circulaires pour visualiser les résultats.

5. **Gestion des Anonymats** :
   - Attribution et récupération des anonymats pour les candidats.
   - Gestion des anonymats pour les épreuves.

6. **Repêchage** :
   - Affichage des candidats repêchables pour le premier et le second tour.
   - Gestion des candidats repêchables en fonction des notes et des critères.

7. **Relevé de Notes** :
   - Génération des relevés de notes pour chaque candidat.
   - Exportation des relevés de notes en format PDF.

8. **Impression en PDF** :
   - Génération de fichiers PDF pour la liste des candidats, les PV de délibération, et les relevés de notes.
   - Ouverture automatique des fichiers PDF générés.

9. **Gestion du Second Tour** :
   - Saisie des notes pour les candidats repêchables au second tour.
   - Délibération des résultats du second tour.

## Installation et Exécution

### Prérequis

- **Python 3.x** : Le projet nécessite Python 3.x pour fonctionner.
- **Bibliothèques Python** : Les bibliothèques suivantes doivent être installées :
  - `tkinter` : Pour l'interface graphique.
  - `sqlite3` : Pour la gestion de la base de données.
  - `matplotlib` : Pour la génération de graphiques.
  - `reportlab` : Pour la génération de fichiers PDF.

### Étapes d'Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-utilisateur/gestion-bfem.git
   cd gestion-bfem
   
#### Installer les dépendance et execution

  pip install -r requirements.txt
Exécuter l'application sur pycharm :
  python main.py
Exécuter l'application sur le fichier directe dans dist avec GestionBfem.exec


##### Utilisation
1.Connexion :
L'application démarre sur la page de connexion. Utilisez les identifiants par défaut (admin / admin) pour accéder à l'interface principale.

2.Navigation :

L'interface principale offre un menu de navigation pour accéder aux différentes fonctionnalités (candidats, jury, délibération, statistiques, etc.).

Chaque page propose des boutons pour effectuer des actions spécifiques (ajouter, modifier, supprimer, générer des rapports, etc.).

Gestion des Candidats :

Vous pouvez ajouter, modifier, supprimer et consulter les candidats via les pages dédiées.

Les informations des candidats sont stockées dans la base de données SQLite.

Délibération :

La page de délibération permet de calculer les points des candidats et de déterminer leur résultat (admis, second tour, échoués, repêchables).

Vous pouvez également gérer les candidats repêchables pour le second tour.

Statistiques :

La page des statistiques affiche des graphiques et des données sur les résultats des candidats.

Vous pouvez exporter ces statistiques en format PDF.

Impression en PDF :

Vous pouvez générer des fichiers PDF pour la liste des candidats, les PV de délibération, et les relevés de notes.

Les fichiers PDF sont automatiquement ouverts après leur génération.

###### Auteurs
[Atta fall] 

[Pape malick thiam] 

[Yacine ndiaga sam secck] 


