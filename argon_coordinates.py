from __future__ import division
from math import sqrt, log
from random import random, choice


k = 0.00831


def multiply_vector_by_number(number, vector):
    return [number * x for x in vector]


def add_vectors(a, b, c):
    return [x1 + x2 + x3 for x1, x2, x3 in zip(a, b, c)]


def atoms_coordinates(n, b1, b2, b3):

    atoms = []
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                atom = add_vectors(multiply_vector_by_number(ix - (n - 1.0)/2, b1),
                                   multiply_vector_by_number(iy - (n - 1.0)/2, b2),
                                   multiply_vector_by_number(iz - (n - 1.0)/2, b3))
                atoms.append(atom)
    return atoms


def save_to_file(coordinates, filename):
    with open(filename, 'w+') as f:
        for x, y, z in coordinates:
            f.write('%s\t%s\t%s\n' % (x, y, z))


def read_parameters(filename):
    with open(filename) as f:
        data = f.read()

    numbers = data.split()
    if len(numbers) != 2:
        print('Wrong %s data' % filename)
        return None
    else:
        a = float(numbers[0])
        n = int(numbers[1])
    return a, n


def start_momentum(atoms, m, To):
    max_energy = - k / 2 * To
    energies = []
    for atom in atoms:
        energies.append((max_energy * log(random()), max_energy * log(random()), max_energy * log(random())))

    # normalization
    average_energy = sum([element for tupl in energies for element in tupl]) / len(energies) / 3

    norm_factor = - max_energy / average_energy
    energies = [multiply_vector_by_number(norm_factor, energy) for energy in energies]

    momentums = []
    
    def compute_momentum(x):
        return choice([-1, 1]) * sqrt(2 * m * x)

    for energy in energies:
        momentum = (compute_momentum(energy[0]), compute_momentum(energy[1]), compute_momentum(energy[2]))
        momentums.append(momentum)
    return momentums


def main():
    assert(multiply_vector_by_number(3, (2, 3, 0)) == [6, 9, 0])
    assert(add_vectors((1, 2, 3), (3, 4, 5), (3, 3, 3)) == [7, 9, 11])
    
    parameters = read_parameters('argon.input')

    if not parameters:
        return 1
    else:
        a, n = parameters
 
    # argon structure
    b1 = (a, 0, 0)
    b2 = (a/2, a * sqrt(3)/ 2, 0)
    b3 = (a/2, a * sqrt(3)/ 6, a * sqrt(2/3))

    # box structure
    p1 = (a, 0, 0)
    p2 = (0, a, 0)
    p3 = (0, 0, a)

    atoms = atoms_coordinates(n, b1, b2, b3)
    save_to_file(atoms, 'aus.dat')

    # atoms = atoms_coordinates(n, p1, p2, p3)
    # save_to_file(atoms, 'simple.dat')
    
    m = 39.948
    To = 100
    momentums = start_momentum(atoms, m, To)
    save_to_file(momentums, 'momentums.dat')


if __name__ == '__main__':
    main()
