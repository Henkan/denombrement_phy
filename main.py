import itertools


def main():
    n = 3  # int(input('Nombre de particules (n): \n > '))
    energy = 6  # int(input('Énergie totale (E=x*e): \n > '))
    print('n = ', n)
    print('e = ', energy)

    to_keep = []
    possible_levels = []
    for j in range(1, energy - n + 1 + 1):
        possible_levels.append(j)

    for i in range(1, energy - n + 1 + 1):
        for subset in itertools.combinations_with_replacement(possible_levels, n):
            _sum = 0
            for j in range(len(subset)):
                _sum += subset[j]

            if _sum == energy and subset not in to_keep:
                to_keep.append(subset)

    print(to_keep)
    print(len(to_keep))


if __name__ == '__main__':
    main()
