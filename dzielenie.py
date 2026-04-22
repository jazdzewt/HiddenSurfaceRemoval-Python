import numpy as np

def dodaj_wezly_do_scian(obiekt, poziom_subdivizji=1):
    """
    Zagęszcza siatkę dodając nowe węzły na środkach krawędzi, 
    bez tworzenia nowych ścian.
    """
    if poziom_subdivizji <= 0:
        return
        
    wezly = [list(w) for w in obiekt.wezly]
    nowe_sciany = []

    for sciana in obiekt.krawedzie:
        zamknieta = len(sciana) > 1 and sciana[0] == sciana[-1]
        unikalne = sciana[:-1] if zamknieta else sciana
        aktualna_sciana = [i - 1 for i in unikalne] # przejście na indeksy 0-based
        
        for _ in range(poziom_subdivizji):
            nowa_sciana = []
            liczba_w = len(aktualna_sciana)
            for i in range(liczba_w):
                idx_a = aktualna_sciana[i]
                idx_b = aktualna_sciana[(i + 1) % liczba_w] 
                
                # 1. Dodaj obecny węzeł
                nowa_sciana.append(idx_a)
                
                # 2. Oblicz środek krawędzi i dodaj do wezly
                p_a = np.array(wezly[idx_a])
                p_b = np.array(wezly[idx_b])
                srodek = (p_a + p_b) / 2.0
                
                wezly.append([srodek[0], srodek[1], srodek[2], 1.0])
                idx_srodka = len(wezly) - 1
                
                # 3. Dodaj srodek do nowej sciany
                nowa_sciana.append(idx_srodka)
                
            aktualna_sciana = nowa_sciana
            
        nowa_sciana_1based = [i + 1 for i in aktualna_sciana]
        if zamknieta:
             nowa_sciana_1based.append(nowa_sciana_1based[0])
             
        nowe_sciany.append(nowa_sciana_1based)

    obiekt.wezly = np.array(wezly)
    obiekt.krawedzie = nowe_sciany
