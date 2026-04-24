import numpy as np

def wektor_normalny(poly):
    """Zwraca normalną (n) i stałą (D). Normalna ZAWSZE patrzy w stronę kamery (0,0,0)."""
    pts = [v[:3] for v in poly]
    if len(pts) < 3: return None, 0
    p0 = pts[0]
    
    for i in range(1, len(pts)-1):
        n = np.cross(pts[i]-p0, pts[i+1]-p0)
        dlugosc = np.linalg.norm(n)
        if dlugosc > 1e-6:
            n = n / dlugosc
            # Odwracamy, jeśli wektor ucieka od kamery
            if np.dot(n, p0) > 0: n = -n
            return n, -np.dot(n, p0)
            
    return None, 0

def czy_calkowicie_za(poly, n, D):
    if n is None: return False
    # Płaszczyzna dzieli świat. Wartości ujemne to przestrzeń "za" płaszczyzną od strony oka.
    return all(np.dot(n, v[:3]) + D < 1e-4 for v in poly)

def czy_calkowicie_przed(poly, n, D):
    if n is None: return False
    # Wartości dodatnie to przestrzeń "przed" płaszczyzną, blisko oka.
    return all(np.dot(n, v[:3]) + D > -1e-4 for v in poly)

def sortuj_sciany(sciany):
    if not sciany: return []

    # 1. Zgrubne sortowanie: od najdalszego punktu do najbliższego
    def max_dist(face):
        return max(np.linalg.norm(v[:3]) for v in face[0])
        
    S = sorted(sciany, key=max_dist, reverse=True)
    
    # Słownik cofnięć zapobiegający nieskończonej pętli, gdy np. bryły utworzą pierścień
    cofniecia = {id(f[0]): 0 for f in S}
    limit_cofniec = len(S)

    i = 0
    while i < len(S):
        P = S[i]
        poly_p = P[0]
        nP, DP = wektor_normalny(poly_p)
        
        j = i + 1
        zmieniono_kolejnosc = False
        
        while j < len(S):
            Q = S[j]
            poly_q = Q[0]
            
            # Test 1: Bounding Box 2D na ekranie
            # Jeśli ściany nie zachodzą na siebie wizualnie na ekranie, ich kolejność nie ma znaczenia
            def obwiednia_2d(poly):
                x = [v[0]/(abs(v[2])+1e-6) for v in poly]
                y = [v[1]/(abs(v[2])+1e-6) for v in poly]
                return min(x), max(x), min(y), max(y)
                
            px0, px1, py0, py1 = obwiednia_2d(poly_p)
            qx0, qx1, qy0, qy1 = obwiednia_2d(poly_q)
            
            if px1 < qx0 or qx1 < px0 or py1 < qy0 or qy1 < py0:
                j += 1
                continue
                
            nQ, DQ = wektor_normalny(poly_q)
            
            # Test 2: P jest z tyłu za płaszczyzną Q -> Poprawnie
            if czy_calkowicie_za(poly_p, nQ, DQ):
                j += 1
                continue
                
            # Test 3: Q jest z przodu przed płaszczyzną P -> Poprawnie
            if czy_calkowicie_przed(poly_q, nP, DP):
                j += 1
                continue
                
            # Wykryto konflikt perspektywy! Sprawdzamy odwrotne zasady.
            # Jeśli Q leży z tyłu P, LUB P leży przed Q -> musimy przesunąć Q przed P w kolejce rysowania.
            wymaga_korekty = False
            if czy_calkowicie_za(poly_q, nP, DP): 
                wymaga_korekty = True
            elif czy_calkowicie_przed(poly_p, nQ, DQ): 
                wymaga_korekty = True
            
            if wymaga_korekty:
                q_id = id(poly_q)
                if cofniecia[q_id] < limit_cofniec:
                    cofniecia[q_id] += 1
                    # Wyciągamy Q z miejsca 'j' i wrzucamy je PRZED 'P' (na pozycję 'i')
                    S.insert(i, S.pop(j))
                    zmieniono_kolejnosc = True
                    break # Przerywamy iterację j, zaczynamy analizować nowe S[i]
            
            j += 1
            
        if not zmieniono_kolejnosc:
            i += 1
            
    return S