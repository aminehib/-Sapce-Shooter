## -*- coding: utf-8 -*-

import pygame
import time
import random

pygame.init() # initialisation du module "pygame"

fenetre = pygame.display.set_mode( (600,600) ) # Création d'une fenêtre graphique de taille 600x600 pixels
pygame.display.set_caption("Pygame hibaoui") # Définit le titre de la fenêtre


## Chargement des images:
#    On définit et affecte les variables qui contiendront les images du vaisseau ou de l'alien
imageAlien = pygame.image.load("alien.png")
imageVaisseau = pygame.image.load("vaisseau.png")
background = pygame.image.load("background.png")
endscreen = pygame.image.load("endscreen.png")
imageBombe = pygame.image.load("bombe.png")
imageVaisseau = pygame.transform.scale(imageVaisseau, (64, 64)) # On redimensionne l'image du vaisseau à une taille de 64x64 pixels
imageBombe = pygame.transform.scale(imageBombe, (30, 30))
score=0 #score
kills=0 #kills
nb_projectile=100 #proj
hearts=3 #vie s
t0=0 #cooldown
t1=time.time() #cooldown
t0+=1000 #cooldown
v=0 #proj
x=1 #proj
l=0 #bonus
trc1=1 #bonus
t00=0 #bonus cooldown
t11=time.time() #bonus cooldown
t111=time.time() #proj cooldown
t000=0 #proj cooldown
t000+=1000 #proj cooldown
# On définit les variables qui contiendront les positions des différents éléments (vaisseau, alien, projectile)
# Chaque position est un couple de valeur '(x,y)'
positionVaisseau = (300,425)
positionAlien = [(9,50), (79,20), (159,50), (229,20), (309,50),(79,75),(229,75)]
projectile = [(-1,-1)]
bombe=[(-30,-30)]
bonus=[(-30,-30)]
arial24 = pygame.font.SysFont("mono",17)
arial25 = pygame.font.SysFont("mono",30)



# Fonction en charge de dessiner tous les éléments sur notre fenêtre graphique.
# Cette fonction sera appelée depuis notre boucle infinie
def dessiner(end):
    global imageAlien, imageVaisseau, fenetre, projectile,vies,n, imageBombe
    # On remplit complètement notre fenêtre avec la couleur noire: (0,0,0)
    # Ceci permet de 'nettoyer' notre fenêtre avant de la dessiner
    fenetre.blit(background, (0,0))
    fenetre.blit(imageVaisseau, positionVaisseau)
    for i in range(len(positionAlien)):
        fenetre.blit(imageAlien, positionAlien[i])  # On dessine l'image du vaisseau à sa position
    texteScore = arial24.render("kills : "+str(kills),True,pygame.Color(0,0,0))
    texteProjectile=arial24.render("Nbr Projectiles : "+str(nb_projectile),True,pygame.Color(0,0,0))
    textehearts = arial24.render("Hearts : "+str(hearts),True,pygame.Color(0,0,0))
    fenetre.blit(texteScore,(15,530))
    fenetre.blit(texteProjectile,(15,550))

    if end==1:
        score= kills*100+hearts*250
        texteScore = arial25.render("score : "+str(score),True,pygame.Color(255,255,255))
        fenetre.blit(endscreen, (150,200))
        fenetre.blit(texteScore,(190,290))
        for i in range(len(positionAlien)):
            positionAlien[i] = (positionAlien[i][0],600)



    for i in range(len(projectile)):
        if projectile[i] != (-1, -1):
            pygame.draw.circle(fenetre, (255,255,255), projectile[i], 5) # On dessine le projectile (un simple petit cercle)
    for i in range(len(bombe)):
        if bombe[i] != (601,601):
            fenetre.blit(imageBombe, bombe[i])
    for i in range(len(bonus)):
        if bonus[i] != (-30, -30):
            pygame.draw.circle(fenetre, (0,0,255), bonus[i], 10)
    pygame.display.flip() # Rafraichissement complet de la fenêtre avec les dernières opérations de dessin


# Fonction en charge de gérer les évènements clavier (ou souris)
# Cette fonction sera appelée depuis notre boucle infinie
trc=1
def gererClavierEtSouris():
    global continuer, positionVaisseau, projectile,nb_projectile,trc,score, t000, t111
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Permet de gérer un clic sur le bouton de fermeture de la fenêtre
            continuer = 0
    # Gestion du clavier: Quelles touches sont pressées ?
    touchesPressees = pygame.key.get_pressed()
    start=time.time()
    end=0
    t000=time.time()
    if hearts !=0 and end !=1:
        for i in range(len(projectile)):
            if touchesPressees[pygame.K_SPACE] == True and nb_projectile>0 and projectile[i]==(-1,-1) and t000-t111>0.2:

                    projectile[i] = (positionVaisseau[0]+32,positionVaisseau[1])
                    projectile.append((-1,-1))
                    t111=time.time()
                    nb_projectile-=1


        if touchesPressees[pygame.K_RIGHT] == True and positionVaisseau[0]<600-64:
            positionVaisseau = ( positionVaisseau[0] + 5 , positionVaisseau[1] )
        if touchesPressees[pygame.K_LEFT] == True and positionVaisseau[0]>0:
            positionVaisseau = ( positionVaisseau[0] - 5 , positionVaisseau[1] )
    if trc%100==0:
        z=random.randint(0,len(positionAlien)-1)
        while 25< positionAlien[z][1]>500:
            z=random.randint(0,len(positionAlien)-1)

        bombe[int(trc/100)-1] = (positionAlien[z][0]+10,positionAlien[z][1])
        bombe.append((-30,-30))
        fenetre.blit(imageBombe, bombe[0])
    trc+=1

