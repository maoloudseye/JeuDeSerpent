Serpent Pro
Un jeu du serpent moderne et amélioré développé avec Python et Pygame.
Description
Serpent Pro est une version améliorée du jeu classique Snake avec de nombreuses fonctionnalités modernes : système de niveaux, bonus spéciaux, effets visuels, sauvegarde du high score et plus encore.
Fonctionnalités
Gameplay

Système de niveaux progressifs - La difficulté augmente avec votre score
Bonus spéciaux apparaissant aléatoirement :

Nourriture dorée : +50 points et croissance x2
Ralentisseur : Vitesse réduite temporairement + invincibilité
Accélérateur : Boost de vitesse pour plus de challenge


High score sauvegardé automatiquement

Modes de jeu

Menu principal avec instructions
Mode pause
Écran Game Over avec statistiques

Installation
Prérequis

Python 3.8 ou supérieur
Pygame 2.0 ou supérieur

Étapes d'installation

Clonez le dépôt :

bashgit clone https://github.com/maoloudseye/JeuDeSerpent.git
cd serpent-pro

Installez les dépendances :

bashpip install pygame

Lancez le jeu :

bashpython jeu.py
Contrôles

Flèches directionnelles : Diriger le serpent
ESPACE : Démarrer / Rejouer
P : Pause
ESC : Quitter / Retour au menu

Système de points

Nourriture normale : +10 points
Nourriture dorée : +50 points
Ralentisseur : +20 points
Accélérateur : +30 points
Nouveau niveau tous les 100 points

Fonctionnalités techniques

Sauvegarde automatique du high score dans snake_score.json
Gestion fluide des collisions
Système de particules pour les effets visuels
Augmentation progressive de la vitesse par niveau
Téléportation aux bords de l'écran
