from functools import partial
from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from io import StringIO
import sys
from PIL import Image, ImageDraw
import math

from main import compute_macro_states


def create_energy_diagram(n, energy, macro_states):
    for i in range(len(macro_states)):
        image = Image.new('RGB', (n * 100, energy * 100 + 10), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.line((0, image.size[1], image.size[0], image.size[1]), fill=128)
        for x in range(1, energy + 1):
            draw.line((0, image.size[1] - x * 100 + 5, image.size[0], image.size[1] - x * 100 + 5), fill=128,
                      width=1)
        e = macro_states[i]
        for j in range(len(e.coeff)):
            if e.coeff[j] != 0:
                t = e.coeff[j]
                j += 1
                if t == 1:
                    t = 2
                else:
                    t += 1
                for x in range(1, t):
                    draw.ellipse(
                        ((image.size[0] / t) * x - 10, image.size[1] - j * 100 + 5 - 10, (image.size[0] / t) * x + 10,
                         image.size[1] - j * 100 + 5 + 10), fill=(0, 0, 0))
        image.save('diagram{0}.png'.format(i), 'PNG')


def valide_nb(self, entry=None):
    if not pattern_area.match(entry.get()):
        entry.config(fg='red')
    else:
        entry.config(fg='black')


if __name__ == "__main__":
    Mafenetre = Tk()
    # type (Boson , Fermions, Classique)
    # energy
    # niveau de dégérénance selon les niveaux
    label_nb_particule = Label(Mafenetre, text='Saisir le nombre de particule')
    label_nb_particule.grid(row='0', column='0')

    pattern_area = re.compile("[0-9]+")

    entry_nb_particule = Entry(Mafenetre, textvariable='nb_particule')
    entry_nb_particule.grid(row='0', column='1')
    entry_nb_particule.bind('<KeyRelease>', partial(valide_nb, entry=entry_nb_particule))

    label_energy = Label(Mafenetre, text="Niveau d'energie")
    label_energy.grid(row='1', column='0')

    entry_energy = Entry(Mafenetre, textvariable='nb_energy')
    entry_energy.grid(row='1', column='1')
    entry_energy.bind('<KeyRelease>', partial(valide_nb, entry=entry_energy))

    label_niveau = Label(Mafenetre, text='Niveau de dégénérescence')
    label_niveau.grid(row='2', column='0')
    explication_degenerescence = Label(Mafenetre, text="Par exemple: 2=3,3=4. (niveau 2 dégénéré 3 fois et niveau 3 dégénéré 4 fois)")
    explication_degenerescence.grid(row='3', column='0')

    entry_degenerescence = Entry(Mafenetre, textvariable='nv_degenerescence')
    entry_degenerescence.grid(row='2', column='1')
    entry_degenerescence.bind('<KeyRelease>', partial(valide_nb, entry=entry_degenerescence))

    type_part = tk.IntVar()

    radioOne = tk.Radiobutton(Mafenetre, text='Classique', variable=type_part, value=1)
    radioOne.grid(row='4', columnspan='2')
    radioOne.select()
    radioTwo = tk.Radiobutton(Mafenetre, text='Boson', variable=type_part, value=2)
    radioTwo.grid(row='5', columnspan='2')
    radioThree = tk.Radiobutton(Mafenetre, text='Fermion', variable=type_part, value=3)
    radioThree.grid(row='6', columnspan='2')

    image_choice = tk.IntVar()
    create_image = tk.Checkbutton(Mafenetre, text="Créer diagrammes macro", variable=image_choice)
    create_image.grid(row='7', columnspan='2')

    def run():
        n = int(entry_nb_particule.get())
        energy = int(entry_energy.get())
        particle_type = int(type_part.get())
        create_diagram = int(image_choice.get())
        degeneration_input = entry_degenerescence.get()
        degeneration_input = degeneration_input.split(',')

        degeneration = []
        for i in range(energy):
            degeneration.append(1)

        for i in range(len(degeneration_input)):
            tmp = degeneration_input[i].split('=')
            if tmp[0] != '':
                degeneration[int(tmp[0]) - 1] = int(tmp[1])

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
            counter = 0
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

            if len(most_probable) == 0:
                print("aucun état n'est plus probable.")
            elif len(most_probable) == 1:
                print("l'état macroscopique le plus probable est le {0}."
                      .format(most_probable[-1][0]))
            else:
                print("les états ", end='')
                for i in range(len(most_probable) - 1):
                    print("{0}, ".format(most_probable[i][0]), end='')
                print('et {0} ont tous une probabilité de {1}.'
                      .format(most_probable[-1][0] + 1,
                              most_probable[-1][1] / sum(state.number_of_micro_states for state in macro_states)))

            for i in range(len(macro_states)):
                nb_etat_micro = math.factorial(n)
                for j in range(len(macro_states[i].coeff)):
                    nb_etat_micro *= (math.pow(degeneration[j], macro_states[i].coeff[j])/math.factorial(macro_states[i].coeff[j]))
                print("Il y a {0} états microscopiques pour l'état macroscopique {1}.".format(int(nb_etat_micro), i))

            if create_diagram == 1:
                create_energy_diagram(n, energy, macro_states)
        elif particle_type == 2:  # Bosons
            print("Avec n={0} bosons et E={1}, il y a {2} états macroscopiques équiprobables."
                  .format(n, energy, len(macro_states)))
            for i in range(len(macro_states)):
                nb_etat_micro = 1
                for j in range(len(macro_states[i].coeff)):
                    nb_etat_micro *= (math.factorial(macro_states[i].coeff[j] + degeneration[j] - 1)/(math.factorial(macro_states[i].coeff[j])*math.factorial(degeneration[j]-1)))
                print("Il y a {0} états microscopiques pour l'état macroscopique {1}.".format(int(nb_etat_micro), i))
            if create_diagram:
                create_energy_diagram(n, energy, macro_states)
        elif particle_type == 3:  # Fermions
            # Get number of states with only one particle
            nb_states = 0
            correct_states = []
            correct_macro_states = []
            for i in range(len(macro_states)):
                state = macro_states[i]
                keep = True
                for e in range(len(state.coeff)):
                    if state.coeff[e] > degeneration[e]:
                        keep = False
                    elif state.coeff[e] == degeneration[e]:
                        pass
                if keep:
                    correct_states.append(i)
                    correct_macro_states.append(macro_states[i])
                    nb_states += 1

            if len(correct_states) > 0:
                print(
                    'Dans le cas des fermions, avec n={0} particules et E={1}, il y a {2} état(s) macroscopique(s) équiprobable(s) : '
                        .format(n, energy, nb_states), end='')
                if len(correct_states) > 1:
                    for i in range(len(correct_states) - 1):
                        print('le {0}, '.format(correct_states[i]), end='')
                    print('et le {0}.'.format(correct_states[-1]))
                else:
                    print('le {0}.'.format(correct_states[-1]))
                for i in correct_states:
                    nb_etat_micro = 1
                    for j in range(len(macro_states[i].coeff)):
                        nb_etat_micro *= (math.factorial(degeneration[j])/(math.factorial(macro_states[i].coeff[j])*math.factorial(degeneration[j]-macro_states[i].coeff[j])))
                    print("Il y a {0} état(s) microscopique(s) pour l'état macroscopique {1}.".format(int(nb_etat_micro), i))

            else:
                print("Dans le cas des fermions, aucun état macroscopique n'est possible.")

            if create_diagram == 1:
                create_energy_diagram(n, energy, correct_macro_states)

        sys.stdout = sys.__stdout__
        global text_out, Mafenetre
        text_out.configure(state='normal')
        text_out.delete('1.0', tk.END)
        text_out.insert(tk.END, custom_output.getvalue())
        text_out.configure(state='disable')
        Mafenetre.mainloop()


    run_button = Button(Mafenetre, text='Run', command=run)
    run_button.grid(row='8', columnspan='2')

    scrollbar = Scrollbar(Mafenetre)

    text_out = ScrolledText(Mafenetre, height=10, width=100, wrap="word")
    text_out.configure(state='disable')
    text_out.grid(row='9', columnspan='2')

    Mafenetre.mainloop()
