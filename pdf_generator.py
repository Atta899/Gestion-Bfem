from fpdf import FPDF


class PDFPage:
    def __init__(self):
        self.pdf = FPDF()

    def generer_liste_candidats(self, candidats):
        """
        Génère un PDF contenant la liste des candidats.
        :param candidats: Liste des candidats sous forme de tuples (Numéro_Table, Prénom, Nom).
        """
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(200, 10, txt="Liste des Candidats", ln=True, align="C")

        # Ajouter chaque candidat dans le PDF
        for candidat in candidats:
            self.pdf.cell(200, 10, txt=f"{candidat[1]} {candidat[2]} - Table {candidat[0]}", ln=True)

        # Enregistrer le fichier PDF
        self.pdf.output("liste_candidats.pdf")
        print("Liste des candidats générée avec succès : liste_candidats.pdf")

    def generer_pv_deliberation(self, pv):
        """
        Génère un PDF contenant le procès-verbal de délibération.
        :param pv: Texte du procès-verbal.
        """
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(200, 10, txt="Procès-Verbal de Délibération", ln=True, align="C")

        # Ajouter le texte du procès-verbal
        self.pdf.multi_cell(0, 10, txt=pv)

        # Enregistrer le fichier PDF
        self.pdf.output("pv_deliberation.pdf")
        print("Procès-verbal de délibération généré avec succès : pv_deliberation.pdf")

    def generer_releve_notes(self, candidat_info, notes):
        """
        Génère un PDF contenant le relevé de notes d'un candidat.
        :param candidat_info: Dictionnaire contenant les informations du candidat (Numéro_Table, Nom, Prénom).
        :param notes: Dictionnaire contenant les notes du candidat (matière: note).
        """
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(200, 10, txt="Relevé de Notes", ln=True, align="C")

        # Ajouter les informations du candidat
        self.pdf.cell(200, 10, txt=f"Candidat: {candidat_info['Nom']} {candidat_info['Prénom']}", ln=True)
        self.pdf.cell(200, 10, txt=f"Numéro de Table: {candidat_info['Numéro Table']}", ln=True)

        # Ajouter les notes
        self.pdf.cell(200, 10, txt="Notes :", ln=True)
        for matiere, note in notes.items():
            self.pdf.cell(200, 10, txt=f"{matiere}: {note}", ln=True)

        # Enregistrer le fichier PDF
        fichier_pdf = f"releve_notes_{candidat_info['Numéro Table']}.pdf"
        self.pdf.output(fichier_pdf)
        print(f"Relevé de notes généré avec succès : {fichier_pdf}")