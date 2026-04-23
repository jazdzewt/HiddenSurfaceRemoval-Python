import numpy as np

def get_plane_eq(poly):
    """Zwraca [A, B, C, D] dla Ax + By + Cz + D = 0."""
    p0, p1, p2 = poly[0][:3], poly[1][:3], poly[2][:3]
    n = np.cross(p1 - p0, p2 - p0)
    # Zabezpieczenie przed kolinearnością
    if np.linalg.norm(n) < 1e-9:
        n = np.cross(poly[1][:3] - poly[0][:3], poly[-1][:3] - poly[0][:3])
    d = -np.dot(n, p0)
    return n, d

def get_aabb(poly):
    """Otoczenie prostokątne w X i Y."""
    pts = np.array([v[:3] for v in poly])
    return np.min(pts[:, 0]), np.max(pts[:, 0]), np.min(pts[:, 1]), np.max(pts[:, 1])

def is_behind(poly_p, n_q, d_q):
    """Test: Czy wielokąt P leży ZA płaszczyzną Q względem oka (0,0,0)."""
    eye_val = d_q 
    eye_sign = np.sign(eye_val)
    eps = 1e-5
    for v in poly_p:
        val = np.dot(n_q, v[:3]) + d_q
        # Jeśli punkt ma ten sam znak co oko, jest PRZED płaszczyzną
        if np.sign(val) == eye_sign and abs(val) > eps:
            return False
    return True

def is_in_front(poly_q, n_p, d_p):
    """Test: Czy wielokąt Q leży PRZED płaszczyzną P względem oka (0,0,0)."""
    eye_val = d_p
    eye_sign = np.sign(eye_val)
    eps = 1e-5
    for v in poly_q:
        val = np.dot(n_p, v[:3]) + d_p
        # Jeśli punkt ma inny znak niż oko, jest ZA płaszczyzną
        if np.sign(val) != eye_sign and abs(val) > eps:
            return False
    return True

def sortuj_sciany(sciany):
    # Wstępne sortowanie po Z_max (Najdalsze na początek listy)
    # Przyjmujemy: większe Z = dalej
    S = sorted(sciany, key=lambda w: max(v[2] for v in w[0]), reverse=True)
    
    i = 0
    while i < len(S):
        P = S[i] # Wielokąt potencjalnie dalszy
        z_min_p = min(v[2] for v in P[0])
        
        j = i + 1
        konflikt_rozwiazany = True
        
        while j < len(S):
            Q = S[j] # Wielokąt potencjalnie bliższy
            
            # Jeśli Q jest całkowicie bliżej niż P w osi Z, nie ma konfliktu
            if max(v[2] for v in Q[0]) <= z_min_p:
                j += 1
                continue
            
            # --- TWOJE TESTY 1-4 ---
            
            # 1. Otoczenia prostokątne X, Y
            min_xp, max_xp, min_yp, max_yp = get_aabb(P[0])
            min_xq, max_xq, min_yq, max_yq = get_aabb(Q[0])
            
            if (max_xp <= min_xq or max_xq <= min_xp or 
                max_yp <= min_yq or max_yq <= min_yp):
                j += 1
                continue

            # 2. Rzuty (pomińmy dla wydajności, AABB zazwyczaj wystarcza dla prostych brył)

            # 3. P za płaszczyzną Q
            nq, dq = get_plane_eq(Q[0])
            if is_behind(P[0], nq, dq):
                j += 1
                continue
                
            # 4. Q przed płaszczyzną P
            np_eq, dp_eq = get_plane_eq(P[0])
            if is_in_front(Q[0], np_eq, dp_eq):
                j += 1
                continue

            # --- KROK 5: Zamiana ról ---
            # Jeśli żaden test nie przeszedł, sprawdzamy czy Q zasłania P
            # Testujemy czy Q jest ZA płaszczyzną P LUB P jest PRZED płaszczyzną Q
            if is_behind(Q[0], np_eq, dp_eq) or is_in_front(P[0], nq, dq):
                # Q jest w rzeczywistości dalej niż P - przesuń Q na miejsce i
                temp_q = S.pop(j)
                S.insert(i, temp_q)
                konflikt_rozwiazany = False
                break
            else:
                # KROK 6: Podział (Polygon Splitting)
                # W Twoim przypadku (brak przenikania) nie powinno się to dziać.
                # Używamy Z_mean jako ostatecznego ratunku.
                j += 1
        
        if konflikt_rozwiazany:
            i += 1
            
    return S