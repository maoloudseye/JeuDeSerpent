import pygame
import random
import sys
import json
import os

pygame.init()

# Configuration
LARGEUR = 800
HAUTEUR = 600
TAILLE_CASE = 20
FPS_BASE = 8

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (50, 205, 50)
ROUGE = (220, 20, 60)
VERT_FONCE = (34, 139, 34)
OR = (255, 215, 0)
BLEU = (30, 144, 255)
VIOLET = (138, 43, 226)
GRIS = (128, 128, 128)
GRIS_FONCE = (40, 40, 40)

# Vecteurs directionnels
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# États du jeu
MENU = 0
JOUER = 1
PAUSE = 2
GAME_OVER = 3

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption('Serpent Pro 🐍')
horloge = pygame.time.Clock()


class Particule:
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.couleur = couleur
        self.vie = 30
        self.taille = random.randint(3, 6)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vie -= 1
        self.vy += 0.2

    def dessiner(self, surface):
        alpha = int(255 * (self.vie / 30))
        couleur_alpha = (*self.couleur[:3], alpha)
        pygame.draw.circle(surface, self.couleur, (int(self.x), int(self.y)), self.taille)


class Bonus:
    def __init__(self, type_bonus):
        self.type = type_bonus
        self.position = (0, 0)
        self.temps_vie = 200
        self.randomiser_position()
        
        if type_bonus == "golden":
            self.couleur = OR
            self.points = 50
        elif type_bonus == "speed_down":
            self.couleur = BLEU
            self.points = 20
        elif type_bonus == "speed_up":
            self.couleur = VIOLET
            self.points = 30

    def randomiser_position(self):
        self.position = (
            random.randint(0, LARGEUR // TAILLE_CASE - 1) * TAILLE_CASE,
            random.randint(0, HAUTEUR // TAILLE_CASE - 1) * TAILLE_CASE,
        )

    def update(self):
        self.temps_vie -= 1
        return self.temps_vie > 0

    def dessiner(self, surface):
        r = pygame.Rect(self.position[0], self.position[1], TAILLE_CASE, TAILLE_CASE)
        
        # Effet de clignotement
        if self.temps_vie < 50 and self.temps_vie % 10 < 5:
            return
            
        # Ombre
        ombre = pygame.Rect(self.position[0] + 2, self.position[1] + 2, TAILLE_CASE, TAILLE_CASE)
        pygame.draw.rect(surface, GRIS_FONCE, ombre, border_radius=5)
        
        pygame.draw.rect(surface, self.couleur, r, border_radius=5)
        pygame.draw.rect(surface, BLANC, r, 2, border_radius=5)


class Serpent:
    def __init__(self):
        self.longueur = 1
        self.positions = [(LARGEUR // 2, HAUTEUR // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.couleur_tete = VERT
        self.invincible = 0

    def obtenir_tete(self):
        return self.positions[0]

    def tourner(self, direction):
        if self.longueur > 1 and (direction[0] == -self.direction[0] and direction[1] == -self.direction[1]):
            return
        self.direction = direction

    def deplacer(self):
        x, y = self.direction
        tete_x, tete_y = self.obtenir_tete()

        nouvelle_tete = (
            (tete_x + x * TAILLE_CASE) % LARGEUR,
            (tete_y + y * TAILLE_CASE) % HAUTEUR
        )

        # Collision avec le corps (sauf si invincible)
        if self.invincible <= 0 and len(self.positions) > 2 and nouvelle_tete in self.positions[2:]:
            return False

        self.positions.insert(0, nouvelle_tete)
        if len(self.positions) > self.longueur:
            self.positions.pop()

        if self.invincible > 0:
            self.invincible -= 1

        return True

    def reinitialiser(self):
        self.longueur = 1
        self.positions = [(LARGEUR // 2, HAUTEUR // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.invincible = 0

    def dessiner(self, surface):
        for i, p in enumerate(self.positions):
            if i == 0:
                # Tête avec effet brillant
                couleur = self.couleur_tete if self.invincible <= 0 else BLEU
                r = pygame.Rect(p[0], p[1], TAILLE_CASE, TAILLE_CASE)
                pygame.draw.rect(surface, couleur, r, border_radius=8)
                pygame.draw.rect(surface, BLANC, r, 2, border_radius=8)
                
                # Yeux
                eye_size = 3
                if self.direction == UP:
                    pygame.draw.circle(surface, BLANC, (p[0] + 6, p[1] + 6), eye_size)
                    pygame.draw.circle(surface, BLANC, (p[0] + 14, p[1] + 6), eye_size)
                elif self.direction == DOWN:
                    pygame.draw.circle(surface, BLANC, (p[0] + 6, p[1] + 14), eye_size)
                    pygame.draw.circle(surface, BLANC, (p[0] + 14, p[1] + 14), eye_size)
                elif self.direction == LEFT:
                    pygame.draw.circle(surface, BLANC, (p[0] + 6, p[1] + 6), eye_size)
                    pygame.draw.circle(surface, BLANC, (p[0] + 6, p[1] + 14), eye_size)
                else:
                    pygame.draw.circle(surface, BLANC, (p[0] + 14, p[1] + 6), eye_size)
                    pygame.draw.circle(surface, BLANC, (p[0] + 14, p[1] + 14), eye_size)
            else:
                # Corps avec dégradé
                intensite = 255 - int((i / len(self.positions)) * 100)
                couleur = (0, max(155, intensite), 0)
                r = pygame.Rect(p[0], p[1], TAILLE_CASE, TAILLE_CASE)
                pygame.draw.rect(surface, couleur, r, border_radius=5)
                pygame.draw.rect(surface, VERT_FONCE, r, 1, border_radius=5)

    def grandir(self):
        self.longueur += 1


class Nourriture:
    def __init__(self):
        self.position = (0, 0)
        self.couleur = ROUGE
        self.randomiser_position()

    def randomiser_position(self):
        self.position = (
            random.randint(0, LARGEUR // TAILLE_CASE - 1) * TAILLE_CASE,
            random.randint(0, HAUTEUR // TAILLE_CASE - 1) * TAILLE_CASE,
        )

    def dessiner(self, surface):
        r = pygame.Rect(self.position[0], self.position[1], TAILLE_CASE, TAILLE_CASE)
        
        # Ombre
        ombre = pygame.Rect(self.position[0] + 2, self.position[1] + 2, TAILLE_CASE, TAILLE_CASE)
        pygame.draw.rect(surface, GRIS_FONCE, ombre, border_radius=8)
        
        pygame.draw.circle(surface, self.couleur, 
                          (self.position[0] + TAILLE_CASE//2, self.position[1] + TAILLE_CASE//2), 
                          TAILLE_CASE//2)
        pygame.draw.circle(surface, (255, 100, 100), 
                          (self.position[0] + TAILLE_CASE//2, self.position[1] + TAILLE_CASE//2), 
                          TAILLE_CASE//2, 2)


class Jeu:
    def __init__(self):
        self.serpent = Serpent()
        self.nourriture = Nourriture()
        self.score = 0
        self.niveau = 1
        self.etat = MENU
        self.bonus_actif = None
        self.compteur_bonus = 0
        self.fps = FPS_BASE
        self.modificateur_vitesse = 0
        self.particules = []
        self.high_score = self.charger_high_score()

    def charger_high_score(self):
        try:
            if os.path.exists('snake_score.json'):
                with open('snake_score.json', 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except:
            pass
        return 0

    def sauvegarder_high_score(self):
        try:
            with open('snake_score.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass

    def creer_particules(self, x, y, couleur):
        for _ in range(10):
            self.particules.append(Particule(x + TAILLE_CASE//2, y + TAILLE_CASE//2, couleur))

    def gerer_bonus(self):
        self.compteur_bonus += 1
        
        # Créer un nouveau bonus tous les 300 frames
        if self.compteur_bonus > 300 and self.bonus_actif is None:
            type_bonus = random.choice(["golden", "speed_down", "speed_up"])
            self.bonus_actif = Bonus(type_bonus)
            self.compteur_bonus = 0

        # Mettre à jour le bonus actif
        if self.bonus_actif:
            if not self.bonus_actif.update():
                self.bonus_actif = None
            elif self.serpent.obtenir_tete() == self.bonus_actif.position:
                self.creer_particules(self.bonus_actif.position[0], self.bonus_actif.position[1], 
                                     self.bonus_actif.couleur)
                self.score += self.bonus_actif.points
                
                if self.bonus_actif.type == "golden":
                    self.serpent.grandir()
                    self.serpent.grandir()
                elif self.bonus_actif.type == "speed_down":
                    self.modificateur_vitesse = -2
                    self.serpent.invincible = 50
                elif self.bonus_actif.type == "speed_up":
                    self.modificateur_vitesse = 3
                
                self.bonus_actif = None

    def update(self):
        if self.etat != JOUER:
            return

        # Déplacer le serpent
        if not self.serpent.deplacer():
            self.etat = GAME_OVER
            if self.score > self.high_score:
                self.high_score = self.score
                self.sauvegarder_high_score()
            return

        # Vérifier si le serpent mange
        if self.serpent.obtenir_tete() == self.nourriture.position:
            self.serpent.grandir()
            self.score += 10
            self.creer_particules(self.nourriture.position[0], self.nourriture.position[1], ROUGE)
            self.nourriture.randomiser_position()
            
            # Augmenter le niveau
            if self.score % 100 == 0:
                self.niveau += 1
                self.fps = FPS_BASE + (self.niveau - 1)

        # Gérer les bonus
        self.gerer_bonus()

        # Mettre à jour les particules
        self.particules = [p for p in self.particules if p.vie > 0]
        for p in self.particules:
            p.update()

        # Réinitialiser le modificateur de vitesse
        if self.modificateur_vitesse != 0:
            self.modificateur_vitesse = max(0, self.modificateur_vitesse - 0.1)

    def dessiner(self):
        # Fond avec grille
        ecran.fill(NOIR)
        for x in range(0, LARGEUR, TAILLE_CASE):
            pygame.draw.line(ecran, (20, 20, 20), (x, 0), (x, HAUTEUR))
        for y in range(0, HAUTEUR, TAILLE_CASE):
            pygame.draw.line(ecran, (20, 20, 20), (0, y), (LARGEUR, y))

        if self.etat == MENU:
            self.afficher_menu()
        elif self.etat == JOUER or self.etat == PAUSE:
            self.serpent.dessiner(ecran)
            self.nourriture.dessiner(ecran)
            if self.bonus_actif:
                self.bonus_actif.dessiner(ecran)
            
            # Dessiner les particules
            for p in self.particules:
                p.dessiner(ecran)
            
            self.afficher_hud()
            
            if self.etat == PAUSE:
                self.afficher_pause()
        elif self.etat == GAME_OVER:
            self.afficher_game_over()

    def afficher_hud(self):
        police = pygame.font.Font(None, 32)
        
        # Score
        texte_score = police.render(f"Score: {self.score}", True, BLANC)
        ecran.blit(texte_score, (10, 10))
        
        # Niveau
        texte_niveau = police.render(f"Niveau: {self.niveau}", True, OR)
        ecran.blit(texte_niveau, (10, 45))
        
        # High Score
        texte_high = police.render(f"Record: {self.high_score}", True, VERT)
        ecran.blit(texte_high, (LARGEUR - 200, 10))
        
        # Longueur
        texte_longueur = police.render(f"Longueur: {self.serpent.longueur}", True, BLEU)
        ecran.blit(texte_longueur, (LARGEUR - 200, 45))

    def afficher_pause(self):
        overlay = pygame.Surface((LARGEUR, HAUTEUR))
        overlay.set_alpha(200)
        overlay.fill(NOIR)
        ecran.blit(overlay, (0, 0))
        
        police = pygame.font.Font(None, 72)
        texte = police.render("PAUSE", True, OR)
        ecran.blit(texte, texte.get_rect(center=(LARGEUR // 2, HAUTEUR // 2)))
        
        police_small = pygame.font.Font(None, 36)
        texte_info = police_small.render("Appuyez sur P pour continuer", True, BLANC)
        ecran.blit(texte_info, texte_info.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 60)))

    def afficher_menu(self):
        police_titre = pygame.font.Font(None, 84)
        texte_titre = police_titre.render("🐍 SERPENT PRO 🐍", True, VERT)
        ecran.blit(texte_titre, texte_titre.get_rect(center=(LARGEUR // 2, 150)))
        
        police = pygame.font.Font(None, 42)
        texte_start = police.render("Appuyez sur ESPACE pour commencer", True, BLANC)
        ecran.blit(texte_start, texte_start.get_rect(center=(LARGEUR // 2, 300)))
        
        police_small = pygame.font.Font(None, 28)
        texte_high = police_small.render(f"Record actuel: {self.high_score}", True, OR)
        ecran.blit(texte_high, texte_high.get_rect(center=(LARGEUR // 2, 380)))
        
        # Instructions
        instructions = [
            "Utilisez les FLÈCHES pour diriger le serpent",
            "P pour pause | ESC pour quitter",
            "🟡 Bonus doré (+50 pts) | 🔵 Ralentisseur | 🟣 Accélérateur"
        ]
        y = 450
        for inst in instructions:
            texte_inst = police_small.render(inst, True, GRIS)
            ecran.blit(texte_inst, texte_inst.get_rect(center=(LARGEUR // 2, y)))
            y += 35

    def afficher_game_over(self):
        overlay = pygame.Surface((LARGEUR, HAUTEUR))
        overlay.set_alpha(200)
        overlay.fill(NOIR)
        ecran.blit(overlay, (0, 0))
        
        police = pygame.font.Font(None, 84)
        texte = police.render("GAME OVER", True, ROUGE)
        ecran.blit(texte, texte.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 80)))

        police_medium = pygame.font.Font(None, 48)
        texte_score = police_medium.render(f"Score final: {self.score}", True, BLANC)
        ecran.blit(texte_score, texte_score.get_rect(center=(LARGEUR // 2, HAUTEUR // 2)))
        
        texte_niveau = police_medium.render(f"Niveau atteint: {self.niveau}", True, OR)
        ecran.blit(texte_niveau, texte_niveau.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 50)))
        
        if self.score == self.high_score and self.score > 0:
            texte_record = police_medium.render("🏆 NOUVEAU RECORD ! 🏆", True, OR)
            ecran.blit(texte_record, texte_record.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 100)))

        police_small = pygame.font.Font(None, 36)
        texte_rejouer = police_small.render("ESPACE: Rejouer | ESC: Menu", True, BLANC)
        ecran.blit(texte_rejouer, texte_rejouer.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 160)))

    def reinitialiser(self):
        self.serpent.reinitialiser()
        self.nourriture.randomiser_position()
        self.score = 0
        self.niveau = 1
        self.fps = FPS_BASE
        self.bonus_actif = None
        self.compteur_bonus = 0
        self.modificateur_vitesse = 0
        self.particules = []


def main():
    jeu = Jeu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if jeu.etat == GAME_OVER:
                        jeu.etat = MENU
                    else:
                        pygame.quit()
                        sys.exit()
                
                if jeu.etat == MENU and event.key == pygame.K_SPACE:
                    jeu.reinitialiser()
                    jeu.etat = JOUER
                
                elif jeu.etat == GAME_OVER and event.key == pygame.K_SPACE:
                    jeu.reinitialiser()
                    jeu.etat = JOUER
                
                elif jeu.etat == JOUER:
                    if event.key == pygame.K_p:
                        jeu.etat = PAUSE
                    elif event.key == pygame.K_UP:
                        jeu.serpent.tourner(UP)
                    elif event.key == pygame.K_DOWN:
                        jeu.serpent.tourner(DOWN)
                    elif event.key == pygame.K_LEFT:
                        jeu.serpent.tourner(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        jeu.serpent.tourner(RIGHT)
                
                elif jeu.etat == PAUSE and event.key == pygame.K_p:
                    jeu.etat = JOUER

        jeu.update()
        jeu.dessiner()
        pygame.display.update()
        
        fps_actuel = jeu.fps + jeu.modificateur_vitesse
        horloge.tick(max(5, fps_actuel))


if __name__ == "__main__":
    main()
