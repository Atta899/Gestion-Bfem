import sqlite3
import random

class GenerateurAnonymat:
    def __init__(self, db_path="bfem.db"):
        self.db_path = db_path
        self.creer_table()

    def creer_table(self):
        """Crée la table des anonymats si elle n'existe pas."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS anonymats (
                    numero_table TEXT PRIMARY KEY,
                    anonymat TEXT UNIQUE,
                    FOREIGN KEY (numero_table) REFERENCES Candidat (numero_table)
                )
            """)
            conn.commit()

    def generer_anonymat(self):
        """Génère un numéro d'anonymat unique."""
        essais = 0
        while essais < 10:  # Limite le nombre d'essais pour éviter une boucle infinie
            anonymat = f"ANON-{random.randint(1000, 9999)}"
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("SELECT 1 FROM anonymats WHERE anonymat = ?", (anonymat,))
                if not cur.fetchone():
                    return anonymat
            essais += 1
        raise Exception("Impossible de générer un anonymat unique après plusieurs essais.")

    def attribuer_anonymat(self, numero_table):
        """Attribue un anonymat à un candidat spécifique."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            # Vérifie si le candidat existe déjà dans la table des anonymats
            cur.execute("SELECT 1 FROM anonymats WHERE numero_table = ?", (numero_table,))
            if cur.fetchone():
                return None  # Le candidat a déjà un anonymat

            # Génère un nouvel anonymat
            anonymat = self.generer_anonymat()
            cur.execute("INSERT INTO anonymats (numero_table, anonymat) VALUES (?, ?)", (numero_table, anonymat))
            conn.commit()
            return anonymat

    def recuperer_anonymat(self, numero_table):
        """Récupère l'anonymat d'un candidat spécifique."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT anonymat FROM anonymats WHERE numero_table = ?", (numero_table,))
            result = cur.fetchone()
            return result[0] if result else None

    def attribuer_anonymats_tous(self):
        """Attribue un anonymat à tous les candidats sans anonymat et retourne la liste des anonymats générés."""
        anonymats_generes = []
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            # Récupère tous les candidats sans anonymat
            cur.execute(
                "SELECT numero_table FROM Candidat WHERE numero_table NOT IN (SELECT numero_table FROM anonymats)")
            candidats_sans_anonymat = cur.fetchall()

            # Attribue un anonymat à chaque candidat
            for (numero_table,) in candidats_sans_anonymat:
                anonymat = self.generer_anonymat()
                try:
                    cur.execute("INSERT INTO anonymats (numero_table, anonymat) VALUES (?, ?)",
                                (numero_table, anonymat))
                    anonymats_generes.append((numero_table, anonymat))
                except sqlite3.IntegrityError:
                    print(f"Erreur : L'anonymat {anonymat} existe déjà. Génération d'un nouvel anonymat.")
                    continue  # Passe au candidat suivant
            conn.commit()
        return anonymats_generes

    def lister_anonymats(self):
        """Retourne la liste de tous les anonymats."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM anonymats")
            return cur.fetchall()