import numpy as np
from functools import cmp_to_key

import numpy as np

import numpy as np

def get_plane_equation(poly):
    """
    poly: lista array([-4., -1., 5., 1.])
    Zwraca: A, B, C, D
    """
    # Wyciągamy współrzędne x, y, z dla trzech punktów
    p0 = poly[0][:3]
    p1 = poly[1][:3]
    p2 = poly[2][:3]
    
    # Wektory pomocnicze
    v1 = p1 - p0
    v2 = p2 - p0
    
    # Iloczyn wektorowy daje wektor normalny [A, B, C]
    normal = np.cross(v1, v2)
    A, B, C = normal
    
    # D = -(A*x + B*y + C*z)
    D = -np.dot(normal, p0)
    
    return A, B, C, D

import numpy as np

def relacja_scian(sciana_A, sciana_B):
    poly_a, poly_b = sciana_A[0], sciana_B[0]
    
    # 1. Test Min-Max Z (Najszybszy i najpewniejszy)
    z_min_a, z_max_a = min(v[2] for v in poly_a), max(v[2] for v in poly_a)
    z_min_b, z_max_b = min(v[2] for v in poly_b), max(v[2] for v in poly_b)
    
    # Jeśli zakresy Z w ogóle się nie nakładają, nie ma co liczyć płaszczyzn
    if z_max_a <= z_min_b: return -1 # A jest całkowicie za B
    if z_min_a >= z_max_b: return 1  # A jest całkowicie przed B

    # 2. Test płaszczyzny (z większą tolerancją - epsilon)
    a, b, c, d = get_plane_equation(poly_b)
    znak_oka = np.sign(d)
    epsilon = 1e-4 # Tolerancja dla krawędzi
    
    za = True
    for p in poly_a:
        val = a*p[0] + b*p[1] + c*p[2] + d
        # Sprawdzamy czy punkt jest po stronie oka
        if np.sign(val) == znak_oka and abs(val) > epsilon:
            za = False
            break
    
    if za: return -1
    
    # 3. Test odwrotny
    a2, b2, c2, d2 = get_plane_equation(poly_a)
    znak_oka2 = np.sign(d2)
    
    przed = True
    for p in poly_b:
        val = a2*p[0] + b2*p[1] + c2*p[2] + d2
        if np.sign(val) != znak_oka2 and abs(val) > epsilon:
            przed = False
            break
            
    if przed: return -1

    # 4. Jeśli nadal nie wiadomo (np. przecinają się), używamy środka ciężkości
    return -1 if np.mean([v[2] for v in poly_a]) > np.mean([v[2] for v in poly_b]) else 1

def sortuj_sciany(sciany):
    """
    Sortowanie 'malarskie' - od najdalszych do najbliższych.
    Używamy Z_max jako głównego kryterium (tak jak w Twoim 1. rozwiązaniu),
    ale dodajemy Z_mean dla stabilności.
    """

    # Sortujemy malejąco: od największego Z (najdalej) do najmniejszego (najbliżej)
    return sorted(sciany, key=cmp_to_key(relacja_scian))