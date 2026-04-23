import pygame
import numpy as np
import sys
from functools import cmp_to_key

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

    def porownaj_sciany(s1, s2):
        """
        Pełny, stabilny test algorytmu malarskiego (sortowanie topologiczne).
        Zwraca -1 gdy s1 powinno być narysowane PRZED s2 (s1 jest dalej).
        """
        n1, d1, wezly3d_1, wezly2d_1, _, cZ1 = s1
        n2, d2, wezly3d_2, wezly2d_2, _, cZ2 = s2
        eps = 1e-5

        # 1. Test Min-Max Z (Z jest głębokością w głąb ekranu)
        Z_min1, Z_max1 = min(v[2] for v in wezly3d_1), max(v[2] for v in wezly3d_1)
        Z_min2, Z_max2 = min(v[2] for v in wezly3d_2), max(v[2] for v in wezly3d_2)

        if Z_min1 > Z_max2 + eps: return -1 # s1 całkowicie za s2
        if Z_min2 > Z_max1 + eps: return 1  # s2 całkowicie za s1

        # 2. Test nakładania się na ekranie (Bounding Box 2D)
        X_min1, X_max1 = min(v[0] for v in wezly2d_1), max(v[0] for v in wezly2d_1)
        Y_min1, Y_max1 = min(v[1] for v in wezly2d_1), max(v[1] for v in wezly2d_1)
        X_min2, X_max2 = min(v[0] for v in wezly2d_2), max(v[0] for v in wezly2d_2)
        Y_min2, Y_max2 = min(v[1] for v in wezly2d_2), max(v[1] for v in wezly2d_2)

        overlap_X = not (X_max1 < X_min2 or X_max2 < X_min1)
        overlap_Y = not (Y_max1 < Y_min2 or Y_max2 < Y_min1)

        if not (overlap_X and overlap_Y):
            # Brak nakładania na ekranie -> kolejność nie ma znaczenia wizualnego
            return -1 if cZ1 > cZ2 else (1 if cZ1 < cZ2 else 0)

        # 3. Testy płaszczyznowe
        strona_kamery_s2 = -d2
        znaki_s1_wzgl_s2 = [np.dot(n2, v) - d2 for v in wezly3d_1]
        
        # S1 jest ZA S2, jeśli żaden wierzchołek S1 nie jest stricte PRZED S2
        s1_za_s2 = all(z * strona_kamery_s2 < eps for z in znaki_s1_wzgl_s2)
        # S1 jest PRZED S2, jeśli żaden wierzchołek S1 nie jest stricte ZA S2
        s1_przed_s2 = all(z * strona_kamery_s2 > -eps for z in znaki_s1_wzgl_s2)

        strona_kamery_s1 = -d1
        znaki_s2_wzgl_s1 = [np.dot(n1, v) - d1 for v in wezly3d_2]
        
        s2_za_s1 = all(z * strona_kamery_s1 < eps for z in znaki_s2_wzgl_s1)
        s2_przed_s1 = all(z * strona_kamery_s1 > -eps for z in znaki_s2_wzgl_s1)

        # Gwarancja asymetrii w Pythonowym sort():
        if s1_za_s2 and not s2_za_s1: return -1
        if s2_za_s1 and not s1_za_s2: return 1

        if s2_przed_s1 and not s1_przed_s2: return -1
        if s1_przed_s2 and not s2_przed_s1: return 1

        # 4. Fallback (np. przecinające się ściany, współpłaszczyznowe)
        if cZ1 > cZ2: return -1
        elif cZ1 < cZ2: return 1
        return 0

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

                # --- Wyznaczanie płaszczyzny ściany ---
                A = np.array(przetransformowane_wezly[sciana[0] - 1][:3])
                B = np.array(przetransformowane_wezly[sciana[1] - 1][:3])
                C = np.array(przetransformowane_wezly[sciana[2] - 1][:3])

                # Iloczyn wektorowy → normalna płaszczyzny
                AB = B - A
                AC = C - A
                normalna = np.cross(AB, AC)

                dlugosc_normalnej = np.linalg.norm(normalna)
                if dlugosc_normalnej < 1e-10:
                    continue  # zdegenerowana ściana

                normalna_znorm = normalna / dlugosc_normalnej

                # Równanie płaszczyzny: n · P = d
                d = np.dot(normalna_znorm, A)

                # --- Rzutowanie + zbieranie wierzchołków 3D ---
                rysowac = True
                wezly_na_ekranie = []
                wezly_3d = []
                suma_z = 0.0

                for id_wezla in sciana:
                    wezel_3d_raw = przetransformowane_wezly[id_wezla - 1]
                    rzutowany_wezel = camera.rzutowanie(wezel_3d_raw, szerokosc, wysokosc)

                    if rzutowany_wezel:
                        wezly_na_ekranie.append(rzutowany_wezel)
                        wezly_3d.append(np.array(wezel_3d_raw[:3]))
                        suma_z += wezel_3d_raw[2]
                    else:
                        rysowac = False
                        break

                if rysowac:
                    kolor = obiekt.color
                    centroid_z = suma_z / len(sciana)
                    # Przechowuj: normalna, d, wierzchołki 3D, wierzchołki 2D, kolor, centroid_z
                    sciany_renderowanie.append((normalna_znorm, d, wezly_3d, wezly_na_ekranie, kolor, centroid_z))

        # --- Algorytm malarski: sortowanie testem płaszczyznowym ---
        # porownaj_sciany sprawdza czy wierzchołki s1 leżą za płaszczyzną s2
        sciany_renderowanie.sort(key=cmp_to_key(porownaj_sciany))

        for _, _, _, wezly_na_ekranie, kolor, _ in sciany_renderowanie:
            pygame.draw.polygon(screen, kolor, wezly_na_ekranie)
            pygame.draw.polygon(screen, (0, 0, 0), wezly_na_ekranie, 2)

        pygame.display.flip()

        clock.tick(60) #fps  

if __name__ == "__main__":
    main() 