# fichier: jury.py
import sqlite3

class Jury:
    def __init__(self, db_name="bfem.db"):
        self.db_name = db_name

    def enregistrer_jury(self, donnees):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Jury (Region, Departement, Localite, Centre_Examen, President_Jury, Telephone) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            donnees["Région"],
            donnees["Département"],
            donnees["Localité"],
            donnees["Centre d'Examen"],
            donnees["Président de Jury"],
            donnees["Téléphone"]
        ))
        conn.commit()
        conn.close()
