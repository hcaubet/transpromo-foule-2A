## Fichier Individu.py
## Creation et suppression d'individus, gestion des interactions avec leur environnement

from Vect2D import *
from math import floor
import numpy as np
import random as rd
import Variables as Var


class individu:
    def __init__(self, pos, dpos, vmoy, r, canvas, color):
        self.pos = pos          # Position de chaque individu
        self.dpos = dpos        # Vitesse de chaque individu
        self.r = r              # Rayon de chaque individu
        self.vmoy = Var.dimCase*Var.TpsRaffraichissement/1000.0*Var.multipleVitesse        # Vitesse moyenne d'un individu
        self.canvas = canvas    # Le Canevas sur lequel on dessine
        self.color = color      # Couleur de chaque individu
        self.flightAssert = False
        self.flightState = False
        self.id = canvas.create_oval(-1 * r, -1 * r, r, r, fill = color, outline = color) #Représentation graphique
        self.canvas.move(self.id, pos.x, pos.y) #On le place à sa position
    
    def bouge(self):
        '''deplace un individu de dpos'''
        self.canvas.move(self.id, self.dpos.x, self.dpos.y)
        self.pos += self.dpos
        return
    
    def rafraichir(self,color):
        self.canvas.itemconfig(self.id, fill = color, outline = "black")
        if color=="yellow":
            self.vmoy=0.4*Var.dimCase*Var.TpsRaffraichissement/1000.0*Var.multipleVitesse  
        elif color=="orange":
            self.vmoy=0.2*Var.dimCase*Var.TpsRaffraichissement/1000.0*Var.multipleVitesse  
        if color=="red":
            self.vmoy=-1
        return
    
    def refFlightState(self,fs):
        self.flightAssert=True
        if fs == True:
            self.flightState=True
            self.canvas.itemconfig(self.id, fill="darkgray")
            self.vmoy =0.7*Var.dimCase*Var.TpsRaffraichissement/1000.0*Var.multipleVitesse  
            
        return

# Fonction de gestion du nombre d'individu
def init_indiv(terrain):
    supprime_indiv(terrain)
    for i in range(Var.NIndiv):
        # Afin d'éviter que des individus se retrouve a moitie dans un mur on genere sur un intervalle ou chacun d'eux est pleinement dans une case
        while 1 :
            x = rd.uniform(Var.rIndiv, (Var.largeur - 1) * Var.dimCase - Var.rIndiv)
            y = rd.uniform(Var.rIndiv, (Var.hauteur - 1) * Var.dimCase - Var.rIndiv)
            if Var.TCase[floor(y / Var.dimCase), floor(x / Var.dimCase)].type >= 0 :
                break
        pose_indiv(x, y, terrain,"blue")
    return

def changement_couleur(attribut, valeur):
    
    individu.color=valeur
    individu.canvas.itemconfig(fill=valeur)
    
#Fonction d'évaluation de la densité
def renvoie_densite(terrain):
    for x in range(Var.largeur):
        for y in range(Var.hauteur): 
            activateImmFlight= False
            activateRepFlight = False
            density=0
            for i in Var.LIndivDangereux:
                if (floor(i.pos.y/Var.dimCase)==y and floor(i.pos.x/Var.dimCase)==x) : 
                    activateImmFlight=True;
                    Var.TCase[y,x].hasDanger = True
            for i in Var.LIndiv:
                a =rd.randint(1,100)
                if (floor(i.pos.y/Var.dimCase)==y and floor(i.pos.x/Var.dimCase)==x) :   
                    if (activateImmFlight==True or activateRepFlight==True):
                        if activateImmFlight == True:
                            death = rd.randint(1,100)
                            if death<=50:
                                terrain.delete(i.id)
                                Var.LIndiv.remove(i)
                                Var.LMorts.append(i)
                            elif i.flightAssert == False:
                                if a > 30:
                                    i.refFlightState(1)
                                else:
                                    i.refFlightState(0)
                        elif activateRepFlight == True and i.flightAssert == False:
                            if a > 60 :
                                i.refFlightState(1)
                            else:
                                i.refFlightState(0)
                    elif activateImmFlight== False and i.flightState == True:
                        activateRepFlight= True
                    density+=1
                    if density<2 and i.flightState == False:
                        i.rafraichir("blue")
                        if Var.TCase[y,x].type == -3:
                            Var.TCase[y,x].type = 0
                            Var.TCase[y, x].rafraichir()
                            
                    elif density>=2 and density<4 and i.flightState == False :
                        i.rafraichir("yellow")
                        if Var.TCase[y,x].type == -3:
                            Var.TCase[y,x].type = 0
                            Var.TCase[y, x].rafraichir()
                            
                            
                    elif density>=4 and density <6 and i.flightState == False :
                        i.rafraichir("orange")
                        if Var.TCase[y,x].type == 0:
                            Var.TCase[y,x].type = -3
                            Var.TCase[y, x].rafraichir()
                            Var.LSortieD.append([x,y])
                            
                    elif density>=6 and i.flightState == False:
                        i.rafraichir("red")
                        if Var.TCase[y,x].type == 0:
                            Var.TCase[y,x].type = -3
                            Var.TCase[y, x].rafraichir()
                            Var.LSortieD.append([x,y])
                        
                            
              
    return
    

    
