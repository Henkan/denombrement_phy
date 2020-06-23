import itertools
import collections
import math

from macro_state import MacroState


def main():
    n = 2  # int(input('Nombre de particules (n): \n > '))
    energy = 4  # int(input('Énergie totale (E=x*e): \n > '))
    particle_type = 1  # int(input('Type de particule (1=classique, 2=bosons, 3=fermions): \n > ')
    degeneration_input = "2=2"
    degeneration_input = degeneration_input.split(',')

    degeneration = []
    for i in range(energy):
        degeneration.append(1)

    for i in range(len(degeneration_input)):
        tmp = degeneration_input[i].split('=')
        if tmp[0] != '':
            degeneration[int(tmp[0]) - 1] = int(tmp[1])

    # TODO: check examples
    macro_states = compute_macro_states(n, energy, degeneration)


    '''
    Display stuff
    '''
    print('Les états macroscopiques sont:')
    for i in range(len(macro_states)):
        print("\tÉtat {0}: {{".format(i), end='')
        for j in range(len(macro_states[i].coeff)):
            print("n{0}={1}, ".format(j + 1, macro_states[i].coeff[j]), end='')
        print('...}')

    if particle_type == 1:  # Classic particle
        print("Nombre d'états microscopiques:")
        counter = 1
        for state in macro_states:
            print("\t{0} pour l'état macro {1}".format(int(state.number_of_micro_states), counter))
            counter += 1

        print('Il y a donc un total de {0} états microscopiques.'.format(
            int(sum([s.number_of_micro_states for s in macro_states]))))

        # Get number of states with the same highest probability
        most_probable = []
        for i in range(len(macro_states)):
            if len(most_probable) > 0:
                if macro_states[i].number_of_micro_states > most_probable[-1][1]:
                    most_probable = [(i, macro_states[i].number_of_micro_states)]
                elif macro_states[i].number_of_micro_states == most_probable[-1][1]:
                    most_probable.append((i, macro_states[i].number_of_micro_states))
            else:
                most_probable.append((i, macro_states[i].number_of_micro_states))

        print("Avec n={0} particules classiques et E={1}, ".format(n, energy), end='')

        if len(most_probable) == 1:
            print("l'état macroscopique le plus probable est le {0}."
                  .format(most_probable[-1][0] + 1))
        else:
            print("les états ", end='')
            for i in range(len(most_probable) - 1):
                print("{0}, ".format(most_probable[i][0] + 1), end='')
            print('et {0} ont tous une probabilité de {1}.'
                  .format(most_probable[-1][0] + 1,
                          most_probable[-1][1] / sum(state.number_of_micro_states for state in macro_states)))

    elif particle_type == 2:  # Bosons
        print("Avec n={0} bosons et E={1}, il y a {2} états macroscopiques équiprobables."
              .format(n, energy, len(macro_states)))
    elif particle_type == 3:  # Fermions
        # Get number of states with only one particle
        nb_states = 0
        for state in macro_states:
            keep = True
            for e in state.coeff:
                if e not in [0, 1]:
                    keep = False
            if keep:
                nb_states += 1

        print('Avec n={0} fermions et E={1}, il y a {2} états macroscopiques équiprobables.'
              .format(n, energy, nb_states))


def compute_macro_states(n, energy, degeneration):
    possible_levels = []
    to_keep = []
    handle_degeneration = len(degeneration) != 0
    # Create the different possible levels on energy
    # based on the total energy and the number of particles
    for j in range(1, energy+1):
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

    states = []
    # Compute the number of possible states
    nb_micro_per_macro = []
    for i in range(len(to_keep)):
        if not handle_degeneration:
            state = MacroState()
            coeff = []
            # Formulae is n!/product(ni!)
            number_of_states = math.factorial(n)
            denominator = 1

            # Count number of each state, e.g. (1,1,2) returns {1:2,2:1}
            count = collections.Counter(k for k in to_keep[i])

            for j in range(1, energy + 1):  # All levels
                val = 0
                for item in count.items():
                    if item[0] == j:
                        val = item[1]
                coeff.append(val)
                denominator *= math.factorial(val)

            # Apply formula
            number_of_states /= denominator
            nb_micro_per_macro.append(number_of_states)
            # Create object
            state.number_of_micro_states = number_of_states
            state.coeff = coeff
            states.append(state)
        else:
            # Handle degeneration
            state = MacroState()
            coeff = []
            # Init formulae
            number_of_states = math.factorial(n)
            product = 1

            # Count number of each state, e.g. (1,1,2) returns {1:2,2:1}
            count = collections.Counter(k for k in to_keep[i])

            for level in range(1, energy + 1):  # All levels
                ni = 0
                for item in count.items():
                    if item[0] == level:
                        ni = item[1]
                coeff.append(ni)
                product *= pow(degeneration[level-1], ni)
                product /= math.factorial(ni)

            # Apply formula
            number_of_states *= product

            # Apply formula
            nb_micro_per_macro.append(number_of_states)
            # Create object
            state.number_of_micro_states = number_of_states
            state.coeff = coeff
            states.append(state)

    return states


if __name__ == '__main__':
    main()
