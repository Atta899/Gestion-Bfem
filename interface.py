import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from tkinter.font import Font
from database import create_database
from candidat import Candidat
from jury import Jury
from deliberation import Deliberation, DeliberationPage
from statistiques import Statistiques
from releve_notes import Releve_Notes
from repechage import Repechage
from pdf_generator import PDFPage
from anonymat import GenerateurAnonymat
import os
import platform
import matplotlib
matplotlib.use('TkAgg')  # Utilisez le backend TkAgg pour matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gestionsecondtour import GestionSecondTour



# Configuration des styles
def configure_styles():
    style = ttk.Style()
    style.configure("Blue.TButton", font=("Helvetica", 12, "bold"),
                    background="#007BFF", foreground="white",
                    borderwidth=0, focusthickness=3, focuscolor="#007BFF",
                    padding=10, relief="flat")
    style.map("Blue.TButton", background=[("active", "#0056b3")])
    style.configure("Blue.TEntry", font=("Helvetica", 12), borderwidth=2,
                    relief="flat", padding=5, fieldbackground="#ffffff",
                    foreground="#333333")

# Configuration des styles
configure_styles()

class BasePage(tk.Frame):
    def __init__(self, parent, controller, title):
        super().__init__(parent)
        self.controller = controller
        self.title = title
        self.configure(bg="#ffffff")
        tk.Frame.__init__(self, parent, bg="#ffffff")  # Fond blanc
        self.controller = controller

        # En-tête de la page
        self.header = tk.Frame(self, bg="#007BFF", height=80)  # Fond bleu
        self.header.pack(fill="x")

        self.title_label = tk.Label(self.header, text=title, font=controller.title_font,
                                    bg="#007BFF", fg="white")  # Texte blanc
        self.title_label.pack(pady=20)

        # Boutons de navigation
        self.back_button = ttk.Button(self.header, text="← Retour",
                                      command=lambda: controller.show_frame("HomePage"),
                                      style="Blue.TButton")
        self.back_button.pack(side="left", padx=20)

        # Bouton de déconnexion
        self.logout_button = ttk.Button(self.header, text="Déconnexion",
                                        command=lambda: controller.show_frame("LoginPage"),
                                        style="Blue.TButton")
        self.logout_button.pack(side="right", padx=20)



