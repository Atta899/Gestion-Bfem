import sqlite3
import tkinter as tk
from tkinter import messagebox

class Candidat:
    def __init__(self):
        self.conn = sqlite3.connect('bfem.db')
        self.cursor = self.conn.cursor()

    def ajouter_candidat(self, numero_table, prenom, nom, date_naissance, lieu_naissance, sexe, nationalite, choix_epr_facultative, epreuve_facultative, aptitude_sportive):
        try:
            self.cursor.execute('''
                INSERT INTO Candidat (Numero_Table, Prenom_s, Nom, Date_Naissance, Lieu_Naissance, Sexe, Nationalite, Choix_Epr_Facultative, Epreuve_Facultative, Aptitude_Sportive)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (numero_table, prenom, nom, date_naissance, lieu_naissance, sexe, nationalite, choix_epr_facultative, epreuve_facultative, aptitude_sportive))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")
            return False

    def modifier_candidat(self, numero_table, prenom, nom, date_naissance, lieu_naissance, sexe, nationalite, choix_epr_facultative, epreuve_facultative, aptitude_sportive):
        try:
            self.cursor.execute('''
                UPDATE Candidat
                SET Prenom_s = ?, Nom = ?, Date_Naissance = ?, Lieu_Naissance = ?, Sexe = ?, Nationalite = ?, Choix_Epr_Facultative = ?, Epreuve_Facultative = ?, Aptitude_Sportive = ?
                WHERE Numero_Table = ?
            ''', (prenom, nom, date_naissance, lieu_naissance, sexe, nationalite, choix_epr_facultative, epreuve_facultative, aptitude_sportive, numero_table))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")
            return False

    def supprimer_candidat(self, numero_table):
        try:
            self.cursor.execute('DELETE FROM Candidat WHERE Numero_Table = ?', (numero_table,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")
            return False

    def lister_candidats(self, numero_table=None):
        try:
            if numero_table:
                self.cursor.execute('SELECT * FROM Candidat WHERE Numero_Table = ?', (numero_table,))
                return self.cursor.fetchone()
            else:
                self.cursor.execute('SELECT * FROM Candidat')
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la lecture: {str(e)}")
            return None

    def rechercher_candidat(self, numero_table):
        try:
            self.cursor.execute('SELECT * FROM Candidat WHERE Numero_Table = ?', (numero_table,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche: {str(e)}")
            return None

    def compter_candidats(self):
        try:
            self.cursor.execute('SELECT COUNT(*) FROM Candidat')
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors du comptage: {str(e)}")
            return 0

    def __del__(self):
        self.conn.close()