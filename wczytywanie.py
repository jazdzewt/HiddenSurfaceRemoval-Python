import numpy as np
import os

from dzielenie import dodaj_wezly_do_scian
from obiekt import Obiekt, Scena


def wczytaj_obiekty(folder_path):

    scena = Scena()

    try:
        for file in os.listdir(folder_path):

            filepath = os.path.join(folder_path, file)
            if not filepath.endswith(".txt"):
                continue

            with open(filepath, 'r') as f:
                obiekt = Obiekt(file)

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

                    # Nowe =======================================

                    dodaj_wezly_do_scian(obiekt, poziom_subdivizji=2)

                    print(obiekt.name)
                    print()
                    print("wezly: ", obiekt.wezly)
                    print()
                    print("krawedzie: ", obiekt.krawedzie)

                    # Koniec =======================================

                    scena.dodaj_obiekt(obiekt)
        return scena

    except FileNotFoundError:
        print("Brak folderu!")
        return Scena()