class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion BFEM")
        self.root.geometry("1200x800")
        self.root.configure(bg="#ffffff")  # Fond blanc

        # Création de la base de données
        create_database()

        # Initialisation des gestionnaires
        self.candidat = Candidat()
        self.jury = Jury()
        self.deliberation = Deliberation()
        self.anonymat = GenerateurAnonymat()
        self.repechage = Repechage()
        self.gestionsecondtour = GestionSecondTour()
        # Configuration des polices
        self.title_font = Font(family="Helvetica", size=28, weight="bold")
        self.button_font = Font(family="Helvetica", size=14, weight="bold")
        self.label_font = Font(family="Helvetica", size=12)
        self.entry_font = Font(family="Helvetica", size=12)

        # Gestion des pages
        self.frames = {}
        self._initialiser_pages()

        # Affichage de la page de connexion par défaut
        self.show_frame("LoginPage")

        # Configuration du redimensionnement
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def _initialiser_pages(self):
        # Liste des pages Tkinter (avec ReleveNotesPage)
        for F in (
                LoginPage, HomePage, AddCandidatPage, EditCandidatPage, DeleteCandidatPage, ListCandidatPage, JuryPage,
                DeliberationPage, AnonymatPage, RepechagePage, ReleveNotesPage, StatistiquesPage, PDFPageUI,
                GestionSecondTourPage
        ):
            page_name = F.__name__
            frame = F(parent=self.root, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
    def logout(self):
        # Exemple : Fermer l'application ou rediriger vers la page de connexion
        print("Déconnexion en cours...")
        self.root.destroy()  # Ferme l'application
        # Ou rediriger vers une page de connexion :
        # self.show_frame("LoginPage")


    def show_frame(self, page_name):
        """Affichage d'une page spécifique"""
        frame = self.frames[page_name]
        frame.tkraise()

    def run(self):
        """Démarrage de l'application"""
        self.root.mainloop()



class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f0f2f5")  # Fond léger et moderne
        self.controller = controller

        # Configuration des styles
        self.configure_styles()

        # Titre de la page
        self.title_label = tk.Label(self, text="Connexion", font=("Helvetica", 24, "bold"),
                                    bg="#f0f2f5", fg="#007BFF")  # Texte bleu
        self.title_label.pack(pady=(50, 20))

        # Formulaire de connexion
        self.form_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="groove",
                                   padx=20, pady=20)
        self.form_frame.pack(pady=20, padx=50, fill="both", expand=True)

        # Icône ou illustration (optionnel)
        self.icon_label = tk.Label(self.form_frame, text="🔒", font=("Helvetica", 48),
                                   bg="#ffffff", fg="#007BFF")
        self.icon_label.pack(pady=(0, 20))

        # Champ Nom d'utilisateur
        tk.Label(self.form_frame, text="Nom d'utilisateur", bg="#ffffff", fg="#333333",
                 font=("Helvetica", 12)).pack(pady=5)
        self.username_entry = ttk.Entry(self.form_frame, font=("Helvetica", 12),
                                        style="Rounded.TEntry")
        self.username_entry.pack(pady=5, fill="x", ipady=8)

        # Champ Mot de passe
        tk.Label(self.form_frame, text="Mot de passe", bg="#ffffff", fg="#333333",
                 font=("Helvetica", 12)).pack(pady=5)
        self.password_entry = ttk.Entry(self.form_frame, font=("Helvetica", 12),
                                        style="Rounded.TEntry", show="*")
        self.password_entry.pack(pady=5, fill="x", ipady=8)

        # Bouton de connexion
        login_button = ttk.Button(self.form_frame, text="Se connecter",
                                  command=self.validate_login, style="Accent.TButton")
        login_button.pack(pady=20, fill="x", ipady=10)

        # Lien "Mot de passe oublié" (optionnel)
        forgot_password_label = tk.Label(self.form_frame, text="Mot de passe oublié ?",
                                         bg="#ffffff", fg="#007BFF", font=("Helvetica", 10, "underline"),
                                         cursor="hand2")
        forgot_password_label.pack(pady=10)
        forgot_password_label.bind("<Button-1>", lambda e: self.forgot_password())

    def configure_styles(self):
        """Configure les styles pour les widgets"""
        style = ttk.Style()
        style.configure("Rounded.TEntry", borderwidth=0, relief="flat",
                         background="#f0f2f5", padding=10, bordercolor="#007BFF",
                         focuscolor="#007BFF", lightcolor="#007BFF", darkcolor="#007BFF")
        style.map("Rounded.TEntry",
                  bordercolor=[("focus", "#007BFF"), ("!focus", "#cccccc")],
                  lightcolor=[("focus", "#007BFF"), ("!focus", "#cccccc")],
                  darkcolor=[("focus", "#007BFF"), ("!focus", "#cccccc")])

        style.configure("Accent.TButton", background="#007BFF", foreground="white",
                        font=("Helvetica", 12, "bold"), borderwidth=0, padding=10)
        style.map("Accent.TButton",
                  background=[("active", "#0056b3"), ("!active", "#007BFF")],
                  foreground=[("active", "white"), ("!active", "white")])

    def validate_login(self):
        """Validation des informations de connexion"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        # Validation des credentials
        if username == "admin" and password == "admin":
            self.controller.show_frame("HomePage")
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    def forgot_password(self):
        """Gestion du mot de passe oublié"""
        messagebox.showinfo("Mot de passe oublié", "Un lien de réinitialisation a été envoyé à votre adresse e-mail.")

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")  # Fond blanc pour la page

        # Configuration des frames principaux
        self.sidebar = tk.Frame(self, bg="white")  # Sidebar en blanc
        self.sidebar.pack(side="left", fill="y", padx=5)

        self.main_content = tk.Frame(self, bg="white")  # Contenu principal en blanc
        self.main_content.pack(side="right", fill="both", expand=True, padx=5)

        # Configuration de la sidebar
        self._configurer_sidebar()

        # Configuration du contenu principal
        self._configurer_contenu_principal()

        # Ajout des cartes dans le contenu principal
        self._ajouter_cartes()

    def _configurer_sidebar(self):
        # Logo et titre
        logo_frame = tk.Frame(self.sidebar, bg="white")  # Fond blanc
        logo_frame.pack(fill="x", pady=10)

        tk.Label(logo_frame, text="BFEM", font=("Helvetica", 20, "bold"),
                bg="white", fg="#007BFF").pack(pady=10)  # Texte en bleu

        # Séparateur
        separator = tk.Frame(self.sidebar, bg="#007BFF", height=2)  # Séparateur bleu
        separator.pack(fill="x", padx=10, pady=10)

        # Menu de navigation
        menu_items = [
            ("Accueil", "HomePage"),
            ("Candidats", "ListCandidatPage"),
            ("Jury", "JuryPage"),
            ("Délibération", "DeliberationPage"),
            ("Statistiques", "StatistiquesPage")
        ]

        for text, page in menu_items:
            btn = ttk.Button(self.sidebar, text=text, style="Blue.TButton",
                           command=lambda p=page: self.controller.show_frame(p))
            btn.pack(fill="x", padx=10, pady=5)

        # Boutons "Retour" et "Déconnexion" à droite
        button_frame = tk.Frame(self.sidebar, bg="white")  # Fond blanc
        button_frame.pack(side="bottom", fill="x", pady=10)

        retour_btn = ttk.Button(button_frame, text="Retour", style="Green.TButton",
                              command=lambda: self.controller.show_frame("PreviousPage"))
        retour_btn.pack(side="right", padx=5, pady=5)

        deconnexion_btn = ttk.Button(button_frame, text="Déconnexion", style="Green.TButton",
                                   command=self.controller.logout)
        deconnexion_btn.pack(side="right", padx=5, pady=5)

    def _configurer_contenu_principal(self):
        # En-tête du contenu principal
        header = tk.Frame(self.main_content, bg="white")  # Fond blanc
        header.pack(fill="x")

        tk.Label(header, text="Acceuil", font=("Helvetica", 18, "bold"),
                bg="white", fg="#007BFF").pack(pady=20)  # Texte en bleu

        # Contenu principal avec scroll
        self.content_frame = tk.Frame(self.main_content, bg="white")  # Fond blanc
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Configuration du scroll
        self.canvas = tk.Canvas(self.content_frame, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical",
                                     command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _ajouter_cartes(self):
        cards = [
            ("Ajouter Candidat", "AddCandidatPage"),
            ("Modifier Candidat", "EditCandidatPage"),
            ("Supprimer Candidat", "DeleteCandidatPage"),
            ("Liste des Candidats", "ListCandidatPage"),
            ("Paramétre Jury", "JuryPage"),
            ("Délibération", "DeliberationPage"),
            ("Générer Anonymats", "AnonymatPage"),
            ("Gestion Repêchages", "RepechagePage"),
            ("Relevés de Notes", "ReleveNotesPage"),
            ("Statistiques", "StatistiquesPage"),
            ("Impression en PDF", "PDFPageUI"),
            ("Gestion du Second Tour","GestionSecondTourPage")
        ]

        for i, (text, page) in enumerate(cards):
            card = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid",
                          padx=40, pady=40)
            card.grid(row=i // 3, column=i % 3, padx=20, pady=20, sticky="nsew")

            label = tk.Label(card, text=text, font=self.controller.button_font,
                           bg="white", fg="#007BFF")  # Texte en bleu
            label.pack(pady=20)

            # Gestion des événements
            card.bind("<Button-1>", lambda e, p=page:
                     self.controller.show_frame(p))
            label.bind("<Button-1>", lambda e, p=page:
                      self.controller.show_frame(p))

            # Effet de survol vert
            card.bind("<Enter>", lambda e, c=card: c.configure(bg="#e0f7e0"))  # Vert clair
            card.bind("<Leave>", lambda e, c=card: c.configure(bg="white"))
            label.bind("<Enter>", lambda e, c=card: c.configure(bg="#e0f7e0"))
            label.bind("<Leave>", lambda e, c=card: c.configure(bg="white"))

    # Configuration des styles
    style = ttk.Style()
    style.configure("Blue.TButton", background="#007BFF", foreground="white",
                    font=("Helvetica", 12, "bold"))
    style.configure("Green.TButton", background="#4CAF50", foreground="white",
                    font=("Helvetica", 12, "bold"))


class AddCandidatPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Ajouter un Candidat")

        container = tk.Frame(self, bg="#ffffff")
        container.pack(pady=20, padx=50, fill="both", expand=True)

        # Ajout d'un canvas et d'une barre de défilement
        canvas = tk.Canvas(container, bg="#ffffff")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.form_frame = tk.Frame(canvas, bg="#ffffff")

        self.form_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Champs du formulaire
        self.fields = ["Numéro Table", "Prénom", "Nom", "Date Naissance",
                       "Lieu Naissance", "Sexe", "Nationalité",
                       "Choix Épreuve Facultative", "Épreuve Facultative",
                       "Aptitude Sportive"]
        self.entries = {}

        for field in self.fields:
            row = tk.Frame(self.form_frame, bg="#ffffff")
            row.pack(pady=5, fill="x")
            tk.Label(row, text=field, bg="#ffffff", fg="#333",
                     font=("Arial", 12, "bold")).pack(side="left", padx=10)
            entry = ttk.Entry(row, font=("Arial", 12))
            entry.pack(side="right", padx=10, fill="x", expand=True)
            self.entries[field] = entry

        # Bouton d'ajout
        submit_button = ttk.Button(self, text="Ajouter", command=self.add_candidat, style="Blue.TButton")
        submit_button.pack(pady=20)

    def add_candidat(self):
        valeurs = {champ: self.entries[champ].get() for champ in self.entries}

        if not all(valeurs.values()):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        try:
            self.controller.candidat.ajouter_candidat(**valeurs)
            messagebox.showinfo("Succès", "Candidat ajouté avec succès")
            self._vider_formulaire()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")

    def _vider_formulaire(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)


class EditCandidatPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Modifier un Candidat")

        container = tk.Frame(self, bg="#ffffff")
        container.pack(pady=20, padx=50, fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#ffffff")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.form_frame = tk.Frame(canvas, bg="#ffffff")

        self.form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(self.form_frame, text="Sélectionner un candidat:",
                 bg="#ffffff", fg="#333", font=("Arial", 12, "bold")).pack(pady=10)

        self.candidat_var = tk.StringVar()
        self.candidat_combo = ttk.Combobox(self.form_frame, textvariable=self.candidat_var, state='readonly')
        self.candidat_combo.pack(pady=10, fill="x")

        ttk.Button(self.form_frame, text="Charger les informations",
                   command=self.charger_informations, style="Blue.TButton").pack(pady=10)

        self.fields = ["Numéro Table", "Prénom", "Nom", "Date Naissance",
                       "Lieu Naissance", "Sexe", "Nationalité",
                       "Choix Épreuve Facultative", "Épreuve Facultative",
                       "Aptitude Sportive"]
        self.entries = {}

        for field in self.fields:
            row = tk.Frame(self.form_frame, bg="#ffffff")
            row.pack(pady=5, fill="x")
            tk.Label(row, text=field, bg="#ffffff", fg="#333",
                     font=("Arial", 12, "bold")).pack(side="left", padx=10)
            entry = ttk.Entry(row, font=("Arial", 12))
            entry.pack(side="right", padx=10, fill="x", expand=True)
            self.entries[field] = entry

        submit_button = ttk.Button(self, text="Modifier", command=self.modifier_candidat, style="Blue.TButton")
        submit_button.pack(pady=20)

        self.mettre_a_jour_liste_candidats()

    def mettre_a_jour_liste_candidats(self):
        self.candidat_combo['values'] = [c[0] for c in self.controller.candidat.lister_candidats()]

    def charger_informations(self):
        numero_table = self.candidat_var.get()
        if numero_table:
            candidat = self.controller.candidat.lister_candidats(numero_table)
            if candidat:
                for champ, valeur in zip(self.fields, candidat):
                    self.entries[champ].delete(0, tk.END)
                    self.entries[champ].insert(0, valeur)

    def modifier_candidat(self):
        numero_table = self.candidat_var.get()
        if not numero_table:
            messagebox.showerror("Erreur", "Veuillez sélectionner un candidat")
            return

        valeurs = {champ: self.entries[champ].get() for champ in self.fields}
        if not all(valeurs.values()):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        try:
            self.controller.candidat.modifier_candidat(numero_table, **valeurs)
            messagebox.showinfo("Succès", "Candidat modifié avec succès")
            self.mettre_a_jour_liste_candidats()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")


class DeleteCandidatPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Supprimer un Candidat")

        self.frame_principal = tk.Frame(self, bg="#f0f2f5")
        self.frame_principal.pack(pady=20, padx=50, fill="both", expand=True)

        # Liste des candidats
        self.liste_candidats = tk.Listbox(self.frame_principal, width=60, height=10)
        self.liste_candidats.pack(pady=10, padx=10)

        # Boutons
        bouton_frame = tk.Frame(self.frame_principal, bg="#f0f2f5")
        bouton_frame.pack(pady=10)

        ttk.Button(bouton_frame, text="Actualiser",
                   command=self.actualiser_liste, style="Blue.TButton").pack(side="left", padx=5)
        ttk.Button(bouton_frame, text="Supprimer",
                   command=self.supprimer_candidat, style="Blue.TButton").pack(side="left", padx=5)

        self.actualiser_liste()

    def actualiser_liste(self):
        """Actualisation de la liste des candidats"""
        self.liste_candidats.delete(0, tk.END)
        for candidat in self.controller.candidat.lister_candidats():
            self.liste_candidats.insert(tk.END, f"{candidat[0]} - {candidat[1]} {candidat[2]}")

    def supprimer_candidat(self):
        """Suppression d'un candidat"""
        selection = self.liste_candidats.curselection()
        if not selection:
            messagebox.showerror("Erreur", "Veuillez sélectionner un candidat à supprimer")
            return

        numero_table = self.liste_candidats.get(selection[0]).split('-')[0].strip()
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce candidat?"):
            try:
                self.controller.candidat.supprimer_candidat(numero_table)
                self.actualiser_liste()
                messagebox.showinfo("Succès", "Candidat supprimé avec succès")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")

class ListCandidatPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Liste des Candidats")

        # Configuration du Treeview
        self.tree = ttk.Treeview(self, columns=("Numero_Table", "Nom", "Prenom_s",
                                                "Date_Naissance", "Lieu_Naissance",
                                                "Sexe", "Nationalite"), show="headings")

        # Configuration des en-têtes
        for col in ("Numero_Table", "Nom", "Prenom_s", "Date_Naissance",
                    "Lieu_Naissance", "Sexe", "Nationalite"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Bouton de rafraîchissement
        ttk.Button(self, text="Rafraîchir",
                   command=self.rafraichir_liste, style="Blue.TButton").pack(pady=10)

        self.rafraichir_liste()

    def rafraichir_liste(self):
        """Rafraîchissement de la liste des candidats"""
        # Effacement des données existantes
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Ajout des nouveaux candidats
        for candidat in self.controller.candidat.lister_candidats():
            self.tree.insert("", "end", values=candidat[:7])


class JuryPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Parametren jury")
        tk.Frame.__init__(self, parent, bg="#f0f2f5")  # Fond léger et moderne
        self.controller = controller

        # Titre de la page
        self.title_label = tk.Label(self, text="Paramétrer le Jury", font=("Helvetica", 24, "bold"),
                                    bg="#f0f2f5", fg="#007BFF")  # Texte bleu
        self.title_label.pack(pady=(20, 10))

        # Cadre principal
        self.main_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="groove",
                                   padx=20, pady=20)
        self.main_frame.pack(pady=20, padx=50, fill="both", expand=True)

        # Formulaire
        self.form_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.form_frame.pack(pady=20, fill="x")

        # Champs du formulaire
        fields = ["Région", "Département", "Localité", "Centre d'Examen", "Président de Jury", "Téléphone"]
        self.entries = {}

        for field in fields:
            row = tk.Frame(self.form_frame, bg="#ffffff")
            row.pack(pady=10, fill="x")

            # Label du champ
            tk.Label(row, text=field, bg="#ffffff", fg="#333333",
                     font=("Helvetica", 12)).pack(side="left", padx=10)

            # Champ de saisie
            entry = ttk.Entry(row, font=("Helvetica", 12), style="Rounded.TEntry")
            entry.pack(side="right", padx=10, fill="x", expand=True, ipady=5)
            self.entries[field] = entry

        # Bouton de sauvegarde
        save_button = ttk.Button(self.main_frame, text="Sauvegarder",
                                 command=self.sauvegarder_configuration, style="Accent.TButton")
        save_button.pack(pady=20, fill="x", ipady=10)

        # Boutons "Retour" et "Déconnexion"
        button_frame = tk.Frame(self.main_frame, bg="#ffffff")
        button_frame.pack(side="bottom", fill="x", pady=10)

        retour_btn = ttk.Button(button_frame, text="Retour", style="Green.TButton",
                              command=lambda: self.controller.show_frame("HomePage"))  # Retour à HomePage
        retour_btn.pack(side="left", padx=5, pady=5)

        deconnexion_btn = ttk.Button(button_frame, text="Déconnexion", style="Green.TButton",
                                   command=self.controller.logout)
        deconnexion_btn.pack(side="right", padx=5, pady=5)

    def sauvegarder_configuration(self):
        """Valide et sauvegarde la configuration du jury"""
        valeurs = {champ: self.entries[champ].get().strip() for champ in self.entries}

        # Validation des champs
        if not all(valeurs.values()):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            self.highlight_empty_fields()
            return

        try:
            # Enregistrement du jury
            self.controller.jury.enregistrer_jury(valeurs)
            messagebox.showinfo("Succès", "Configuration du jury sauvegardée avec succès !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {str(e)}")

    def highlight_empty_fields(self):
        """Met en évidence les champs vides"""
        for field, entry in self.entries.items():
            if not entry.get().strip():
                entry.configure(style="Error.TEntry")  # Style d'erreur
            else:
                entry.configure(style="Rounded.TEntry")  # Style normal

    def configure_styles(self):
        """Configure les styles pour les widgets"""
        style = ttk.Style()
        style.configure("Rounded.TEntry", borderwidth=0, relief="flat",
                         background="#f0f2f5", padding=10, bordercolor="#007BFF",
                         focuscolor="#007BFF", lightcolor="#007BFF", darkcolor="#007BFF")
        style.map("Rounded.TEntry",
                  bordercolor=[("focus", "#007BFF"), ("!focus", "#cccccc")],
                  lightcolor=[("focus", "#007BFF"), ("!focus", "#cccccc")],
                  darkcolor=[("focus", "#007BFF"), ("!focus", "#cccccc")])

        style.configure("Error.TEntry", bordercolor="#ff0000", lightcolor="#ff0000",
                         darkcolor="#ff0000")

        style.configure("Accent.TButton", background="#007BFF", foreground="white",
                        font=("Helvetica", 12, "bold"), borderwidth=0, padding=10)
        style.map("Accent.TButton",
                  background=[("active", "#0056b3"), ("!active", "#007BFF")],
                  foreground=[("active", "white"), ("!active", "white")])


class AnonymatPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Gérer les Anonymats")

        # Configuration des styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("Blue.TButton", background="#4CAF50", foreground="white", font=("Helvetica", 12, "bold"))
        self.style.configure("TEntry", font=("Helvetica", 12), padding=5)

        # Cadre principal
        self.main_frame = ttk.Frame(self, padding="20")
        self.main_frame.pack(fill="both", expand=True)

        # Titre de la page
        self.title_label = ttk.Label(self.main_frame, text="Gestion des Anonymats", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Champ pour le numéro de table
        self.numero_table_label = ttk.Label(self.main_frame, text="Numéro de Table :")
        self.numero_table_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.numero_table_entry = ttk.Entry(self.main_frame, width=30)
        self.numero_table_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Boutons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        self.attribuer_button = ttk.Button(self.button_frame, text="Attribuer Anonymat", command=self.attribuer_anonymat, style="Blue.TButton")
        self.attribuer_button.pack(side="left", padx=10)

        self.recuperer_button = ttk.Button(self.button_frame, text="Récupérer Anonymat", command=self.recuperer_anonymat, style="Blue.TButton")
        self.recuperer_button.pack(side="left", padx=10)

        self.attribuer_tous_button = ttk.Button(self.button_frame, text="Attribuer à Tous", command=self.attribuer_anonymats_tous, style="Blue.TButton")
        self.attribuer_tous_button.pack(side="left", padx=10)

        # Résultat
        self.result_label = ttk.Label(self.main_frame, text="", font=("Helvetica", 12))
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

        # Liste des anonymats générés
        self.liste_frame = ttk.Frame(self.main_frame)
        self.liste_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=10)

        self.liste_label = ttk.Label(self.liste_frame, text="Anonymats Générés :", font=("Helvetica", 12, "bold"))
        self.liste_label.pack(anchor="w", pady=(0, 10))

        self.liste_anonymats = tk.Listbox(self.liste_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12), height=10)
        self.liste_anonymats.pack(fill="both", expand=True)

        # Configurer la grille pour redimensionnement
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(4, weight=1)

    def attribuer_anonymat(self):
        numero_table = self.numero_table_entry.get().strip()

        if not numero_table:
            messagebox.showerror("Erreur", "Veuillez entrer un numéro de table.")
            return

        anonymat = self.controller.anonymat.attribuer_anonymat(numero_table)

        if anonymat:
            self.result_label.config(text=f"Anonymat attribué : {anonymat}", foreground="green")
            messagebox.showinfo("Succès", f"Anonymat attribué au candidat {numero_table} : {anonymat}")
        else:
            self.result_label.config(text=f"Erreur : Le candidat {numero_table} a déjà un anonymat.", foreground="red")
            messagebox.showerror("Erreur", f"Impossible d'attribuer un anonymat au candidat {numero_table}.")

    def recuperer_anonymat(self):
        numero_table = self.numero_table_entry.get().strip()

        if not numero_table:
            messagebox.showerror("Erreur", "Veuillez entrer un numéro de table.")
            return

        anonymat = self.controller.anonymat.recuperer_anonymat(numero_table)

        if anonymat:
            self.result_label.config(text=f"Anonymat du candidat {numero_table} : {anonymat}", foreground="green")
        else:
            self.result_label.config(text=f"Aucun anonymat trouvé pour le candidat {numero_table}.", foreground="red")
            messagebox.showerror("Erreur", f"Aucun anonymat trouvé pour le candidat {numero_table}.")

    def attribuer_anonymats_tous(self):
        """Attribue un anonymat à tous les candidats et affiche les résultats dans la liste."""
        anonymats_generes = self.controller.anonymat.attribuer_anonymats_tous()

        if anonymats_generes:
            self.liste_anonymats.delete(0, tk.END)  # Efface la liste actuelle
            for numero_table, anonymat in anonymats_generes:
                self.liste_anonymats.insert(tk.END, f"{numero_table} : {anonymat}")
            self.result_label.config(text=f"{len(anonymats_generes)} anonymats ont été attribués.", foreground="green")
            messagebox.showinfo("Succès", f"{len(anonymats_generes)} anonymats ont été attribués.")
        else:
            self.result_label.config(text="Aucun candidat sans anonymat trouvé.", foreground="blue")
            messagebox.showinfo("Info", "Aucun candidat sans anonymat trouvé.")


