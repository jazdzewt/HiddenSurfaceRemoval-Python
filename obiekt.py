
class Obiekt:
    def __init__(self, name):
        self.name = name
        self.color = []
        self.wezly = []
        self.krawedzie = []

    def dodaj_wezel(self, wezel):
        self.wezly.append(wezel)

    def dodaj_krawedz(self, krawedz):
        self.krawedzie.append(krawedz)

class Scena: 
    def __init__(self):
        self.obiekty = []
    
    def dodaj_obiekt(self, obiekt):
        self.obiekty.append(obiekt)
