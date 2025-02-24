import pandas as pd
import sqlite3

def create_database():
    file_path = 'BD_BFEM.xlsx'

    try:
        df = pd.read_excel(file_path)
        df['Date de nais.'] = pd.to_datetime(df['Date de nais.'])
        df['Date de nais.'] = df['Date de nais.'].dt.strftime('%Y-%m-%d')

        conn = sqlite3.connect('bfem.db')
        cursor = conn.cursor()

        # Table Candidat
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Candidat (
                Numero_Table INTEGER PRIMARY KEY,
                Prenom_s TEXT,
                Nom TEXT,
                Date_Naissance TEXT,
                Lieu_Naissance TEXT,
                Sexe TEXT,
                Nationalite TEXT,
                Choix_Epr_Facultative BOOLEAN,
                Epreuve_Facultative TEXT,
                Aptitude_Sportive BOOLEAN
            )
        ''')

        # Table Livret_Scolaire
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Livret_Scolaire (
                Numero_Table INTEGER,
                Nombre_de_fois INTEGER,
                Moyenne_6e DECIMAL,
                Moyenne_5e DECIMAL,
                Moyenne_4e DECIMAL,
                Moyenne_3e DECIMAL,
                Moyenne_Cycle DECIMAL,
                FOREIGN KEY (Numero_Table) REFERENCES Candidat(Numero_Table)
            )
        ''')

        # Supprimer la table Notes si elle existe
        cursor.execute('DROP TABLE IF EXISTS Notes')

        # Table Notes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Notes (
                Numero_Table INTEGER,
                Compo_Franc DECIMAL,
                Coef1 INTEGER,
                Dictee DECIMAL,
                Coef2 INTEGER,
                Etude_de_texte DECIMAL,
                Coef3 INTEGER,
                Instruction_Civique DECIMAL,
                Coef4 INTEGER,
                Histoire_Geographie DECIMAL,
                Coef5 INTEGER,
                Mathematiques DECIMAL,
                Coef6 INTEGER,
                PC_LV2 DECIMAL,
                Coef7 INTEGER,
                SVT DECIMAL,
                Coef8 INTEGER,
                Anglais1 DECIMAL,
                Coef9 INTEGER,
                Anglais_Oral DECIMAL,
                Coef10 INTEGER,
                EPS DECIMAL,
                Epreuve_Facultative DECIMAL,
                Points DECIMAL,  -- Ajout de la colonne Points
                FOREIGN KEY (Numero_Table) REFERENCES Candidat(Numero_Table)
            )
        ''')

        # Table Anonymat
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anonymats (
                numero_table TEXT PRIMARY KEY,
                anonymat TEXT UNIQUE,
                FOREIGN KEY (numero_table) REFERENCES Candidat (numero_table)
            )
        """)

        # Table Jury
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jury (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region TEXT,
                departement TEXT,
                localite TEXT,
                centre_examen TEXT,
                president_jury TEXT,
                telephone TEXT
            )
        """)
        # Table SecondTour
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SecondTour (
                Numero_Table INTEGER PRIMARY KEY,
                Francais DECIMAL,
                Math DECIMAL,
                PC_LV2 DECIMAL,
                Points_Second_Tour DECIMAL,
                Points_Totaux DECIMAL,
                FOREIGN KEY (Numero_Table) REFERENCES Candidat(Numero_Table)
            )
        ''')
        # Suppression des données existantes
        cursor.execute('DELETE FROM Candidat')
        cursor.execute('DELETE FROM Livret_Scolaire')
        cursor.execute('DELETE FROM anonymats')

        # Insertion des données
        for index, row in df.iterrows():
            # Insertion dans la table Candidat
            cursor.execute('''
                INSERT INTO Candidat (Numero_Table, Prenom_s, Nom, Date_Naissance, Lieu_Naissance, Sexe, Nationalite, Choix_Epr_Facultative, Epreuve_Facultative, Aptitude_Sportive)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['N° de table'],
                row['Prenom (s)'],
                row['NOM'],
                row['Date de nais.'],
                row['Lieu de nais.'],
                row['Sexe'],
                row['Nationnallité'],
                row['Type de candidat'],
                row['Epreuve Facultative'],
                row['Etat Sportif']
            ))

            # Insertion dans la table Livret_Scolaire
            cursor.execute('''
                INSERT INTO Livret_Scolaire (Numero_Table, Nombre_de_fois, Moyenne_6e, Moyenne_5e, Moyenne_4e, Moyenne_3e, Moyenne_Cycle)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['N° de table'],
                row['Nb fois'],
                row['Moy_6e'],
                row['Moy_5e'],
                row['Moy_4e'],
                row['Moy_3e'],
                (row['Moy_6e'] + row['Moy_5e'] + row['Moy_4e'] + row['Moy_3e']) / 4
            ))

            # Calcul des points totaux
            points = (
                (row['Note CF'] * 2) +  # Composition Française (Coef 2)
                (row['Note Ort'] * 1) +  # Dictée (Coef 1)
                (row['Note TSQ'] * 1) +  # Étude de Texte (Coef 1)
                (row['Note IC'] * 1) +   # Instruction Civique (Coef 1)
                (row['Note HG'] * 2) +   # Histoire-Géographie (Coef 2)
                (row['Note MATH'] * 4) + # Mathématiques (Coef 4)
                (row['Note PC/LV2'] * 2) + # PC/LV2 (Coef 2)
                (row['Note SVT'] * 2) +  # SVT (Coef 2)
                (row['Note ANG1'] * 2) + # Anglais Écrit (Coef 2)
                (row['Note ANG2'] * 1) + # Anglais Oral (Coef 1)
                row['Note EPS'] +         # EPS (pas de coefficient)
                (row['Note Ep Fac'] if row['Note Ep Fac'] > 10 else 0)  # Bonus épreuve facultative
            )

            # Insertion dans la table Notes
            cursor.execute('''
                INSERT INTO Notes (Numero_Table, Compo_Franc, Coef1, Dictee, Coef2, Etude_de_texte, Coef3, Instruction_Civique, Coef4, Histoire_Geographie, Coef5, Mathematiques, Coef6, PC_LV2, Coef7, SVT, Coef8, Anglais1, Coef9, Anglais_Oral, Coef10, EPS, Epreuve_Facultative, Points)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['N° de table'],
                row['Note CF'], 2,
                row['Note Ort'], 1,
                row['Note TSQ'], 1,
                row['Note IC'], 1,
                row['Note HG'], 2,
                row['Note MATH'], 4,
                row['Note PC/LV2'], 2,
                row['Note SVT'], 2,
                row['Note ANG1'], 2,
                row['Note ANG2'], 1,
                row['Note EPS'],
                row['Note Ep Fac'],
                points  # Ajout des points totaux
            ))

        conn.commit()
        conn.close()

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{file_path}' est introuvable.")
    except sqlite3.IntegrityError as e:
        print(f"Erreur d'intégrité : {e}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    create_database()