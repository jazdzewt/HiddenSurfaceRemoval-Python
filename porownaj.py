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
'''
def czy_z_przodu(wielokat, normalna, odleglosc):
    for wierzcholek in wielokat:
        punkt = wierzcholek[:3]
        wynik = odleglosc + np.dot(normalna, punkt)
        if wynik <= -e:
            return False
    return True
'''

def sprawdz_odleglosc(sciana):

    wierzcholki = sciana[0]

    suma = 0 

    for w in wierzcholki:

        suma += w[2]
    
    odleglosc = suma / len(wierzcholki)

    return odleglosc


def sortuj_sciany(sciany):

    # Wstepne sortowanie: od najdalszych (duze srednie Z) do najblizszych
    sciany = sorted(sciany, key=sprawdz_odleglosc, reverse=True)

    
    for i in range(len(sciany)):
        for j in range(i + 1, len(sciany)):
            sciana1 = sciany[i][0]
            sciana2 = sciany[j][0]

            #normalna1, odleglosc1 = wektor_normalny(sciana1)
            normalna2, odleglosc2 = wektor_normalny(sciana2)

            if czy_z_tylu(sciana1, normalna2, odleglosc2):
                temp = sciany[i] 
                sciany[i] = sciany[j]
                sciany[j] = temp 
            '''
            elif czy_z_przodu(sciana2, normalna1, odleglosc1):
                temp = sciany[i] 
                sciany[i] = sciany[j]
                sciany[j] = temp 
            '''
    
    sciany.reverse()

    return sciany
