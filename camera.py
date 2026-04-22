import numpy as np

class Camera:
    def __init__(self):

        self.pozycja = np.array([0.0, 0.0, 0.0, 1.0])

        # góra / dół
        self.pochylenie = 0 

        # lewo / prawo
        self.obrot = 0 


        # przechylenie na boki 
        self.przechylenie = 0   

        self.f = 600

    def macierz_widoku(self):

        # macierz translacji 
        t_mat = np.array([
            [1, 0, 0, -self.pozycja[0]],
            [0, 1, 0, -self.pozycja[1]],
            [0, 0, 1, -self.pozycja[2]],
            [0, 0, 0, 1]])

        # macierze rotacji  
        r_pochylenie = np.array([
            [1, 0, 0, 0],
            [0, np.cos(self.pochylenie), -np.sin(self.pochylenie), 0],
            [0, np.sin(self.pochylenie), np.cos(self.pochylenie), 0],  
            [0, 0, 0, 1]])

        r_przechylenie = np.array([
            [np.cos(self.przechylenie), -np.sin(self.przechylenie), 0, 0],
            [np.sin(self.przechylenie), np.cos(self.przechylenie), 0, 0], 
            [0, 0, 1, 0],
            [0, 0, 0, 1]])

        r_obrot = np.array([
            [np.cos(self.obrot), 0, np.sin(self.obrot), 0],
            [0, 1, 0, 0],
            [-np.sin(self.obrot), 0, np.cos(self.obrot), 0],
            [0, 0, 0, 1]])
        # macierz widoku
        macierz_w = r_przechylenie @ r_pochylenie @ r_obrot @ t_mat

        return macierz_w

    def rzutowanie(self, punkt, szerokosc, wysokosc):

        x = punkt[0]
        y = punkt[1]
        z = punkt[2]
        
        if z <= 0.1:
            return None 
        
        x_2d = (x * self.f) / z + szerokosc / 2
        y_2d = (-y * self.f) / z + wysokosc / 2
        
        return int(x_2d), int(y_2d)