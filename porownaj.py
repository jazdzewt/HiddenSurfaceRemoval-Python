import numpy as np

e = 0.0001

def wektor_normalny(wielokat):

    pierwszy_punkt = wielokat[0][:3] 
    
    for i in range(1, len(wielokat) - 1):
        drugi_punkt = wielokat[i][:3]
        trzeci_punkt = wielokat[i+1][:3]
        
        wektor1 = drugi_punkt - pierwszy_punkt
        wektor2 = trzeci_punkt - pierwszy_punkt
        
        normalna = np.cross(wektor1, wektor2)
        dlugosc = np.linalg.norm(normalna)
        
        if dlugosc > e:
            normalna = normalna / dlugosc

            if np.dot(normalna, pierwszy_punkt) > 0: 
                normalna = -normalna 
                
            odleglosc_kamera = -np.dot(normalna, pierwszy_punkt)

            return normalna, odleglosc_kamera
            
    return None, 0

def czy_z_tylu(wielokat, normalna, odleglosc):
        
    for wierzcholek in wielokat:

        punkt = wierzcholek[:3]
        wynik = odleglosc + np.dot(normalna, punkt) 
        
        if wynik >= e:
            return False
    return True

def czy_z_przodu(wielokat, normalna, odleglosc):
    for wierzcholek in wielokat:
        punkt = wierzcholek[:3]
        wynik = odleglosc + np.dot(normalna, punkt)
        if wynik <= -e:
            return False
    return True


def sprawdz_odleglosc(sciana):

    wierzcholki = sciana[0]

    max_Z = 0 

    # Centroid Z (srednia) - stabilniejszy niz max_Z
    for w in wierzcholki:
        if w[2] > max_Z:
            max_Z = w[2]

    return max_Z

def sciany_nakladaja_sie_na_ekranie(sciana1, sciana2):
    # Najpierw znajdujemy skrajne punkty pierwszej ściany na płaskim ekranie
    x1 = []
    y1 = []

    for wierzcholek in sciana1:

        z = abs(wierzcholek[2]) + e
        x1.append(wierzcholek[0] / z)
        y1.append(wierzcholek[1] / z)
        
    min_x1, max_x1 = min(x1), max(x1)
    min_y1, max_y1 = min(y1), max(y1)

    # To samo robimy dla drugiej ściany
    x2 = []
    y2 = []
    for wierzcholek in sciana2:

        z = abs(wierzcholek[2]) + e
        x2.append(wierzcholek[0] / z)
        y2.append(wierzcholek[1] / z)
        
    min_x2, max_x2 = min(x2), max(x2)
    min_y2, max_y2 = min(y2), max(y2)
    
    # Sprawdzamy czy narysowane prostokąty się mijają (nie dotykają się)
    if max_x1 < min_x2 or max_x2 < min_x1 or max_y1 < min_y2 or max_y2 < min_y1:
        return False # Mijają się, więc nie musimy ich sortować względem siebie
    else:
        return True # Nakładają się na ekranie


def sortuj_sciany(sciany):

    sciany = sorted(sciany, key=sprawdz_odleglosc, reverse=True)

    
    for i in range(len(sciany)):
        for j in range(i + 1, len(sciany)):
            sciana1 = sciany[i][0]
            sciana2 = sciany[j][0]

            normalna1, odleglosc1 = wektor_normalny(sciana1)
            normalna2, odleglosc2 = wektor_normalny(sciana2)

            #if sciany_nakladaja_sie_na_ekranie(sciana1, sciana2):

                # Zamień tylko gdy OBE płaszczyzny jednoznacznie potwierdzają kolejność
                # (and = konserwatywne, or byłoby zbyt agresywne i powodowało błędne zamiany)
            if czy_z_tylu(sciana2, normalna1, odleglosc1) and czy_z_przodu(sciana1, normalna2, odleglosc2):
                temp = sciany[i] 
                sciany[i] = sciany[j]
                sciany[j] = temp                
                '''
                elif czy_z_przodu(sciana1, normalna2, odleglosc2):
                    temp = sciany[i] 
                    sciany[i] = sciany[j]
                    sciany[j] = temp
                '''
    #sciany.reverse()

    return sciany
