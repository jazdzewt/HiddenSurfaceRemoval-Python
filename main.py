import pygame
import numpy as np
import sys

from camera import Camera
from wczytywanie import wczytaj_obiekty

szerokosc = 1200 
wysokosc = 700


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


        sciany_renderowanie = []

        for obiekt in scena.obiekty:
            przetransformowane_wezly = []
            
            for w in obiekt.wezly:

                wezel = macierz_widoku @ w
                przetransformowane_wezly.append(wezel)

            for sciana in obiekt.krawedzie:

                rysowac = True

                wezly_na_ekranie = []
                glebokosci_wezlow = []
                
                for id_wezla in sciana:
                    wezel_3d = przetransformowane_wezly[id_wezla - 1]
                    rzutowany_wezel = camera.rzutowanie(wezel_3d, szerokosc, wysokosc)
                    
                    if rzutowany_wezel:
                        wezly_na_ekranie.append(rzutowany_wezel)
                        glebokosci_wezlow.append(np.linalg.norm(wezel_3d[:3]))
                    else:
                        rysowac = False
                        break
                        
                if rysowac:

                    kolor = obiekt.color

                    #print("glebokosci_wezlow: ", glebokosci_wezlow)
                    glebokosc_sciany = sum(glebokosci_wezlow) / len(glebokosci_wezlow)

                    sciany_renderowanie.append((glebokosc_sciany, wezly_na_ekranie, kolor))

        # sortowanie
        sciany_renderowanie.sort(key=lambda s: s[0], reverse=True)

        for glebokosc_sciany, wezly_na_ekranie, kolor in sciany_renderowanie:
            pygame.draw.polygon(screen, kolor, wezly_na_ekranie)
            pygame.draw.polygon(screen, (0, 0, 0), wezly_na_ekranie, 2)

        pygame.display.flip()

        clock.tick(60) #fps  

if __name__ == "__main__":
    main() 