# On crée une nouvelle horloge qui nous permettra de fixer la vitesse de rafraichissement de notre fenêtre
clock = pygame.time.Clock()

# La boucle infinie de pygame:
# On va continuellement dessiner sur la fenêtre, gérer les évènements et calculer certains déplacements
continuer = 1
tr=0
y=0
end=0
tb=0
while continuer==1:
    # pygame permet de fixer la vitesse de notre boucle:
    # ici on déclare 50 tours par secondes soit une animation à 50 images par secondes
    clock.tick(70)
    bombetime1=time.time()
    dessiner(end)
    gererClavierEtSouris()
    for i in range(len(positionAlien)):
        if positionAlien[i][0]<10:
            t=0
            tr+=1
            tb+=1
            for j in range(len(positionAlien)):
                if positionAlien[j][1]<500:
                    positionAlien[j]= (positionAlien[j][0], positionAlien[j][1]+15)
        elif positionAlien[i][0]>550:
            t=1
            tr+=1
            tb+=1
            for j in range(len(positionAlien)):
                if positionAlien[j][1]<500:
                    positionAlien[j]= (positionAlien[j][0], positionAlien[j][1]+15)
        if t==0:
            positionAlien[i]= (positionAlien[i][0]+2*(1+tr/10), positionAlien[i][1])
        else:
            positionAlien[i]= (positionAlien[i][0]-2*(1+tr/10), positionAlien[i][1])



    # On fait avancer le projectile (si il existe)
    for i in range(len(projectile)):
        if projectile[i][1]>5:
            projectile[i] = (projectile[i][0], projectile[i][1] - 5) # le projectile "monte" vers le haut de la fenêtre
        for j in range(len(positionAlien)):
            if positionAlien[j][0]<=projectile[i][0]<=positionAlien[j][0]+33 and positionAlien[j][1]<=projectile[i][1]<=positionAlien[j][1]+27:
                projectile[i]=(-1,-1)
                positionAlien[j] = (positionAlien[j][0],-50)
                kills+=1


        if projectile[i][1]<0:
            projectile[i]=(-1,-1)
    while (-1,5) in projectile:
        projectile.remove((-1,5))
    while (-1,-1) in projectile:
        projectile.remove((-1,-1))
    projectile.append((-1,-1))
    for k in range(len(projectile)): #pour que le jeu s'arrete des que toutes les balles sont en -1 # marche pas
        if projectile[k][0] == -1:
            v=1
        else:
            v=0
        if nb_projectile==0 and v==1:
           end=1
    t0=time.time()
    for i in range(len(bombe)):
        if bombe[i][1]<620 and bombe[i][0]!=-30:
            bombe[i] = (bombe[i][0], bombe[i][1] + 5)
        if bombe[i][1]>480:
            bombe[i]=(bombe[i][0], 610)
        if positionVaisseau[0]<=bombe[i][0]<=positionVaisseau[0]+64 and positionVaisseau[1]<=bombe[i][1]<=positionVaisseau[1]+80 and t0-t1>2:
            t1=time.time()
            hearts-=1
            bombe[i]=(bombe[i][0], 610)
            if hearts==0:
                end=1
                imageVaisseau = pygame.image.load("vaisseau.png")
            if hearts==2:
                imageVaisseau = pygame.image.load("vaisseau.png")
            if hearts==1:
                imageVaisseau = pygame.image.load("vaisseau.png")

    for i in range(len(positionAlien)):
        if positionAlien[i][1]>400 and positionAlien[i][1]<600:
            hearts=0
            imageVaisseau = pygame.image.load("vaisseau.png")


    for i in range(len(projectile)):
        if projectile[i][1]<=5:
            projectile[i] = (-1, projectile[i][1])



    if trc1%500==0:
        l=random.randint(0,len(positionAlien)-1)
        while 0< positionAlien[l][1]>600:
            l=random.randint(0,len(positionAlien)-1)
        bonus[int(trc/500)-1] = (int(positionAlien[l][0]+10),int(positionAlien[l][1]))
        bonus.append((-30,-30))
    trc1+=1
    t00=time.time()
    for i in range(len(bonus)):
        if bonus[i][1]<620 and bonus[i][0]!=-30:
            bonus[i] = (bonus[i][0], bonus[i][1] + 5)
        if bonus[i][1]>480:
            bonus[i]=(bonus[i][0], 610)
        if positionVaisseau[0]<=bonus[i][0]<=positionVaisseau[0]+64 and positionVaisseau[1]<=bonus[i][1]<=positionVaisseau[1]+80 and t00-t11>2:
            t11=time.time()
            nb_projectile+=10
            bonus[i]= (bonus[i][0],bonus[i][1]+200)

    for i in range(len(positionAlien)):
        if positionAlien[i][1]>400:
            end=1

    for i in range(len(bonus)):
        if bonus[i][1]>500:
            bonus[i]= (bonus[i][0],bonus[i][1]+200)