from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from io import StringIO
import sys

from main import compute_macro_states

if __name__ == "__main__":
    Mafenetre = Tk()
    # type (Boson , Fermions, Classique)
    # energy
    # niveau de dégérénance selon les niveaux
    label_nb_particule = Label(Mafenetre, text='Saisir le nombre de particule')
    label_nb_particule.grid(row='0', column='0')

    entry_nb_particule = Entry(Mafenetre, textvariable='nb_particule')
    entry_nb_particule.grid(row='0', column='1')

    label_energy = Label(Mafenetre, text="Niveau d'energie")
    label_energy.grid(row='1', column='0')

    entry_energy = Entry(Mafenetre, textvariable='nb_energy')
    entry_energy.grid(row='1', column='1')

    label_niveau = Label(Mafenetre, text='Niveau de dégénérescence')
    label_niveau.grid(row='2', column='0')

    entry_degenerescence = Entry(Mafenetre, textvariable='nv_degenerescence')
    entry_degenerescence.grid(row='2', column='1')

    type_part = tk.IntVar()

    radioOne = tk.Radiobutton(Mafenetre, text='Classique', variable=type_part, value=1)
    radioOne.grid(row='3', columnspan='2')
    radioTwo = tk.Radiobutton(Mafenetre, text='Boson', variable=type_part, value=2)
    radioTwo.grid(row='4', columnspan='2')
    radioThree = tk.Radiobutton(Mafenetre, text='Fermion', variable=type_part, value=3)
    radioThree.grid(row='5', columnspan='2')


    def run():
        n = int(entry_nb_particule.get())
        energy = int(entry_energy.get())
        particle_type = int(type_part.get())
        degeneration_input = entry_degenerescence.get()
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
        custom_output = StringIO()
        sys.stdout = custom_output
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

        sys.stdout = sys.__stdout__
        global text_out, Mafenetre
        text_out.configure(state='normal')
        text_out.delete('1.0', tk.END)
        text_out.insert(tk.END, custom_output.getvalue())
        text_out.configure(state='disable')
        Mafenetre.mainloop()


    run_button = Button(Mafenetre, text='Run', command=run)
    run_button.grid(row='6', columnspan='2')

    scrollbar = Scrollbar(Mafenetre)

    text_out = ScrolledText(Mafenetre, height=10, width=100, wrap="word")
    text_out.configure(state='disable')
    text_out.grid(row='7', columnspan='2')

    Mafenetre.mainloop()
