from decimal import MAX_EMAX
import numpy as np

e = 0.0001

def wektor_normalny(wielokat):

    pierwszy_punkt = wielokat[0][:3] 
    
    for i in range(1, len(wielokat) - 1):
        drugi_punkt = wielokat[i][:3]
        trzeci_punkt = wielokat[i+1][:3]
        
        wektor1 = drugi_punkt - pierwszy_punkt
        wektor2 = trzeci_punkt - pierwszy_punkt
        
        # iloczyn wektorowy 
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

def czy_przod(wielokat, normalna, odleglosc):
        
    for wierzcholek in wielokat:
        punkt = wierzcholek[:3]
        wynik = odleglosc + np.dot(normalna, punkt)
        
        if wynik <= -e:
            return False
            
    return True

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
    
    # Słownik, który pilnuje, żebyśmy nie przekładali tych samych ścian w nieskończoność
    ile_razy_cofnieto = {}
    
    for sciana in sciany:
        id_sciany = id(sciana[0])
        ile_razy_cofnieto[id_sciany] = 0
    
    limit_cofniec = len(sciany)

    # Rozpoczynamy dokładne sprawdzanie i poprawianie kolejności
    i = 0
    while i < len(sciany):
        sciana_P = sciany[i]
        wielokat_P = sciana_P[0]
        
        normalna_P, odleglosc_P = wektor_normalny(wielokat_P)
        zmiana = False
        
        j = i + 1
        while j < len(sciany):
            sciana_Q = sciany[j]
            wielokat_Q = sciana_Q[0]
            
            # TEST 1: Czy ściany w ogóle wchodzą na siebie na ekranie?
            
            if sciany_nakladaja_sie_na_ekranie(wielokat_P, wielokat_Q) == False:
                j += 1
                continue # Nie nakładają się, idziemy sprawdzić kolejną ścianę
            
            normalna_Q, odleglosc_Q = wektor_normalny(wielokat_Q)
            
            if czy_z_tylu(wielokat_P, normalna_Q, odleglosc_Q) or czy_przod(wielokat_Q, normalna_P, odleglosc_P):
                # Jest dobrze, P powinno zostać narysowane wcześniej niż Q
                j += 1
                continue
            
            if czy_z_tylu(wielokat_Q, normalna_P, odleglosc_P) or czy_przod(wielokat_P, normalna_Q, odleglosc_Q):
                id_Q = id(wielokat_Q)
                
                
                if ile_razy_cofnieto[id_Q] < limit_cofniec:
                    ile_razy_cofnieto[id_Q] += 1
                    
                    wyciagnieta_sciana = sciany.pop(j)
                    sciany.insert(i, wyciagnieta_sciana)
                    
                    zmiana = True
                    break
                    
            j += 1
            
        if zmiana == False:
            i += 1
            
    return sciany