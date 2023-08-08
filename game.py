import pygame 
import sys
import time #això no se si es bona solució, hi ha el clock altre, pero es per quee s mogui per defecte
from scripts.utils import cargar_imatge, cargar_imatges, generar_poma, boto

class Game:

    def __init__(self):
        
        pygame.init()
        self.control_temps = time.time()
        self.clock = pygame.time.Clock()
        self.viu = True
        self.registro_mov = [] #variable auxiliar: sirve para que que no pueda cambiar de dirección contraria

        pygame.display.set_caption('Pitó')

        #nota: un problema pot ser que la poma sorti en la serp, pero es fàcil d'arreglar. 
        self.finestra = pygame.display.set_mode((384, 480))
        self.pantalla = pygame.Surface((192,240))

        #Generació de la primera poma
        self.posicio_poma = generar_poma()

        #Textures del joc
        self.assets = {
            'jugador': cargar_imatges('player'),
            'poma' : cargar_imatge('others/apple.png'),
            'mapa' : cargar_imatge('map/map.png'),
            'fons' : cargar_imatge('menu/fons_menu.png'),
            'titol' : pygame.transform.scale(cargar_imatge('menu/titol.png'),(280,140)),
            'perdut' : pygame.transform.scale(cargar_imatge('menu/perdre.png'),(280,140))
        }
        
        #variables de la serp
        self.tamany_serp_inicial = 3
        self.tamany_serp = self.tamany_serp_inicial
        self.pos = [4, 5]
        self.direccio = 'dreta'
        self.posicions_serp = [tuple(self.pos), (3, 5), (2, 5)]
        self.direccions_posicions_serp = [self.direccio] * self.tamany_serp #la direcció per defecte dos cops.
        self.temps_serp = 0.2
        self.llista_imatges_gir = [pygame.transform.rotate(self.assets['jugador'][5],180), 
                                   pygame.transform.rotate(self.assets['jugador'][3],180), 
                                   pygame.transform.rotate(self.assets['jugador'][4],180), 
                                   pygame.transform.rotate(self.assets['jugador'][2],180), 
                                   pygame.transform.rotate(self.assets['jugador'][2],180), 
                                   pygame.transform.rotate(self.assets['jugador'][3],180), 
                                   pygame.transform.rotate(self.assets['jugador'][4],180), 
                                   pygame.transform.rotate(self.assets['jugador'][5],180),
                                   pygame.transform.rotate(self.assets['jugador'][1],270),
                                   pygame.transform.rotate(self.assets['jugador'][1],90),
                                   pygame.transform.rotate(self.assets['jugador'][1],180),
                                   pygame.transform.rotate(self.assets['jugador'][1],0),
                                   pygame.transform.rotate(self.assets['jugador'][6],270),
                                   pygame.transform.rotate(self.assets['jugador'][6],90),
                                   pygame.transform.rotate(self.assets['jugador'][6],180),
                                   pygame.transform.rotate(self.assets['jugador'][6],0),
                                   
                                   pygame.transform.rotate(self.assets['jugador'][0],90),
                                   pygame.transform.rotate(self.assets['jugador'][0],270),
                                   pygame.transform.rotate(self.assets['jugador'][0],0),
                                   pygame.transform.rotate(self.assets['jugador'][0],180),]
        

        
        #variables del joc
        self.lletraTxt = pygame.font.SysFont('Arial',13)
        self.puntuacio = 0
        self.botons = []
        self.archiu = open('data/archius/Menu.txt', 'r')
        self.compMenu = self.archiu.read()
        self.archiu.close()
        self.antirepetir= False
    
    def menu(self):
        for i in self.botons[0:2]:
            i.proces()
        
        self.assets['fons'].set_alpha(100)
        self.finestra.blit(pygame.transform.scale(self.pantalla, self.finestra.get_size()), (0,0))
        self.pantalla.blit(self.assets['mapa'],(0,0))
        self.pantalla.blit(self.assets['fons'],(0,0))
        self.finestra.blit(self.assets['titol'],(384/2-140, 30))

    def perdre(self): #fa la animació de perdre

        self.assets['fons'].set_alpha(100)
        self.finestra.blit(pygame.transform.scale(self.pantalla, self.finestra.get_size()), (0,0))
        self.pantalla.blit(self.assets['mapa'],(0,0))
        self.pantalla.blit(self.assets['fons'],(0,0))
        self.assets['perdut'].set_colorkey(self.assets['perdut'].get_at((0,0)))
        self.finestra.blit(self.assets['perdut'],(384/2-140, 30))

        pasar = False
        archiu = open('data/archius/PuntMax.txt', 'r') #Llegim la puntuació maxima i l'asignem a una variable.
        puntMax = int(archiu.read()) #transformem el contingut del archiu en un int
        archiu.close() 
        if puntMax <= self.puntuacio: #comprobem si la puntuació obtinguda és menor a la puntuació maxima
            archiu = open('data/archius/PuntMax.txt', 'w')
            archiu.write(str(self.puntuacio))
            archiu.close()
            Felicitats= True
        else:
            Felicitats = False
            
        txtFelicitats = self.lletraTxt.render(f'Nova Puntuació Maxima!', True,(255, 255, 255))
        txtPuntuacioMax = self.lletraTxt.render(f'Puntuació Maxima: {puntMax}', True,(255, 255, 255))
        self.pantalla.blit(txtPuntuacioMax, (26, 106))
        self.pantalla.blit(self.txtPuntuacio, (26, 124))
        if Felicitats:
            self.pantalla.blit(txtFelicitats, (26, 142))

        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            pasar = True

        if pasar:
            self.pos = [4, 5]
            self.direccio = 'dreta'
            self.tamany_serp = self.tamany_serp_inicial
            self.posicions_serp = [tuple(self.pos), (3, 5), (2, 5)]
            self.direccions_posicions_serp = [self.direccio] * self.tamany_serp #la direcció per defecte dos cops.
            self.viu = True
            self.puntuacio = 0
            archiu = open('data/archius/menu.txt', 'w')
            archiu.write('True')
            archiu.close()


    def botoJugar():
        archiu = open('data/archius/menu.txt', 'w')
        archiu.write('False')
        archiu.close()
    
    def botoSortir():
        archiu = open('data/archius/menu.txt', 'w')
        archiu.write('True')
        archiu.close()
        pygame.quit()
        sys.exit()

    def run(self):
        #creem tots els botons que utilitzarem:
        self.botons.append(boto(self, (26, 104), 140, 32, 'Jugar', Game.botoJugar))
        self.botons.append(boto(self, (26, 138), 140, 32, 'Sortir', Game.botoSortir))

        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    archiu = open('data/archius/menu.txt', 'w')
                    archiu.write('True')
                    archiu.close()
                    pygame.quit()
                    sys.exit()                    
                if event.type == pygame.KEYDOWN: #només es canvien les direccions
                    #recordar que si queremos, podemos simplificar el código quitando la parte de en medio
                    if event.key == pygame.K_d and not self.direccio == 'esquerra' and 'esquerra' not in self.registro_mov:
                        self.direccio = 'dreta'                              
                    elif event.key == pygame.K_s and not self.direccio == 'adalt' and 'adalt' not in self.registro_mov:                    
                        self.direccio = 'abaix'                    
                    elif event.key == pygame.K_w and not self.direccio == 'abaix' and 'abaix' not in self.registro_mov:                    
                        self.direccio = 'adalt'
                    elif event.key == pygame.K_a and not self.direccio == 'dreta' and 'dreta' not in self.registro_mov:                    
                        self.direccio = 'esquerra'
                    self.registro_mov.append(self.direccio)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass


            self.archiu = open('data/archius/Menu.txt', 'r')
            self.compMenu = self.archiu.read()
            self.archiu.close()

            if self.compMenu == 'True':
                Game.menu(self)
            elif self.viu == False:
                Game.perdre(self)
            else:
                #L'encarregat de ferte perdre
                if self.pos[0] < 1:
                    self.viu = False
                    self.pos[0] = 2
                elif self.pos[0] > 10:
                    self.viu = False
                    self.pos[0] = 9
                elif self.pos[1] < 4:
                    self.viu = False
                    self.pos[1] = 3
                elif self.pos[1] > 13:
                    self.viu = False
                    self.pos[1] = 12
                elif tuple(self.pos) in self.posicions_serp[1:]:#elimino el primer element, ja que es el cap
                    self.viu = False
                else:
                    self.viu = True
                temps_actual = time.time()

                if  temps_actual > self.control_temps + self.temps_serp: 
                    if self.direccio == 'dreta':
                        self.pos[0] += 1
                    elif self.direccio == 'abaix':
                        self.pos[1] += 1
                    elif self.direccio == 'adalt':
                        self.pos[1] -= 1
                    elif self.direccio == 'esquerra':
                        self.pos[0] -= 1
                    self.registro_mov = [self.direccio]
                    self.control_temps = temps_actual
                    self.posicions_serp  = [tuple(self.pos)] + self.posicions_serp 
                    ultima_posicio = self.posicions_serp.pop()
                    ###canvis, haig de fer el mateix amb la llista de les direccions
                    self.direccions_posicions_serp = [self.direccio] + self.direccions_posicions_serp #recordo que no sé com es possa una cossa a davant
                    ultima_direccio = self.direccions_posicions_serp.pop()
                    
                    
                    ### Comporbar si la serp s'ha menjat la poma
                    if self.posicio_poma == tuple(self.pos):
                        self.posicio_poma = generar_poma()
                        while self.posicio_poma in self.posicions_serp:
                            self.posicio_poma =  generar_poma()
                        self.tamany_serp += 1
                        self.puntuacio += 1
                        self.posicions_serp.append(ultima_posicio)
                        ###canvis, al final, com la cua es manté, llavors, hem de recuperar la direcció associada,
                        self.direccions_posicions_serp.append(ultima_direccio)
                    
                    
                    #renderizar la cabeza
                    if self.direccio == 'esquerra':
                        surface_serp = self.llista_imatges_gir[12]
                    elif self.direccio == 'dreta':
                        surface_serp = self.llista_imatges_gir[13]
                    elif self.direccio == 'adalt':
                        surface_serp = self.llista_imatges_gir[14]
                    elif self.direccio == 'abaix':
                        surface_serp = self.llista_imatges_gir[15]
                    self.pantalla.blit(surface_serp, (self.pos[0]*16,(self.pos[1])*16))
                    #aqui he puesto 1 para que no renderitzi el cap dues vegades
                    for i in range(self.tamany_serp-1): #ITEro de la manera i vs i+1, i vaigincrementant aixina, comparo la 0 i la 1, la 1 i 2, etc
                        #defineixo les normes: hi ha 8 casos, a lo millor hi ha un millor algoritme, que sigui capaz d'iterar totes les posibles direccions, amb un for, pero no el conec.
                        #així ja està bé.
                        if  self.posicions_serp[i] != self.posicions_serp[self.tamany_serp-1]:
                            if self.direccions_posicions_serp[i] == 'esquerra' and self.direccions_posicions_serp[i+1] == 'adalt':
                                surface_serp = self.llista_imatges_gir[0]
                            elif self.direccions_posicions_serp[i] == 'esquerra' and self.direccions_posicions_serp[i+1] == 'abaix':
                                surface_serp = self.llista_imatges_gir[1]
                            elif self.direccions_posicions_serp[i] == 'dreta' and self.direccions_posicions_serp[i+1] == 'adalt':
                                surface_serp = self.llista_imatges_gir[2]
                            elif self.direccions_posicions_serp[i] == 'dreta' and self.direccions_posicions_serp[i+1] == 'abaix':
                                surface_serp = self.llista_imatges_gir[3]
                            elif self.direccions_posicions_serp[i] == 'adalt' and self.direccions_posicions_serp[i+1] == 'esquerra':
                                surface_serp = self.llista_imatges_gir[4]
                            elif self.direccions_posicions_serp[i] == 'adalt' and self.direccions_posicions_serp[i+1] == 'dreta':
                                surface_serp = self.llista_imatges_gir[5]
                            elif self.direccions_posicions_serp[i] == 'abaix' and self.direccions_posicions_serp[i+1] == 'esquerra':
                                surface_serp = self.llista_imatges_gir[6]
                            elif self.direccions_posicions_serp[i] == 'abaix' and self.direccions_posicions_serp[i+1] == 'dreta':
                                surface_serp = self.llista_imatges_gir[7]
                            else:
                                ###això vol dir que direccions_posicions_serp[i] ==  direccions_posicions_serp[i+1], llavors un quadrat normal
                                if self.direccions_posicions_serp[i] == 'esquerra':
                                    surface_serp = self.llista_imatges_gir[8]
                                elif self.direccions_posicions_serp[i] == 'dreta':
                                    surface_serp = self.llista_imatges_gir[9]
                                elif self.direccions_posicions_serp[i] == 'adalt':
                                    surface_serp = self.llista_imatges_gir[10]
                                elif self.direccions_posicions_serp[i] == 'abaix':
                                    surface_serp = self.llista_imatges_gir[11]
                        if self.posicions_serp[i+1] == self.posicions_serp[self.tamany_serp-1]: #aquí el único cambio ha sido pasar de i a i+1
                            if self.direccions_posicions_serp[i] == 'esquerra':
                                surface_serp = self.llista_imatges_gir[16]
                            elif self.direccions_posicions_serp[i] == 'dreta':
                                surface_serp = self.llista_imatges_gir[17]
                            elif self.direccions_posicions_serp[i] == 'adalt':
                                surface_serp = self.llista_imatges_gir[18]
                            elif self.direccions_posicions_serp[i] == 'abaix':
                                surface_serp = self.llista_imatges_gir[19]
                        self.pantalla.blit(surface_serp, (self.posicions_serp[i+1][0] * 16, self.posicions_serp[i+1][1] * 16))
                    self.finestra.blit(pygame.transform.scale(self.pantalla, self.finestra.get_size()), (0,0))
                    self.pantalla.blit(self.assets['mapa'],(0,0))
                    self.pantalla.blit(self.assets['poma'], (self.posicio_poma[0]*16,self.posicio_poma[1]*16))
                    self.txtPuntuacio = self.lletraTxt.render(f'Puntuació: {self.puntuacio}', True,(255, 255, 255))
                    self.pantalla.blit(self.txtPuntuacio, (16, 16))

            pygame.display.update()
            self.clock.tick(60)



Game().run()
