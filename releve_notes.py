import sqlite3

# releve_notes.py
class Releve_Notes:
    def __init__(self, db_name="bfem.db"):
        self.db_name = db_name

    def generer_releve_notes(self, numero_table):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Récupérer les informations du candidat
        cursor.execute('''
            SELECT c.numero_table, c.prenom, c.nom, n.compo_franc, n.dictee, n.etude_de_texte, 
                n.instruction_civique, n.histoire_geographie, n.mathematiques, n.pc_lv2, 
                n.svt, n.anglais1, n.anglais_oral, n.eps
            FROM Candidat c
            JOIN Notes n ON c.numero_table = n.numero_table
            WHERE c.numero_table = ?
        ''', (numero_table,))

        candidat = cursor.fetchone()
        conn.close()

        if not candidat:
            raise Exception("Candidat introuvable")

        # Création du PDF
        fichier_pdf = f"Releve_Notes_{candidat[0]}.pdf"
        c = canvas.Canvas(fichier_pdf, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, f"Relevé de Notes - BFEM")
        c.drawString(100, 730, f"Numéro de Table : {candidat[0]}")
        c.drawString(100, 710, f"Nom : {candidat[2]}")
        c.drawString(100, 690, f"Prénom : {candidat[1]}")
        c.drawString(100, 670, "Notes :")

        lignes = [
            f"Composition Française : {candidat[3]}",
            f"Dictée : {candidat[4]}",
            f"Étude de Texte : {candidat[5]}",
            f"Instruction Civique : {candidat[6]}",
            f"Histoire-Géographie : {candidat[7]}",
            f"Mathématiques : {candidat[8]}",
            f"PC/LV2 : {candidat[9]}",
            f"Sciences Naturelles : {candidat[10]}",
            f"Anglais Écrit : {candidat[11]}",
            f"Anglais Oral : {candidat[12]}",
            f"EPS : {candidat[13]}"
        ]

        y = 650
        for ligne in lignes:
            c.drawString(120, y, ligne)
            y -= 20

        c.save()
        print(f"Relevé de notes généré : {fichier_pdf}")