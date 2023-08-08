import pygame
import os
import random

pygame.init()

CASELLES_PROPERES = [(-1, 0), (-1, -1),(0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
CAMI_BASE = 'data/images/'
tamany_m = [11, 14]

def cargar_imatge(cami):
    img = pygame.image.load(CAMI_BASE + cami).convert()
    img.set_colorkey((229, 165, 165,255))
    return img

def cargar_imatges(cami):
    images=[]
    for img_name in sorted(os.listdir(CAMI_BASE + cami)):
        images.append(cargar_imatge(cami + "/" + img_name))
    return images

def generar_poma():
    pos = (random.randint(1, tamany_m[0] - 1) , random.randint(4, tamany_m[1] - 1))
    return pos #posicio matriu



#Codi per fer el boto
lletra = pygame.font.SysFont('Arial', 20) #Seleccionem la font dels textos i el tamany d'aquest



class boto():
    def __init__(self, Game, pos, amplada, altura, text='Boto', funcio=None):
        self.pos = pos #posició
        self.amplada = amplada #amplada i altura del botó
        self.altura = altura
        self.text = lletra.render(text, True, (255,255,255)) #creació del text
        self.funcio = funcio
        self.Game = Game

        #Seleccionem els colors que utilitzarem en el boto
        self.colorsBoto = {
            'normal' : (0, 0, 0),
            'sobre' : (80, 80, 80),
            'clicat' : (40, 40, 40)
        }

        self.surfaceBoto = pygame.Surface((self.amplada, self.altura))#Creació de la superficie del botó ( on es renderitza el text )
        self.coliderBoto = pygame.Rect(self.pos[0],self.pos[1],self.amplada, self.altura) #Creació del colider (per detectar si el ratoli toca amb aquest rectangle)
        
        self.clicat = False #Com només volem que el cliqui una vegada fem una variable que només permeti que cliquis el botó una vegada

    
    def proces(self):
        mpos = pygame.mouse.get_pos() #conseguim la posició del ratoli
        mpos = (int(mpos[0]//2), int(mpos[1]//2))
        print(mpos)

        self.surfaceBoto.fill(self.colorsBoto['normal']) #cambien el color del rectangle
        if self.coliderBoto.collidepoint(mpos): #comprobem si el ratolí està a sobre del botó
            self.surfaceBoto.fill(self.colorsBoto['sobre'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:#get pressed necesita una quantitat de botons que te el teu ratolí, després, hauras d'especificar quin botó vols que sigui pressionat
                #al posar el num_buttons=3, crea una llista amb els botons del ratolí, permitint-nos seleccionar un botó en especific per saber si s'ha persionat
                self.surfaceBoto.fill(self.colorsBoto['clicat'])#pintem amb el color asignat
                if not self.clicat:
                    if self.funcio is not None:
                        self.funcio()#Fa la funció que hem elegit avans
                    self.clicat = True #Això és per que no repeteixi self.funcio() infinitament mentres mantenguis pulsat el botó.
            else:
                self.clicat = False #la deixar de clicar, torna al seu estat original
            
        #Renderitzem el text del botó
        self.surfaceBoto.blit(self.text,(self.amplada/2 - self.text.get_rect().width/2, self.altura/2 - self.text.get_rect().height/2))
        #renderitzem el botó
        self.Game.pantalla.blit(self.surfaceBoto, (self.pos[0], self.pos[1]))
