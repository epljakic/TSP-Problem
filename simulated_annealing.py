import random
import math as m
import numpy as np
import matplotlib.pyplot as plt

class SimulatedAnnealing(object):
    def __init__(self, coordinates, T=-1, T_a=-1, T_end=-1, max_iter=-1):
        """
        Inicijalizacija datog objekta
        :param coordinates: koordinate
        :param T: pocetna temperatura
        :param T_a: koeficijent za eksponencijalno smanjenje temperature
        :param T_end: krajnja vrednost temperature
        :param max_iter: maksimalni broj iteracija
        """
        self.coords = coordinates
        self.N = len(coordinates)
        self.T = m.sqrt(self.N) if T == -1 else T
        self.T_start = self.T
        self.T_a = 0.995 if T_a == -1 else T_a
        self.T_end = 1e-6 if T_end == -1 else T_end
        self.max_iter = 100000 if max_iter == -1 else max_iter
        self.iter = 1

        self.nodes = [i for i in range(self.N)]

        self.best_solution = None
        self.best_distance = float("Inf")
        self.distance_list = []

    def distance_point_to_point(self, node1, node2):
        """
        Funkcija koja vraca rastojanje izmedju dve tacke
        """
        coord1, coord2 = self.coords[node1], self.coords[node2]
        return np.abs(coord1[0] - coord2[0]) + np.abs(coord1[1] - coord2[1])

    def distance(self, solution):
        """
        Funkcija koja vraca ukupnu predjenu putanju
        """
        cur_dist = 0
        for i in range(self.N-1):
            cur_dist += self.distance_point_to_point(solution[i % self.N], solution[(i+1) % self.N])
        return  cur_dist

    def distance_plot(self):
        """
        Funkcija za iscrtavanje vrednosti optimizacione funkcije tokom iteracija
        """
        t = np.arange(0.0, len(self.distance_list), 1.0)
        plt.figure(figsize=(12, 8))
        plt.plot(t, self.distance_list)
        plt.title("Simulirano kaljenje")
        plt.ylabel("Vrednost optimizacione funkcije")
        plt.xlabel("Iteracije")
        plt.show()

    def initial_solution(self):
        """
        Funkcija koja vraca pocetno resenje i distancu za to resenje
        """
        solution = random.sample(self.nodes, len(self.nodes))

        cur_distance = self.distance(solution)
        if cur_distance < self.best_distance:
            self.best_distance = cur_distance
            self.best_solution = solution
        self.distance_list.append(cur_distance)
        return solution, cur_distance

    def accept(self, solution):
        """
        Funkcija koja sluzi za prihvatanje novog resenja
        """
        solution_distance = self.distance(solution)
        if solution_distance < self.cur_distance:
            self.cur_distance, self.cur_solution = solution_distance, solution
            if solution_distance < self.best_distance:
                self.best_distance, self.best_solution = solution_distance, solution
        else:
            if random.random() < m.exp(-abs(solution_distance - self.cur_distance)/self.T):
                self.cur_distance, self.cur_solution = solution_distance, solution

    def simanneal(self):
        """
        Funkcija u kojoj je implementiran algoritam simuliranog kaljenja
        """
        # Inicijalizujemo pocetno resenje i distancu takvog resenja
        self.cur_solution, self.cur_distance = self.initial_solution()

        # Pocetak simuliranog kaljenja
        print("Simulirano kaljenje.")
        while self.T >= self.T_end and self.iter < self.max_iter:
            # Stvaranje novog resenja
            next_solution = list(self.cur_solution)
            k = random.randint(2, self.N - 1)
            l = random.randint(0, self.N - k)
            next_solution[l : (l+k)] = reversed(next_solution[l : (l+k)])

            # Prihvatanje novog resenja
            self.accept(next_solution)
            self.T *= self.T_a
            if self.T <= self.T_end:
                self.T = self.T_end
            self.iter += 1

            # Cuvanje vrednosti optimizacione funkcije tokom iteracija
            self.distance_list.append(self.cur_distance)

        # Najbolje pronadjeno resenje
        print("Najmanje pronadjeno rastojanje je: ", self.best_distance)
        # Najbolji redosled tacaka
        print("Redosled tacaka za koje je dobijeno ovo rastojanje je:")
        print(self.best_solution)

