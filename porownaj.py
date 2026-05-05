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

def czy_z_tylu(wielokat, normalna, d):
        
    for wierzcholek in wielokat:

        punkt = wierzcholek[:3]
        wynik = d + np.dot(normalna, punkt) 
        
        if wynik >= e:
            return False
    return True

def czy_przod(wielokat, normalna, d):
        
    for wierzcholek in wielokat:
        punkt = wierzcholek[:3]
        wynik = d + np.dot(normalna, punkt)
        
        if wynik <= -e:
            return False
            
    return True


def czy_otoczenia_wykluczaja(sciana1, sciana2):

    x1 = []
    y1 = []
    z1 = []

    for wierzcholek in sciana1:
        x1.append(wierzcholek[0])
        y1.append(wierzcholek[1])
        z1.append(abs(wierzcholek[2]))
        
    x2 = []
    y2 = []
    z2 = []

    for wierzcholek in sciana2:
        x2.append(wierzcholek[0])
        y2.append(wierzcholek[1])
        z2.append(abs(wierzcholek[2]))

    # tu jak na and się zmieni to działa
    if max(x1) < min(x2) or max(x2) < min(x1): 
        return True
    if max(y1) < min(y2) or max(y2) < min(y1):
        return True

    if min(z1) > max(z2):
        return True

    return False

def sciany_nakladaja_sie_na_ekranie(sciana1, sciana2):

    x1 = []
    y1 = []

    for wierzcholek in sciana1:

        z = abs(wierzcholek[2]) + e
        x1.append(wierzcholek[0] / z)
        y1.append(wierzcholek[1] / z)
        
    min_x1 = min(x1)
    max_x1 = max(x1)
    min_y1 = min(y1)
    max_y1 = max(y1)

    x2 = []
    y2 = []
    for wierzcholek in sciana2:

        z = abs(wierzcholek[2]) + e
        x2.append(wierzcholek[0] / z)
        y2.append(wierzcholek[1] / z)
        
    min_x2 = min(x2)
    max_x2 = max(x2)
    min_y2 = min(y2)
    max_y2 = max(y2)
    
    if max_x1 < min_x2 or max_x2 < min_x1 or max_y1 < min_y2 or max_y2 < min_y1:
        return False
    else:
        return True

def sortuj_sciany(sciany):
    
    i = 0
    while i < len(sciany):
        sciana1 = sciany[i][0]
        
        normalna1, odleglosc1 = wektor_normalny(sciana1)
        zmiana = False
        
        j = i + 1
        while j < len(sciany):
            sciana2 = sciany[j][0]

            
            if czy_otoczenia_wykluczaja(sciana1, sciana2):
                j += 1
                continue
            
                      
            if sciany_nakladaja_sie_na_ekranie(sciana1, sciana2) == False:

                j = j + 1

                continue
            
            normalna2, odleglosc2 = wektor_normalny(sciana2)
            
            if czy_z_tylu(sciana1, normalna2, odleglosc2) or czy_przod(sciana2, normalna1, odleglosc1):

                j = j + 1

                continue
            
            if czy_z_tylu(sciana2, normalna1, odleglosc1) or czy_przod(sciana1, normalna2, odleglosc2):

                wyciagniete = sciany.pop(j)
                sciany.insert(i, wyciagniete)
                    
                zmiana = True
                break
                    
            j = j + 1
            
        if zmiana == False:
            i = i + 1
            
    return sciany