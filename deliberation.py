import tkinter as tk
from tkinter import ttk
import sqlite3
from base_page import BasePage

class Deliberation:
    def __init__(self):
        self.conn = sqlite3.connect('bfem.db')
        self.cursor = self.conn.cursor()

    def calculer_points(self, numero_table):
        self.cursor.execute('SELECT * FROM Notes WHERE Numero_Table = ?', (numero_table,))
        notes = self.cursor.fetchone()

        if notes:
            # Remplacer les valeurs None par 0
            notes = [0 if note is None else note for note in notes]

            points = (
                (notes[1] * 2) +  # Compo_Franc
                (notes[3] * 1) +  # Dictee
                (notes[5] * 1) +  # Etude_de_texte
                (notes[7] * 1) +  # Instruction_Civique
                (notes[9] * 2) +  # Histoire_Geographie
                (notes[11] * 4) +  # Mathematiques
                (notes[13] * 2) +  # PC_LV2
                (notes[15] * 2) +  # SVT
                (notes[17] * 2) +  # Anglais1
                (notes[19] * 1) +  # Anglais_Oral
                (notes[21] * 1)    # EPS
            )

            if notes[22] is not None and float(notes[22]) > 10:
                points += (float(notes[22]) - 10)

            return points
        return 0

    def deliberer(self, numero_table):
        points = self.calculer_points(numero_table)
        if points >= 180:
            return "Admis"
        elif points >= 153:
            return "Second Tour"
        else:
            return "Échec"

    def __del__(self):
        self.conn.close()

class DeliberationPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Délibération des résultats")
        self.deliberation = Deliberation()

        self.tree = ttk.Treeview(self, columns=("Numéro Table", "Nom", "Prénom", "Points", "Résultat"), show="headings")
        self.tree.heading("Numéro Table", text="Numéro Table")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Prénom", text="Prénom")
        self.tree.heading("Points", text="Points")
        self.tree.heading("Résultat", text="Résultat")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.load_button = ttk.Button(self, text="Charger les données", command=self.load_data, style="Blue.TButton")
        self.load_button.pack(pady=10)

    def load_data(self):
        self.deliberation.cursor.execute('SELECT Numero_Table, Nom, Prenom_s FROM Candidat')
        candidats = self.deliberation.cursor.fetchall()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for candidat in candidats:
            numero_table, nom, prenom = candidat
            points = self.deliberation.calculer_points(numero_table)
            resultat = self.deliberation.deliberer(numero_table)
            self.tree.insert("", "end", values=(numero_table, nom, prenom, points, resultat))