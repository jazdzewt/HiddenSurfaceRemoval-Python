import pygame
import numpy as np
import sys
import os 

szerokosc = 1200 
wysokosc = 700

class Obiekt:
    def __init__(self):
        self.color = []
        self.wezly = []
        self.krawedzie = []

    def dodaj_wezel(self, wezel):
        self.wezly.append(wezel)

    def dodaj_krawedz(self, krawedz):
        self.krawedzie.append(krawedz)

class Scena: 
    def __init__(self):
        self.obiekty = []
    
    def dodaj_obiekt(self, obiekt):
        self.obiekty.append(obiekt)

class Camera:
    def __init__(self):

        self.pozycja = np.array([0.0, 0.0, 0.0, 1.0])

        # góra / dół
        self.pochylenie = 0 

        # lewo / prawo
        self.obrot = 0 


        # przechylenie na boki 
        self.przechylenie = 0   

        self.f = 600

    def macierz_widoku(self):

        # macierz translacji 
        t_mat = np.array([
            [1, 0, 0, -self.pozycja[0]],
            [0, 1, 0, -self.pozycja[1]],
            [0, 0, 1, -self.pozycja[2]],
            [0, 0, 0, 1]])

        # macierze rotacji  
        r_pochylenie = np.array([
            [1, 0, 0, 0],
            [0, np.cos(self.pochylenie), -np.sin(self.pochylenie), 0],
            [0, np.sin(self.pochylenie), np.cos(self.pochylenie), 0],  
            [0, 0, 0, 1]])

        r_przechylenie = np.array([
            [np.cos(self.przechylenie), -np.sin(self.przechylenie), 0, 0],
            [np.sin(self.przechylenie), np.cos(self.przechylenie), 0, 0], 
            [0, 0, 1, 0],
            [0, 0, 0, 1]])

        r_obrot = np.array([
            [np.cos(self.obrot), 0, np.sin(self.obrot), 0],
            [0, 1, 0, 0],
            [-np.sin(self.obrot), 0, np.cos(self.obrot), 0],
            [0, 0, 0, 1]])
        # macierz widoku
        macierz_w = r_przechylenie @ r_pochylenie @ r_obrot @ t_mat

        return macierz_w

    def rzutowanie(self, punkt):

        x = punkt[0]
        y = punkt[1]
        z = punkt[2]
        
        if z <= 0.1:
            return None 
        
        x_2d = (x * self.f) / z + szerokosc / 2
        y_2d = (-y * self.f) / z + wysokosc / 2
        
        return int(x_2d), int(y_2d)

def wczytaj_obiekty(folder_path):

    scena = Scena()

    try:
        for file in os.listdir(folder_path):

            filepath = os.path.join(folder_path, file)
            if not filepath.endswith(".txt"):
                continue

            with open(filepath, 'r') as f:
                obiekt = Obiekt()

                for line in f:
                    parts = line.split()
                
                    if not parts:
                        continue

                    if parts[0] == 'w':
                        obiekt.dodaj_wezel([float(parts[1]), float(parts[2]), float(parts[3]), 1.0])

                    elif parts[0] == 'k':
                        krawedz = []
                        for i in range(1, len(parts)):
                            krawedz.append(int(parts[i]))
                        obiekt.dodaj_krawedz(krawedz)

                    elif parts[0] == 'c':
                        obiekt.color = (int(parts[1]), int(parts[2]), int(parts[3]))

                if obiekt.wezly:
                    obiekt.wezly = np.array(obiekt.wezly)
                    scena.dodaj_obiekt(obiekt)
        return scena

    except FileNotFoundError:
        print("Brak folderu!")
        return Scena()

def main():

    pygame.init()

    screen = pygame.display.set_mode((szerokosc, wysokosc))
    clock = pygame.time.Clock()
    camera = Camera()
    
    
    #wezly, krawedzie = wczytaj_obiekt('data/scena.txt')
    scena = wczytaj_obiekty('./data')

    while True:

        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        x = 0.0  
        y = 0.0 
        z = 0.0 

        krok1 = 0.1

        if keys[pygame.K_w]: 
            z = z + krok1  # przód
        if keys[pygame.K_s]: 
            z = z - krok1  # tył
        if keys[pygame.K_a]: 
            x = x - krok1  # lewo
        if keys[pygame.K_d]: 
            x = x + krok1 # prawo
        if keys[pygame.K_SPACE]: 
            y = y + krok1 # góra
        if keys[pygame.K_LCTRL]: 
            y = y - krok1 # dół

        if x != 0 or y != 0 or z != 0:
            
            macierz_w = camera.macierz_widoku()
            
            macierz_w_T = macierz_w.T
            lokalny_kierunek = np.array([x, y, z, 0.0])

            globalny_kierunek = macierz_w_T @ lokalny_kierunek

            camera.pozycja[0] = camera.pozycja[0] + globalny_kierunek[0]
            camera.pozycja[1] = camera.pozycja[1] + globalny_kierunek[1]
            camera.pozycja[2] = camera.pozycja[2] + globalny_kierunek[2]

        krok2 = 0.01

        if keys[pygame.K_LEFT]: 
            camera.obrot = camera.obrot + krok2
        if keys[pygame.K_RIGHT]: 
            camera.obrot = camera.obrot - krok2

        if keys[pygame.K_q]: 
            camera.przechylenie = camera.przechylenie - krok2
        if keys[pygame.K_e]: 
            camera.przechylenie = camera.przechylenie + krok2

        if keys[pygame.K_UP]: 
            camera.pochylenie = camera.pochylenie + krok2
        if keys[pygame.K_DOWN]: 
            camera.pochylenie = camera.pochylenie - krok2
        
        # ZOOM
        zoom = 5
        
        if keys[pygame.K_EQUALS]: 
            camera.f = camera.f + zoom
        if keys[pygame.K_MINUS]:  
            camera.f = camera.f - zoom  

        # renderowanie 
        macierz_widoku = camera.macierz_widoku() 


        for obiekt in scena.obiekty:
            przetransformowane_wezly = []
            for w in obiekt.wezly:
                przetransformowane_wezly.append(macierz_widoku @ w)

            for sciana in obiekt.krawedzie:
                '''
                for i in range(len(sciana) - 1):
                    id_poczatkowy = sciana[i] - 1
                    id_koncowy = sciana[i + 1] - 1  
                    
                    wezel_poczatkowy = przetransformowane_wezly[id_poczatkowy]
                    wezel_koncowy = przetransformowane_wezly[id_koncowy]

                    punkt_pocz = camera.rzutowanie(wezel_poczatkowy)
                    punkt_kon = camera.rzutowanie(wezel_koncowy)

                    if punkt_pocz and punkt_kon:
                        pygame.draw.line(screen, (0, 0, 0), punkt_pocz, punkt_kon, 2)
                '''
                punkty_na_ekranie = []
                czy_rysowac = True
                
                for id_wezla in sciana:
                    wezel = przetransformowane_wezly[id_wezla - 1]
                    rzut = camera.rzutowanie(wezel)
                    if rzut:
                        punkty_na_ekranie.append(rzut)
                    else:
                        czy_rysowac = False
                        break
                        
                if czy_rysowac and len(punkty_na_ekranie) >= 3:
                    kolor = obiekt.color if obiekt.color else (200, 200, 200)
                    pygame.draw.polygon(screen, kolor, punkty_na_ekranie)
                    pygame.draw.polygon(screen, (0, 0, 0), punkty_na_ekranie, 2)
                    
        pygame.display.flip()

        clock.tick(60) #fps  

if __name__ == "__main__":
    main() 