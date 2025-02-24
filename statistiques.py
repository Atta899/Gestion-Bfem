# statistiques.py

import sqlite3

class Statistiques:
    def __init__(self, db_name="bfem.db"):
        self.db_name = db_name

    def nombre_candidats(self):
        """
        Retourne le nombre total de candidats.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM Candidat')
        result = cursor.fetchone()[0]
        conn.close()
        return result

    def moyenne_points(self):
        """
        Retourne la moyenne des points de tous les candidats.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT AVG(Points) FROM Notes')
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0  # Retourne 0 si aucune donnée n'est trouvée

    def candidats_repechables(self):
        """
        Retourne le nombre de candidats repêchables selon les règles métiers.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) 
            FROM Notes n
            JOIN Livret_Scolaire l ON n.Numero_Table = l.Numero_Table
            WHERE (n.Points BETWEEN 144 AND 179.9 AND l.Moyenne_Cycle >= 12)
            OR (n.Points BETWEEN 171 AND 179.9)
            OR (n.Points BETWEEN 144 AND 152.9 AND l.Nombre_de_fois <= 2)
        ''')
        result = cursor.fetchone()[0]
        conn.close()
        return result

    def candidats_admis(self):
        """
        Retourne le nombre de candidats admis (points >= 180).
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM Notes WHERE Points >= 180')
        result = cursor.fetchone()[0]
        conn.close()
        return result

    def candidats_second_tour(self):
        """
        Retourne le nombre de candidats admis au second tour (points entre 153 et 179.9).
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM Notes WHERE Points BETWEEN 153 AND 179.9')
        result = cursor.fetchone()[0]
        conn.close()
        return result

    def candidats_echoues(self):
        """
        Retourne le nombre de candidats échoués (points < 153).
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM Notes WHERE Points < 153')
        result = cursor.fetchone()[0]
        conn.close()
        return result