import random
import numpy as np
import matplotlib.pyplot as plt
from simulirano_kaljenje import SimulatedAnnealing

def read_coordinates(path):
    """
        Funkcija koja ucitava koordinate tacaka iz txt fajla
    """
    coordinates = []
    with open(path, "r") as f:
        for line in f.readlines():
            line = [float(x.replace("\n", "")) for x in line.split("  ")]
            coordinates.append(line)
    return coordinates

def distance(coordinates):
    """
        Funkcija koja vraca ukupnu predjenu putanju za dato resenje
    """
    dist = 0
    for i in range(1, len(coordinates)):
        dist += np.abs(coordinates[i][0] - coordinates[i-1][0]) + np.abs(coordinates[i][1] - coordinates[i-1][1])
    return dist

def temp_start(coordinates):
    """
        Funkcija koja vraca pocetnu temperaturu
    """
    N = 200
    f_sr = 0
    delta_f_sr = 0
    f = []

    for i in range(N):
        new_coordinates = random.sample(coordinates, len(coordinates))
        f.append(distance(new_coordinates))
        f_sr += f[i]
    f_sr /= N

    for i in range(N):
        delta_f_sr += np.abs(f[i] - f_sr)

    T0 = delta_f_sr/N
    return T0

if __name__ == "__main__":
    # Ucitavanje koordinata
    coordinates = read_coordinates("coordinates.txt")
    # Racunanje pocetne temperature
    T0 = temp_start(coordinates)

    # Iscrtavanje redosleda povezivanja tacaka pre simuliranog kaljenja
    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    for first, second in zip(coordinates[:-1], coordinates[1:]):
        ax1.plot([first[0], second[0]], [first[1], second[1]], 'b')
    for c in coordinates:
        ax1.plot(c[0], c[1], 'ro')
    ax1.title.set_text("Pre simuliranog kaljenja")

    # Simulirano kaljenje
    # Pravljenje objekta klase SimulatedAnnealing
    SA = SimulatedAnnealing(coordinates, T=T0, max_iter=100000)
    # Pozivanje funkcije za simulirano kaljenje
    SA.simanneal()

    # Cuvanje konacnog resenja  u formatu x-y koordinata
    best_coordinates = []
    for i in range(SA.N):
        best_coordinates.append(coordinates[SA.best_solution[i]])

    # Iscrtavanje redosleda povezivanja tacaka pre simuliranog kaljenja
    for first, second in zip(best_coordinates[:-1], best_coordinates[1:]):
        ax2.plot([first[0], second[0]], [first[1], second[1]], 'b')
    for c in best_coordinates:
        ax2.plot(c[0], c[1], 'ro')
    ax1.title.set_text("Posle simuliranog kaljenja")
    plt.show()

    # Iscrtavanje vrednosti optimizacione funkcije tokom iteracija
    SA.distance_plot()



