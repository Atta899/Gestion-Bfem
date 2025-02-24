import sqlite3

class GestionSecondTour:
    def __init__(self, db_path="bfem.db"):
        self.db_path = db_path

    def saisir_notes_repechage_second_tour(self, anonymat, francais, math, pc_lv2):
        """
        Saisit les notes du second tour pour un candidat repêchable.
        Les coefficients sont fixés : Français (3), Mathématiques (3), PC/LV2 (2).
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()

                # Récupérer le numéro de table correspondant à l'anonymat
                cur.execute("SELECT numero_table FROM anonymats WHERE anonymat = ?", (anonymat,))
                result = cur.fetchone()
                if not result:
                    return False, "Anonymat non trouvé."

                numero_table = result[0]

                # Vérifier si le candidat est repêchable
                cur.execute("""
                       SELECT n.Points, l.Nombre_de_fois
                       FROM Notes n
                       JOIN Livret_Scolaire l ON n.Numero_Table = l.Numero_Table
                       WHERE n.Numero_Table = ? AND n.Points BETWEEN 76 AND 79.9 AND l.Nombre_de_fois <= 2
                   """, (numero_table,))
                candidat_repechable = cur.fetchone()
                if not candidat_repechable:
                    return False, "Le candidat n'est pas repêchable pour le second tour."

                # Récupérer les points du premier tour
                cur.execute("SELECT Points FROM Notes WHERE Numero_Table = ?", (numero_table,))
                points_premier_tour = cur.fetchone()[0]

                # Calculer les points du second tour
                points_second_tour = (francais * 3) + (math * 3) + (pc_lv2 * 2)

                # Calculer les points totaux
                points_totaux = points_premier_tour + points_second_tour

                # Enregistrer les notes du second tour
                cur.execute("""
                       INSERT INTO SecondTour (Numero_Table, Francais, Math, PC_LV2, Points_Second_Tour, Points_Totaux)
                       VALUES (?, ?, ?, ?, ?, ?)
                   """, (numero_table, francais, math, pc_lv2, points_second_tour, points_totaux))

                conn.commit()
                return True, "Notes du second tour enregistrées avec succès pour le candidat repêchable."

        except sqlite3.Error as e:
            return False, f"Erreur SQL : {e}"

    def saisir_notes_second_tour(self, anonymat, francais, math, pc_lv2):
        """
        Saisit les notes du second tour pour un candidat en fonction de son anonymat.
        Les coefficients sont fixés : Français (3), Mathématiques (3), PC/LV2 (2).
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                # Récupérer le numéro de table correspondant à l'anonymat
                cur.execute("SELECT numero_table FROM anonymats WHERE anonymat = ?", (anonymat,))
                result = cur.fetchone()
                if not result:
                    print(f"Erreur : Anonymat {anonymat} non trouvé.")
                    return False, "Anonymat non trouvé."

                numero_table = result[0]
                print(f"Numéro de table trouvé : {numero_table}")

                # Récupérer les points du premier tour
                cur.execute("SELECT Points FROM Notes WHERE Numero_Table = ?", (numero_table,))
                points_premier_tour = cur.fetchone()[0]
                print(f"Points du premier tour : {points_premier_tour}")

                # Calculer les points du second tour
                points_second_tour = (francais * 3) + (math * 3) + (pc_lv2 * 2)
                print(f"Points du second tour : {points_second_tour}")

                # Calculer les points totaux
                points_totaux = points_premier_tour + points_second_tour
                print(f"Points totaux : {points_totaux}")

                # Enregistrer les notes du second tour
                cur.execute("""
                    INSERT INTO SecondTour (Numero_Table, Francais, Math, PC_LV2, Points_Second_Tour, Points_Totaux)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (numero_table, francais, math, pc_lv2, points_second_tour, points_totaux))

                conn.commit()
                print("Notes du second tour enregistrées avec succès.")
                return True, "Notes du second tour enregistrées avec succès."

        except sqlite3.Error as e:
            print(f"Erreur SQL : {e}")
            return False, f"Erreur SQL : {e}"

    def deliberer_second_tour(self):
        """
        Délibère les candidats après le second tour et détermine s'ils sont admis, repêchables ou échoués.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()

                # Vérifier si la colonne Resultat existe dans la table Notes
                cur.execute("PRAGMA table_info(Notes)")
                columns = cur.fetchall()
                column_names = [column[1] for column in columns]
                if "Resultat" not in column_names:
                    # Ajouter la colonne Resultat si elle n'existe pas
                    cur.execute("ALTER TABLE Notes ADD COLUMN Resultat TEXT")
                    conn.commit()

                # Récupérer tous les candidats ayant passé le second tour
                cur.execute("""
                      SELECT s.Numero_Table, s.Points_Totaux, c.Prenom_s, c.Nom
                      FROM SecondTour s
                      JOIN Candidat c ON s.Numero_Table = c.Numero_Table
                  """)
                candidats_second_tour = cur.fetchall()

                for candidat in candidats_second_tour:
                    numero_table, points_totaux, prenom, nom = candidat

                    # Délibération
                    if points_totaux >= 180:
                        resultat = "Admis"
                    elif points_totaux >= 153:
                        resultat = "Second Tour"
                    else:
                        resultat = "Échec"

                    # Mettre à jour le résultat dans la base de données
                    cur.execute("""
                          UPDATE Notes
                          SET Resultat = ?
                          WHERE Numero_Table = ?
                      """, (resultat, numero_table))

                conn.commit()
                return True, "Délibération du second tour terminée avec succès."

        except sqlite3.Error as e:
            return False, f"Erreur SQL : {e}"