def pose_indiv(x, y, terrain, couleur):
    '''Pose un inidividu sur le terrain en (x,y)'''
    pos = vect2D(x, y)
    dpos = vect2D(0, 0)
    indiv=individu(pos, dpos, rd.uniform(Var.vminIndiv, Var.vmaxIndiv), Var.rIndiv, terrain,couleur)
    Var.LIndiv.append(indiv)
    return

def supprime_indiv(terrain):
    '''supprime tous les individus du terrain'''
    for i in Var.LIndiv :
        terrain.delete(i.id)
    Var.LIndiv = []
    return
    
def sortir_indiv(terrain):
    '''Permet de supprimer un individu lorsqu'il a atteint la sortie'''
    for individu in Var.LIndiv :
        x = floor(individu.pos.x / Var.dimCase)
        y = floor(individu.pos.y / Var.dimCase)
        if Var.TCase[y, x].type == 1 :
            terrain.delete(individu.id)
            Var.LIndiv.remove(individu)
    return 
    
# Fonction de gestion des collisions avec les murs, les bords et les autres individus
def touche_indiv(individu1, individu2):
    '''Test si deux individus se touchent'''
    return (individu1.pos - individu2.pos).norme() <= individu1.r + individu2.r

def rebond_indiv(individu1, individu2): 
    '''Lorsqu'il y a collision entre deux individu, calcule les vitesses de chacun après le choc'''
    if p_scal(individu1.dpos, individu2.dpos) < 0 : #Vérifie si les individus ne s'éloignent pas déjà
        return
    
    n = individu1.pos - individu2.pos
    n1 = projection(individu1.dpos, n)
    n2 = projection(individu2.dpos, n)
    
    t1 = individu1.dpos - n1
    t2 = individu2.dpos - n2
    #On conserve les composantes tangentielles et on échange les composantes normales
    individu1.dpos = (t1 + n2)
    individu2.dpos = (t2 + n1)
    
    return
    
def rebond_mur(individu):
    '''Lorsqu'un individu touche un mur, on le fait rebondir en inversant sa vitesse selon les axes de chocs'''
    pos = individu.pos
    r = individu.r
    c = Var.TCase[floor(pos.y / Var.dimCase), floor(pos.x / Var.dimCase)]
    if c.type == -1 :
        if pos.x -r < c.pos.x or pos.x + r > c.pos.x + Var.dimCase :
            individu.dpos.x *= -1
        if pos.y -r < c.pos.y or pos.y + r > c.pos.y + Var.dimCase :
            individu.dpos.y *= -1
    return
    
def rebond_bord(individu):
    '''Lorsqu'un individu touche un mur, on le fait rebondir en inversant sa vitesse selon les axes de chocs'''
    pos = individu.pos
    r = individu.r
    if pos.x -r < 0 or pos.x + r > Var.largeur*Var.dimCase:
        individu.dpos.x *= -1
    if pos.y - r < 0 or pos.y + r > Var.hauteur*Var.dimCase :
        individu.dpos.y *= -1
    return

# Programme de gestion des mouvements
def bouge_indiv2():
    '''Gestion du mouvement des individus en fonction de l'environnement de chacun'''
    for i, individu1 in enumerate(Var.LIndiv) :
        x = floor(individu1.pos.x / Var.dimCase)
        y = floor(individu1.pos.y / Var.dimCase)
        individu1.dpos = individu1.dpos.normalise() * np.random.normal(individu1.vmoy, 0.2)
        if individu1.flightState == False:
            individu1.dpos += Var.Tdirection[y,x]
        for individu2 in Var.LIndiv[i+1:] :
            if touche_indiv(individu1, individu2) :
                rebond_indiv(individu1, individu2)
        rebond_bord(individu1)
        rebond_mur(individu1)
        individu1.bouge()
    return
