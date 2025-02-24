import tkinter as tk
from tkinter import ttk


class BasePage(tk.Frame):
    def __init__(self, parent, controller, title):
        tk.Frame.__init__(self, parent, bg="#ffffff")  # Fond blanc
        self.controller = controller

        # En-tête de la page
        self.header = tk.Frame(self, bg="#007BFF", height=80)  # Bleu pour l'en-tête
        self.header.pack(fill="x")

        self.title_label = tk.Label(self.header, text=title, font=controller.title_font, bg="#007BFF", fg="white") # Texte blanc
        self.title_label.pack(pady=20)

        # Bouton de retour
        self.back_button = ttk.Button(self.header, text="← Retour", command=lambda: controller.show_frame("HomePage"),
                                      style="Blue.TButton")
        self.back_button.pack(side="left", padx=20)

        # Bouton de déconnexion
        self.logout_button = ttk.Button(self.header, text="Déconnexion", command=lambda: controller.show_frame("LoginPage"),
                                        style="Blue.TButton")
        self.logout_button.pack(side="right", padx=20)