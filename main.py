import itertools
import collections
import math


def main():
    n = 3  # int(input('Nombre de particules (n): \n > '))
    energy = 6  # int(input('Énergie totale (E=x*e): \n > '))

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

    print('Les états macroscopiques possibles sont:')
    # Compute the number of possible states
    most_probable = (0, 0)
    nb_micro_per_state = []
    for i in range(len(to_keep)):
        # Formulae is n!/product(ni!)
        number_of_states = math.factorial(n)
        denominator = 1

        # Count number of each state, e.g. (1,1,2) returns {1:2,2:1}
        count = collections.Counter(k for k in to_keep[i])
        print('\tÉtat {0}: {{'.format(i + 1), end="")

        for j in range(1, energy + 1):
            val = 0
            for item in count.items():
                if item[0] == j:
                    val = item[1]
            print('n{0}={1}, '.format(j, val), end='')
            denominator *= math.factorial(val)
        print('...}')

        # Apply formula
        number_of_states /= denominator
        nb_micro_per_state.append(number_of_states)
        if number_of_states > most_probable[1]:
            most_probable = (i, number_of_states)

    print("Nombre d'états microscopiques:")
    counter = 1
    for nb_states in nb_micro_per_state:
        print("\t{0} pour l'état macro {1}".format(int(nb_states), counter))
        counter += 1

    print('Il y a donc un total de {0} états microscopiques'.format(int(sum(nb_micro_per_state))))
    print("Avec n={0} particules et E={1}, l'état macroscopique le plus probable est le {2}.".format(n, energy,
                                                                                                     most_probable[
                                                                                                         0] + 1))


if __name__ == '__main__':
    main()
