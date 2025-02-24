import sqlite3

class Repechage:
    def __init__(self, db_name="bfem.db"):
        self.db_name = db_name

    def get_candidats_repechables(self):
        """
        Récupère la liste des candidats repêchables pour le premier tour.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.Numero_Table, c.Prenom_s, c.Nom, n.Points, l.Moyenne_Cycle, l.Nombre_de_fois
                FROM Candidat c
                JOIN Notes n ON c.Numero_Table = n.Numero_Table
                JOIN Livret_Scolaire l ON c.Numero_Table = l.Numero_Table
                WHERE (n.Points BETWEEN 144 AND 179.9 AND l.Moyenne_Cycle >= 12)
                OR (n.Points BETWEEN 171 AND 179.9)
                OR (n.Points BETWEEN 144 AND 152.9 AND l.Nombre_de_fois <= 2)
            ''')
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur SQL : {e}")
            return []
        finally:
            conn.close()

    def get_candidats_repechables_second_tour(self):
        """
        Récupère la liste des candidats repêchables pour le second tour.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.Numero_Table, c.Prenom_s, c.Nom, n.Points, l.Moyenne_Cycle, l.Nombre_de_fois
                FROM Candidat c
                JOIN Notes n ON c.Numero_Table = n.Numero_Table
                JOIN Livret_Scolaire l ON c.Numero_Table = l.Numero_Table
                WHERE n.Points BETWEEN 76 AND 79.9 AND l.Nombre_de_fois <= 2
            ''')
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur SQL : {e}")
            return []
        finally:
            conn.close()