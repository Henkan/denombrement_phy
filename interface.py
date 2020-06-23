from tkinter import *
import tkinter as tk

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

run_button = Button(Mafenetre, text='run')
run_button.grid(row='6', columnspan='2')

text_out = Text(Mafenetre, height=6, width=50, wrap="word")
text_out.configure(state='disabled')
text_out.grid(row='7', columnspan='2')

Mafenetre.mainloop()
