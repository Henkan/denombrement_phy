import itertools


def main():
    n = 3  # int(input('Nombre de particules (n): \n > '))
    energy = 6  # int(input('Énergie totale (E=x*e): \n > '))
    print('n = ', n)
    print('e = ', energy)

    to_keep = []
    possible_levels = []
    # Create the different possible levels on energy
    # based on the total energy and the number of particles
    for j in range(1, energy - n + 1 + 1):
        possible_levels.append(j)

    for i in range(1, energy - n + 1 + 1):
        # Get all the possible combinations
        for subset in itertools.combinations_with_replacement(possible_levels, n):
            _sum = 0
            for j in range(len(subset)):
                _sum += subset[j]

            # Only keep those that correspond to the total energy
            if _sum == energy and subset not in to_keep:
                to_keep.append(subset)

    print(to_keep)


if __name__ == '__main__':
    main()