class RepechagePage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Gestion des Repêchages")

        # Configuration des styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("Blue.TButton", background="#4CAF50", foreground="white", font=("Helvetica", 12, "bold"))
        self.style.configure("Red.TButton", background="#FF5733", foreground="white", font=("Helvetica", 12, "bold"))
        self.style.configure("TEntry", font=("Helvetica", 12), padding=5)

        # Cadre principal
        self.frame_principal = ttk.Frame(self, padding="20")
        self.frame_principal.pack(fill="both", expand=True)

        # Titre de la page
        self.title_label = ttk.Label(self.frame_principal, text="Gestion des Repêchages", font=("Helvetica", 20, "bold"), background="#f0f0f0", foreground="#333333")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Bouton pour afficher les candidats repêchables (1er tour)
        self.btn_premier_tour = ttk.Button(self.frame_principal, text="Afficher Candidats Repêchables (1er Tour)",
                                          command=self.afficher_repechables_premier_tour, style="Blue.TButton")
        self.btn_premier_tour.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Bouton pour afficher les candidats repêchables (2nd tour)
        self.btn_second_tour = ttk.Button(self.frame_principal, text="Afficher Candidats Repêchables (2nd Tour)",
                                          command=self.afficher_repechables_second_tour, style="Blue.TButton")
        self.btn_second_tour.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Zone de texte pour afficher les résultats
        self.result_frame = ttk.Frame(self.frame_principal, style="TFrame")
        self.result_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)

        self.result_label = ttk.Label(self.result_frame, text="Résultats :", font=("Helvetica", 14, "bold"), background="#f0f0f0", foreground="#333333")
        self.result_label.pack(anchor="w", pady=(0, 10))

        self.result_text = tk.Text(self.result_frame, wrap=tk.WORD, height=10, width=80, font=("Helvetica", 12), bg="#ffffff", fg="#333333", bd=2, relief="groove")
        self.result_text.pack(fill="both", expand=True)

        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(self.result_text)
        scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)

        # Bouton pour effacer les résultats
        self.btn_effacer = ttk.Button(self.frame_principal, text="Effacer les Résultats", command=self.effacer_resultats, style="Red.TButton")
        self.btn_effacer.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        # Configurer la grille pour redimensionnement
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.columnconfigure(1, weight=1)
        self.frame_principal.rowconfigure(2, weight=1)

    def afficher_repechables_premier_tour(self):
        """Affiche les candidats repêchables pour le 1er tour"""
        repechage = Repechage()
        candidats = repechage.get_candidats_repechables()
        self.result_text.delete(1.0, tk.END)
        if candidats:
            self.result_text.insert(tk.END, "Candidats repêchables (1er tour):\n\n")
            for candidat in candidats:
                self.result_text.insert(tk.END, f"Numéro Table: {candidat[0]}\n")
                self.result_text.insert(tk.END, f"Prénom: {candidat[1]}\n")
                self.result_text.insert(tk.END, f"Nom: {candidat[2]}\n")
                self.result_text.insert(tk.END, f"Points: {candidat[3]}\n")
                self.result_text.insert(tk.END, f"Moyenne Cycle: {candidat[4]}\n")
                self.result_text.insert(tk.END, f"Nombre de fois: {candidat[5]}\n")
                self.result_text.insert(tk.END, "-" * 50 + "\n")
        else:
            self.result_text.insert(tk.END, "Aucun candidat repêchable pour le 1er tour.\n")


    def afficher_repechables_second_tour(self):
        """Affiche les candidats repêchables pour le 2nd tour."""
        repechage = Repechage()
        candidats = repechage.get_candidats_repechables_second_tour()
        self.result_text.delete(1.0, tk.END)
        if candidats:
            self.result_text.insert(tk.END, "Candidats repêchables (2nd tour):\n\n")
            for candidat in candidats:
                self.result_text.insert(tk.END, f"Numéro Table: {candidat[0]}\n")
                self.result_text.insert(tk.END, f"Prénom: {candidat[1]}\n")
                self.result_text.insert(tk.END, f"Nom: {candidat[2]}\n")
                self.result_text.insert(tk.END, f"Points: {candidat[3]}\n")
                self.result_text.insert(tk.END, f"Moyenne Cycle: {candidat[4]}\n")
                self.result_text.insert(tk.END, f"Nombre de fois: {candidat[5]}\n")
                self.result_text.insert(tk.END, "-" * 50 + "\n")
        else:
            self.result_text.insert(tk.END, "Aucun candidat repêchable pour le 2nd tour.\n")


    def effacer_resultats(self):
        """Efface le contenu de la zone de texte des résultats"""
        self.result_text.delete(1.0, tk.END)



class ReleveNotesPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Relevé de Notes")

        # Configuration des styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("Blue.TButton", background="#4CAF50", foreground="white", font=("Helvetica", 12, "bold"))
        self.style.configure("TEntry", font=("Helvetica", 12), padding=5)

        # Cadre principal
        self.frame_principal = ttk.Frame(self, padding="20")
        self.frame_principal.pack(fill="both", expand=True)

        # Titre de la page
        self.title_label = ttk.Label(self.frame_principal, text="Relevé de Notes", font=("Helvetica", 18, "bold"), background="#f0f0f0")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Champ pour entrer le numéro de table
        self.numero_table_label = ttk.Label(self.frame_principal, text="Numéro de Table :", background="#f0f0f0")
        self.numero_table_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.numero_table_entry = ttk.Entry(self.frame_principal, width=30)
        self.numero_table_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Bouton pour générer le relevé de notes
        self.btn_generer = ttk.Button(self.frame_principal, text="Générer Relevé de Notes",
                                      command=self.generer_releve_notes, style="Blue.TButton")
        self.btn_generer.grid(row=2, column=0, columnspan=2, pady=20, sticky="ew")

        # Zone de texte pour afficher les notes
        self.notes_frame = ttk.Frame(self.frame_principal, style="TFrame")
        self.notes_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)

        self.notes_label = ttk.Label(self.notes_frame, text="Relevé de Notes :", font=("Helvetica", 14, "bold"), background="#f0f0f0")
        self.notes_label.pack(anchor="w", pady=(0, 10))

        self.notes_text = tk.Text(self.notes_frame, wrap=tk.WORD, height=10, width=80, font=("Helvetica", 12), bg="#ffffff", fg="#333333", bd=2, relief="groove")
        self.notes_text.pack(fill="both", expand=True)

        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(self.notes_text)
        scrollbar.pack(side="right", fill="y")
        self.notes_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.notes_text.yview)

        # Configurer la grille pour redimensionnement
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.columnconfigure(1, weight=1)
        self.frame_principal.rowconfigure(3, weight=1)

    def generer_releve_notes(self):
        """
        Génère un relevé de notes pour un candidat.
        """
        numero_table = self.numero_table_entry.get().strip()
        if not numero_table:
            messagebox.showerror("Erreur", "Veuillez entrer un numéro de table.")
            return

        # Récupérer les notes du candidat depuis la base de données
        conn = sqlite3.connect('bfem.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.Numero_Table, c.Prenom_s, c.Nom, n.Compo_Franc, n.Dictee, n.Etude_de_texte, 
                   n.Instruction_Civique, n.Histoire_Geographie, n.Mathematiques, n.PC_LV2, 
                   n.SVT, n.Anglais1, n.Anglais_Oral, n.EPS, n.Epreuve_Facultative
            FROM Candidat c
            JOIN Notes n ON c.Numero_Table = n.Numero_Table
            WHERE c.Numero_Table = ?
        ''', (numero_table,))

        candidat = cursor.fetchone()
        conn.close()

        if not candidat:
            messagebox.showerror("Erreur", "Aucun candidat trouvé avec ce numéro de table.")
            return

        # Afficher les notes dans la zone de texte
        self.notes_text.delete(1.0, tk.END)
        self.notes_text.insert(tk.END, f"Relevé de Notes pour {candidat[2]} {candidat[1]} (Table {candidat[0]})\n\n")
        self.notes_text.insert(tk.END, f"Composition Française: {candidat[3]}\n")
        self.notes_text.insert(tk.END, f"Dictée: {candidat[4]}\n")
        self.notes_text.insert(tk.END, f"Étude de Texte: {candidat[5]}\n")
        self.notes_text.insert(tk.END, f"Instruction Civique: {candidat[6]}\n")
        self.notes_text.insert(tk.END, f"Histoire-Géographie: {candidat[7]}\n")
        self.notes_text.insert(tk.END, f"Mathématiques: {candidat[8]}\n")
        self.notes_text.insert(tk.END, f"PC/LV2: {candidat[9]}\n")
        self.notes_text.insert(tk.END, f"SVT: {candidat[10]}\n")
        self.notes_text.insert(tk.END, f"Anglais Écrit: {candidat[11]}\n")
        self.notes_text.insert(tk.END, f"Anglais Oral: {candidat[12]}\n")
        self.notes_text.insert(tk.END, f"EPS: {candidat[13]}\n")
        self.notes_text.insert(tk.END, f"Épreuve Facultative: {candidat[14]}\n")

        # Générer le PDF
        self.generer_pdf_releve_notes(candidat)

    def generer_pdf_releve_notes(self, candidat):
        """
        Génère un PDF avec le relevé de notes du candidat.
        """
        pdf = PDFPage()

        # Informations du candidat
        candidat_info = {
            "Numéro Table": candidat[0],
            "Nom": candidat[2],
            "Prénom": candidat[1]
        }

        # Notes du candidat
        notes = {
            "Composition Française": candidat[3],
            "Dictée": candidat[4],
            "Étude de Texte": candidat[5],
            "Instruction Civique": candidat[6],
            "Histoire-Géographie": candidat[7],
            "Mathématiques": candidat[8],
            "PC/LV2": candidat[9],
            "SVT": candidat[10],
            "Anglais Écrit": candidat[11],
            "Anglais Oral": candidat[12],
            "EPS": candidat[13],
            "Épreuve Facultative": candidat[14]
        }

        # Générer le PDF
        pdf.generer_releve_notes(candidat_info, notes)
        messagebox.showinfo("Succès", f"Relevé de notes généré pour le candidat {candidat_info['Nom']} {candidat_info['Prénom']}.")
class StatistiquesPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Statistiques")

        self.controller = controller
        self.configure(bg="#ffffff")

        # Création du conteneur principal
        self.frame_principal = tk.Frame(self, bg="#ffffff")
        self.frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

        # Cadre pour les boutons (colonne de gauche)
        self.frame_boutons = tk.Frame(self.frame_principal, bg="#ffffff")
        self.frame_boutons.pack(side="left", padx=20, fill="y")

        # Zone de texte avec barre de défilement
        self.text_frame = tk.Frame(self.frame_boutons, bg="#ffffff")
        self.text_frame.pack(pady=10, fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.statistiques_text = tk.Text(self.text_frame, wrap=tk.WORD, height=10, width=40,
                                         yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.statistiques_text.yview)

        self.statistiques_text.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Boutons à gauche
        ttk.Button(self.frame_boutons, text="Afficher Statistiques", command=self.afficher_statistiques,
                   style="Blue.TButton").pack(pady=5, fill="x")
        ttk.Button(self.frame_boutons, text="Exporter en PDF", command=self.exporter_en_pdf, style="Blue.TButton").pack(
            pady=5, fill="x")

        # Cadre pour le graphique (colonne de droite)
        self.frame_graph = tk.Frame(self.frame_principal, bg="#ffffff")
        self.frame_graph.pack(side="right", padx=20, fill="both", expand=True)

        # Barre de défilement pour le graphique
        self.canvas_frame = tk.Canvas(self.frame_graph, bg="#ffffff")
        self.scrollbar_graph = tk.Scrollbar(self.frame_graph, orient="vertical", command=self.canvas_frame.yview)
        self.graph_container = tk.Frame(self.canvas_frame, bg="#ffffff")

        self.canvas_frame.create_window((0, 0), window=self.graph_container, anchor="nw")
        self.canvas_frame.config(yscrollcommand=self.scrollbar_graph.set)

        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.scrollbar_graph.pack(side="right", fill="y")

    def afficher_statistiques(self):
        """
        Affiche les statistiques et génère un graphique circulaire.
        """
        stats = Statistiques()  # Classe à définir
        nombre_candidats = stats.nombre_candidats()
        moyenne_points = stats.moyenne_points()
        candidats_admis = stats.candidats_admis()
        candidats_second_tour = stats.candidats_second_tour()
        candidats_echoues = stats.candidats_echoues()
        candidats_repechables = stats.candidats_repechables()

        # Mise à jour de la zone de texte
        self.statistiques_text.delete(1.0, tk.END)
        self.statistiques_text.insert(tk.END, f"Nombre total de candidats : {nombre_candidats}\n")
        self.statistiques_text.insert(tk.END, f"Moyenne des points : {moyenne_points:.2f}\n")
        self.statistiques_text.insert(tk.END, f"Candidats admis : {candidats_admis}\n")
        self.statistiques_text.insert(tk.END, f"Candidats au second tour : {candidats_second_tour}\n")
        self.statistiques_text.insert(tk.END, f"Candidats échoués : {candidats_echoues}\n")
        self.statistiques_text.insert(tk.END, f"Candidats repêchables : {candidats_repechables}\n")

        # Générer le graphique
        self.afficher_graphiques(candidats_admis, candidats_second_tour, candidats_echoues, candidats_repechables)

    def afficher_graphiques(self, admis, second_tour, echoues, repechables):
        """
        Affiche un diagramme circulaire centré et plus grand.
        """
        for widget in self.graph_container.winfo_children():
            widget.destroy()

        labels = ['Admis', 'Second Tour', 'Échoués', 'Repêchables']
        valeurs = [admis, second_tour, echoues, repechables]
        couleurs = ['#2E8B57', '#FFD700', '#DC143C', '#1E90FF']  # Vert, Jaune, Rouge, Bleu

        fig, ax = plt.subplots(figsize=(8, 8))  # Agrandir la figure
        wedges, texts, autotexts = ax.pie(valeurs, labels=labels, autopct='%1.1f%%',
                                          startangle=90, colors=couleurs, wedgeprops={'edgecolor': 'black'})

        for text in autotexts:
            text.set_color("white")
            text.set_fontsize(12)

        ax.legend(wedges, labels, title="Statistiques", loc="upper right", bbox_to_anchor=(1.2, 0.8))
        ax.axis('equal')

        # Intégrer le graphique dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Mettre à jour la scrollbar
        self.graph_container.update_idletasks()
        self.canvas_frame.config(scrollregion=self.canvas_frame.bbox("all"))

    def exporter_en_pdf(self):
        """
        Exporte les statistiques en PDF.
        """
        messagebox.showinfo("Succès", "Exportation PDF réussie !")

class PDFPage:
    def generer_liste_candidats(self, candidats):
        """Simule la génération d'un fichier PDF avec la liste des candidats."""
        with open("liste_candidats.pdf", "w", encoding="utf-8") as file:
            file.write("Liste des candidats:\n")
            for candidat in candidats:
                file.write(f"- {candidat}\n")
        print(f"Fichier PDF généré : liste_candidats.pdf")

    def generer_pv_deliberation(self, pv_content):
        """Simule la génération d'un fichier PDF avec le PV de délibération."""
        with open("pv_deliberation.pdf", "w", encoding="utf-8") as file:
            file.write(pv_content)
        print(f"Fichier PDF généré : pv_deliberation.pdf")

    def generer_releve_notes(self, releve_content):
        """Simule la génération d'un fichier PDF avec le relevé de notes."""
        with open("releve_notes.pdf", "w", encoding="utf-8") as file:
            file.write(releve_content)
        print(f"Fichier PDF généré : releve_notes.pdf")

def ouvrir_fichier_pdf(fichier_pdf):
    """
    Ouvre un fichier PDF avec le lecteur PDF par défaut du système.
    
    :param fichier_pdf: Le chemin du fichier PDF à ouvrir.
    """
    if os.name == 'nt':  # Pour Windows
        os.startfile(fichier_pdf)
    elif os.name == 'posix':  # Pour macOS et Linux
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener, fichier_pdf])
    else:
        raise OSError("Système d'exploitation non supporté")

class PDFPageUI(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Impression en PDF")

        self.frame_principal = tk.Frame(self, bg="#ffffff")
        self.frame_principal.pack(pady=20, padx=50, fill="both", expand=True)

        # Bouton pour générer la liste des candidats en PDF
        ttk.Button(self.frame_principal, text="Générer Liste des Candidats",
                   command=self.generer_liste_candidats_pdf, style="Blue.TButton").pack(pady=20)

        # Bouton pour générer le PV de délibération en PDF
        ttk.Button(self.frame_principal, text="Générer PV de Délibération",
                   command=self.generer_pv_deliberation_pdf, style="Blue.TButton").pack(pady=20)

        # Champ pour entrer le numéro de table
        tk.Label(self.frame_principal, text="Numéro de Table:", bg="#ffffff", fg="#333333",
                 font=controller.label_font).pack(pady=5)
        self.numero_table_entry = ttk.Entry(self.frame_principal, font=controller.entry_font, style="Blue.TEntry")
        self.numero_table_entry.pack(pady=5, fill="x")

        # Bouton pour générer un relevé de notes
        ttk.Button(self.frame_principal, text="Générer Relevé de Notes",
                   command=self.generer_releve_notes_pdf, style="Blue.TButton").pack(pady=20)

    def generer_liste_candidats_pdf(self):
        """Génère un PDF avec la liste des candidats et l'ouvre automatiquement"""
        pdf = PDFPage()
        candidats = self.controller.candidat.lister_candidats()  # Récupérer la liste des candidats
        fichier_pdf = "liste_candidats.pdf"
        pdf.generer_liste_candidats(candidats)
        messagebox.showinfo("Succès", f"Liste des candidats générée en PDF : {fichier_pdf}")
        ouvrir_fichier_pdf(fichier_pdf)  # Ouvrir le fichier PDF

    def generer_releve_notes_pdf(self):
        """Génère un PDF avec le relevé de notes d'un candidat et l'ouvre automatiquement"""
        pdf = PDFPage()
        numero_table = self.numero_table_entry.get()  # Récupérer le numéro de table depuis l'interface

        if not numero_table:
            messagebox.showerror("Erreur", "Veuillez entrer un numéro de table.")
            return

        # Récupérer les informations du candidat et ses notes
        conn = sqlite3.connect('bfem.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.Numero_Table, c.Prenom_s, c.Nom, n.Compo_Franc, n.Dictee, n.Etude_de_texte, 
                   n.Instruction_Civique, n.Histoire_Geographie, n.Mathematiques, n.PC_LV2, 
                   n.SVT, n.Anglais1, n.Anglais_Oral, n.EPS, n.Epreuve_Facultative
            FROM Candidat c
            JOIN Notes n ON c.Numero_Table = n.Numero_Table
            WHERE c.Numero_Table = ?
        ''', (numero_table,))

        candidat = cursor.fetchone()
        conn.close()

        if not candidat:
            messagebox.showerror("Erreur", "Aucun candidat trouvé avec ce numéro de table.")
            return

        # Créer un dictionnaire avec les informations du candidat et ses notes
        candidat_info = {
            "Numéro Table": candidat[0],
            "Nom": candidat[2],
            "Prénom": candidat[1]
        }

        notes = {
            "Composition Française": candidat[3],
            "Dictée": candidat[4],
            "Étude de Texte": candidat[5],
            "Instruction Civique": candidat[6],
            "Histoire-Géographie": candidat[7],
            "Mathématiques": candidat[8],
            "PC/LV2": candidat[9],
            "SVT": candidat[10],
            "Anglais Écrit": candidat[11],
            "Anglais Oral": candidat[12],
            "EPS": candidat[13],
            "Épreuve Facultative": candidat[14]
        }

        # Générer le PDF
        fichier_pdf = f"releve_notes_{candidat_info['Numéro Table']}.pdf"
        pdf.generer_releve_notes(candidat_info, notes)
        messagebox.showinfo("Succès", f"Relevé de notes généré en PDF : {fichier_pdf}")
        ouvrir_fichier_pdf(fichier_pdf)  # Ouvrir le fichier PDF

    def generer_pv_deliberation_pdf(self):
        """Génère un PDF avec le PV de délibération et l'ouvre automatiquement"""
        pdf = PDFPage()
        deliberation = Deliberation()

        # Récupérer les résultats de la délibération pour tous les candidats
        conn = sqlite3.connect('bfem.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Numero_Table, Nom, Prenom_s FROM Candidat')
        candidats = cursor.fetchall()

        pv_content = "Procès-Verbal de Délibération\n\n"
        for candidat in candidats:
            numero_table, nom, prenom = candidat
            points = deliberation.calculer_points(numero_table)
            resultat = deliberation.deliberer(numero_table)
            pv_content += f"Candidat: {nom} {prenom} (Table {numero_table})\n"
            pv_content += f"Points: {points}\n"
            pv_content += f"Résultat: {resultat}\n\n"

        conn.close()

        # Générer le PDF
        fichier_pdf = "pv_deliberation.pdf"
        pdf.generer_pv_deliberation(pv_content)
        messagebox.showinfo("Succès", f"PV de délibération généré en PDF : {fichier_pdf}")
        ouvrir_fichier_pdf(fichier_pdf)  # Ouvrir le fichier PDF



class GestionSecondTourPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Gestion du Second Tour")

        # Initialisation de GestionSecondTour avec le chemin de la base de données
        self.db_path = "bfem.db"  # Définir le chemin de la base de données
        self.gestion_second_tour = GestionSecondTour(self.db_path)  # Passer db_path à GestionSecondTour

        # Configuration des styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("Blue.TButton", background="#4CAF50", foreground="white", font=("Helvetica", 12, "bold"))
        self.style.configure("TEntry", font=("Helvetica", 12), padding=5)

        # Cadre principal
        self.frame_principal = ttk.Frame(self, padding="20")
        self.frame_principal.pack(fill="both", expand=True)

        # Titre de la page
        self.title_label = ttk.Label(self.frame_principal, text="Gestion du Second Tour", font=("Helvetica", 20, "bold"), background="#f0f0f0", foreground="#333333")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Liste des anonymats des candidats admis au second tour ou repêchables
        self.liste_anonymats = tk.Listbox(self.frame_principal, width=60, height=10)
        self.liste_anonymats.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Bouton pour actualiser la liste des anonymats
        self.actualiser_button = ttk.Button(self.frame_principal, text="Actualiser la liste", command=self.actualiser_liste_anonymats, style="Blue.TButton")
        self.actualiser_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        # Champ pour la note de Français
        self.francais_label = ttk.Label(self.frame_principal, text="Français :", background="#f0f0f0")
        self.francais_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.francais_entry = ttk.Entry(self.frame_principal, width=30)
        self.francais_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Champ pour la note de Mathématiques
        self.math_label = ttk.Label(self.frame_principal, text="Mathématiques :", background="#f0f0f0")
        self.math_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.math_entry = ttk.Entry(self.frame_principal, width=30)
        self.math_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Champ pour la note de PC/LV2
        self.pc_lv2_label = ttk.Label(self.frame_principal, text="PC/LV2 :", background="#f0f0f0")
        self.pc_lv2_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.pc_lv2_entry = ttk.Entry(self.frame_principal, width=30)
        self.pc_lv2_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # Bouton pour enregistrer les notes
        self.save_button = ttk.Button(self.frame_principal, text="Enregistrer les notes", command=self.enregistrer_notes, style="Blue.TButton")
        self.save_button.grid(row=6, column=0, columnspan=2, pady=20, sticky="ew")

        # Bouton pour lancer la délibération
        self.deliberer_button = ttk.Button(self.frame_principal, text="Délibérer le second tour", command=self.deliberer_second_tour, style="Blue.TButton")
        self.deliberer_button.grid(row=7, column=0, columnspan=2, pady=20, sticky="ew")

        # Bouton de retour
        self.retour_button = ttk.Button(self.frame_principal, text="Retour", command=lambda: self.controller.show_frame("HomePage"), style="Blue.TButton")
        self.retour_button.grid(row=8, column=0, columnspan=2, pady=20, sticky="ew")

        # Actualiser la liste des anonymats au démarrage
        self.actualiser_liste_anonymats()

    def actualiser_liste_anonymats(self):
        """Actualise la liste des anonymats des candidats admis au second tour ou repêchables."""
        self.liste_anonymats.delete(0, tk.END)  # Efface la liste actuelle

        # Récupérer les anonymats des candidats admis au second tour ou repêchables
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT a.anonymat
                FROM anonymats a
                JOIN Candidat c ON a.numero_table = c.Numero_Table
                JOIN Notes n ON c.Numero_Table = n.Numero_Table
                JOIN Livret_Scolaire l ON c.Numero_Table = l.Numero_Table
                WHERE (n.Points >= 153)  -- Admis au second tour (RM5)
                   OR (n.Points BETWEEN 76 AND 79.9 AND l.Nombre_de_fois <= 2)  -- Repêchable pour le second tour (RM10 et RM12)
            """)
            anonymats = cur.fetchall()

            # Ajouter les anonymats à la liste
            for anonymat in anonymats:
                self.liste_anonymats.insert(tk.END, anonymat[0])

    def enregistrer_notes(self):
        """Enregistre les notes du second tour."""
        # Récupérer l'anonymat sélectionné
        selection = self.liste_anonymats.curselection()
        if not selection:
            messagebox.showerror("Erreur", "Veuillez sélectionner un anonymat.")
            return

        anonymat = self.liste_anonymats.get(selection[0])

        # Récupérer les notes
        francais = self.francais_entry.get().strip()
        math = self.math_entry.get().strip()
        pc_lv2 = self.pc_lv2_entry.get().strip()

        if not francais or not math or not pc_lv2:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        try:
            francais = float(francais)
            math = float(math)
            pc_lv2 = float(pc_lv2)
        except ValueError:
            messagebox.showerror("Erreur", "Les notes doivent être des nombres décimaux.")
            return

        # Enregistrer les notes
        success, message = self.gestion_second_tour.saisir_notes_second_tour(anonymat, francais, math, pc_lv2)
        if success:
            messagebox.showinfo("Succès", message)
            self.francais_entry.delete(0, tk.END)
            self.math_entry.delete(0, tk.END)
            self.pc_lv2_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", message)

    def deliberer_second_tour(self):
        """Lance la délibération du second tour et affiche les résultats."""
        # Lancer la délibération
        success, message = self.gestion_second_tour.deliberer_second_tour()

        if success:
            # Afficher un message de succès
            messagebox.showinfo("Succès", message)

            # Récupérer les résultats de la délibération depuis la base de données
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT c.Numero_Table, c.Prenom_s, c.Nom, n.Resultat
                    FROM Candidat c
                    JOIN Notes n ON c.Numero_Table = n.Numero_Table
                    WHERE n.Resultat IS NOT NULL
                """)
                resultats = cur.fetchall()

            # Afficher les résultats dans une zone de texte
            self.afficher_resultats(resultats)
        else:
            # Afficher un message d'erreur
            messagebox.showerror("Erreur", message)

    def afficher_resultats(self, resultats):
        """Affiche les résultats de la délibération dans une zone de texte."""
        # Créer une nouvelle fenêtre pour afficher les résultats
        resultats_window = tk.Toplevel(self)
        resultats_window.title("Résultats de la Délibération")
        resultats_window.geometry("600x400")

        # Ajouter une zone de texte avec une barre de défilement
        text_frame = tk.Frame(resultats_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        resultats_text = tk.Text(text_frame, wrap="none", yscrollcommand=scrollbar.set)
        resultats_text.pack(fill="both", expand=True)

        scrollbar.config(command=resultats_text.yview)

        # Ajouter les résultats dans la zone de texte
        resultats_text.insert("end", "Résultats de la Délibération :\n\n")
        for resultat in resultats:
            numero_table, prenom, nom, statut = resultat
            resultats_text.insert("end", f"Numéro Table: {numero_table}\n")
            resultats_text.insert("end", f"Nom: {nom} {prenom}\n")
            resultats_text.insert("end", f"Statut: {statut}\n")
            resultats_text.insert("end", "-" * 50 + "\n")

        # Désactiver l'édition de la zone de texte
        resultats_text.config(state="disabled")
# Configuration des styles
def configure_styles():
    style = ttk.Style()
    style.configure("Blue.TButton", font=("Helvetica", 12, "bold"),
                    background="#007BFF", foreground="white",
                    borderwidth=0, focusthickness=3, focuscolor="#007BFF",
                    padding=10, relief="flat")
    style.map("Blue.TButton", background=[("active", "#0056b3")])
    style.configure("Blue.TEntry", font=("Helvetica", 12), borderwidth=2,
                    relief="flat", padding=5, fieldbackground="#ffffff",
                    foreground="#333333")


# Configuration des styles
configure_styles()
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

