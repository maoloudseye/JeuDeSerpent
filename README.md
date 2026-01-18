# **🐍 Serpent Pro**

Un jeu du serpent moderne et amélioré développé avec Python et Pygame.

Afficher l'image
Afficher l'image
Afficher l'image

# **📋 Description**

Serpent Pro est une version améliorée du jeu classique Snake avec de nombreuses fonctionnalités modernes : système de niveaux, bonus spéciaux, effets visuels, sauvegarde du high score et plus encore.

# **✨ Fonctionnalités**

## **🎮 Gameplay**

- Système de niveaux progressifs - La difficulté augmente avec votre score  
- Bonus spéciaux apparaissant aléatoirement :
  - 🟡 Nourriture dorée : +50 points et croissance x2
  - 🔵 Ralentisseur : Vitesse réduite temporairement + invincibilité
  - 🟣 Accélérateur : Boost de vitesse pour plus de challenge
- High score sauvegardé automatiquement

## **🎨 Visuels**

- Effets de particules lors de la collecte
- Animations fluides
- Ombres portées
- Dégradé sur le corps du serpent
- Yeux animés selon la direction
- Grille de fond élégante
- Interface HUD complète

## **🎯 Modes de jeu**

- Menu principal avec instructions
- Mode pause
- Écran Game Over avec statistiques

# **🚀 Installation**

### Prérequis

- Python 3.8 ou supérieur
- Pygame 2.0 ou supérieur

### Étapes d'installation

Clonez le dépôt :

```bash
git clone https://github.com/votre-username/serpent-pro.git
cd serpent-pro
```

Installez les dépendances :

```bash
pip install pygame
```

Lancez le jeu :

```bash
python jeu.py
```

# **🎮 Contrôles**

- Touche → ↑ ↓ ← : Diriger le serpent  
- ESPACE : Démarrer / Rejouer  
- P : Pause  
- ESC : Quitter / Retour au menu

# **📊 Système de points**

- Nourriture normale : +10 points  
- Nourriture dorée : +50 points  
- Ralentisseur : +20 points  
- Accélérateur : +30 points  
- Nouveau niveau tous les 100 points

# **🏆 Fonctionnalités techniques**

- Sauvegarde automatique du high score dans `snake_score.json`  
- Gestion fluide des collisions  
- Système de particules pour les effets visuels  
- Augmentation progressive de la vitesse par niveau  
- Téléportation aux bords de l'écran

# **📁 Structure du projet**

```
serpent-pro/
│
├── jeu.py              # Fichier principal du jeu
├── snake_score.json    # Fichier de sauvegarde (généré automatiquement)
└── README.md           # Ce fichier
```

# **🛠️ Technologies utilisées**

- Python - Langage de programmation  
- Pygame - Bibliothèque de développement de jeux  
- JSON - Sauvegarde des données

# **📝 Améliorations futures**

- Système de sons et musique  
- Plusieurs modes de difficulté  
- Power-ups supplémentaires  
- Obstacles sur la carte  
- Multijoueur local  
- Thèmes visuels personnalisables  
- Leaderboard en ligne

# **🤝 Contribution**

Les contributions sont les bienvenues ! N'hésitez pas à :

- Fork le projet  
- Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)  
- Commit vos changements (`git commit -m 'Add some AmazingFeature'`)  
- Push vers la branche (`git push origin feature/AmazingFeature`)  
- Ouvrir une Pull Request

# **📜 Licence**

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

# **👤 Auteur**

Votre Nom

GitHub: @votre-username

# **🙏 Remerciements**

Inspiré du jeu classique Snake  
Développé avec ❤️ et Python

⭐ N'oubliez pas de mettre une étoile si vous aimez ce projet !
