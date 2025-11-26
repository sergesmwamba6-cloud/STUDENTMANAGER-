import tkinter as tk
from tkinter import ttk, messagebox, font
import csv
import os

FICHIER_DONNEES = 'etudiants.csv'
MATRICULE_INDEX = 0

class GestionEtudiants(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des étudiants")
        self.geometry("900x650")
        self.configure(bg="#6F4E37")

        self.etudiants = []
        self.dernier_matricule = 0
        self.charger_donnees()

        self.matricule_var = tk.StringVar(
            value=str(self.dernier_matricule + 1))
        self.nom_var = tk.StringVar()
        self.postnom_var = tk.StringVar()
        self.prenom_var = tk.StringVar()
        self.sexe_var = tk.StringVar(value="M")
        self.departement_var = tk.StringVar()
        self.rechercher_var = tk.StringVar()

        self._configurer_styles()
        self._creer_widgets()
        self.tree_frame.pack_forget()
        self.protocol("WM_DELETE_WINDOW", self.on_fermeture)


    def charger_donnees(self):
        """ Charge les données des étudiants depuis le fichier CSV et détermine le dernier matricule. """
        self.etudiants = []
        max_matricule = 0
        if os.path.exists(FICHIER_DONNEES):
            try:
                with open(FICHIER_DONNEES, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        self.etudiants.append(tuple(row))
                        try:
                            max_matricule = max(max_matricule, int(row[MATRICULE_INDEX]))
                        except ValueError:
                            continue
                self.dernier_matricule = max_matricule
            except Exception as e:
                messagebox.showerror("Erreur de Chargement", f"Impossible de lire le fichier CSV : {e}")
        else:
            self.dernier_matricule = 0

    def _get_next_matricule(self):
        """ Incrémente et retourne le prochain matricule disponible. """
        self.dernier_matricule += 1
        return str(self.dernier_matricule)

    def _configurer_styles(self):
        # ... (Styles inchangés)
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('.', background="#6F4E37", foreground="white")
        style.configure('TFrame', background="#6F4E37")
        style.configure('TLabel', background="#6F4E37", foreground="white", font=("Roboto", 16))
        style.configure('TEntry', fieldbackground="#D2B48C", foreground="black", font=("Roboto", 16))
        style.configure('TButton', background="#8B4513", foreground="black", font=("Roboto", 12, "bold"), padding=5)
        style.map('TButton', background=[('active', '#A0522D')])
        style.configure('TMenubutton', background="#D2B48C", foreground="black", font=("Roboto", 16))
        style.configure("Treeview",
                        background="lightgrey",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="lightgrey",
                        font=("Roboto", 12))
        style.map('Treeview', background=[('selected', '#347083')])
        style.configure("Treeview.Heading",
                        font=("Roboto", 12, "bold"),
                        background="#ADD8E6",
                        foreground="black")
        try:
            title_font = font.Font(family="Roboto", size=30, weight="bold")
            self.option_add("*Font", title_font)
        except tk.TclError:
            title_font = font.Font(family="Arial", size=30, weight="bold")
        style.configure("Title.TLabel",
                        background="skyblue",
                        foreground="navy",
                        font=title_font)

    def vider_champs(self, keep_matricule=False):
        """ Vide les champs de saisie et réinitialise le champ de recherche. """
        if not keep_matricule:
            self.matricule_var.set(str(self.dernier_matricule + 1))
        self.nom_var.set("")
        self.postnom_var.set("")
        self.prenom_var.set("")
        self.sexe_var.set("M")
        self.departement_var.set("")
        self.rechercher_var.set("")

    def _creer_widgets(self):

        # --- Cadre de Titre ---
        title_frame = ttk.Frame(self, padding="10", style="Title.TLabel")
        title_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(title_frame, text="GESTION DES ÉTUDIANTS", style="Title.TLabel").pack(expand=True)

        # --- Cadre de Saisie (input_frame) ---
        self.input_frame = ttk.Frame(self, padding="10")
        self.input_frame.pack(fill='x')

        # Matricule (lecture seule, auto-incrémenté)
        ttk.Label(self.input_frame, text="Matricule:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(self.input_frame, textvariable=self.matricule_var, relief="solid", width=30).grid(row=0, column=1,
                                                                                                    sticky='ew', padx=5,
                                                                                                    pady=2)

        # Les autres champs sont des Entry
        self.entry_nom = ttk.Entry(self.input_frame, textvariable=self.nom_var, width=30)
        self.entry_postnom = ttk.Entry(self.input_frame, textvariable=self.postnom_var, width=30)
        self.entry_prenom = ttk.Entry(self.input_frame, textvariable=self.prenom_var, width=30)
        self.entry_departement = ttk.Entry(self.input_frame, textvariable=self.departement_var, width=30)

        ttk.Label(self.input_frame, text="Nom:").grid(row=1, column=0, sticky='w', padx=5, pady=2);
        self.entry_nom.grid(row=1, column=1, sticky='ew', padx=5, pady=2)

        ttk.Label(self.input_frame, text="Post-Nom:").grid(row=2, column=0, sticky='w', padx=5, pady=2);
        self.entry_postnom.grid(row=2, column=1, sticky='ew', padx=5, pady=2)

        ttk.Label(self.input_frame, text="Prénom:").grid(row=3, column=0, sticky='w', padx=5, pady=2);
        self.entry_prenom.grid(row=3, column=1, sticky='ew', padx=5, pady=2)

        ttk.Label(self.input_frame, text="Département:").grid(row=4, column=0, sticky='w', padx=5, pady=2);
        self.entry_departement.grid(row=4, column=1, sticky='ew', padx=5, pady=2)

        # Sexe
        ttk.Label(self.input_frame, text="Sexe:").grid(row=5, column=0, sticky='w', padx=5, pady=2)
        ttk.OptionMenu(self.input_frame, self.sexe_var, "M", "M", "F").grid(row=5, column=1, sticky='ew', padx=5,
                                                                            pady=2)

        # Cadre des Boutons d'Action
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill='x')
        ttk.Button(button_frame, text="ENREGISTRER", command=self.enregistrer_etudiant).pack(side='left', padx=5)
        ttk.Button(button_frame, text="MODIFIER", command=self.action_modifier).pack(side='left',
                                                                                       padx=5)
        ttk.Button(button_frame, text="CONSULTER LISTE", command=self.consulter_afficher_tout).pack(
            side='left', padx=5)
        ttk.Button(button_frame, text="SUPPRIMER", command=self.action_supprimer).pack(side='left',
                                                                                         padx=5)

        # --- Cadre de Recherche Simplifiée ---
        search_frame = ttk.Frame(self, padding="10")
        search_frame.pack(fill='x')

        ttk.Label(search_frame, text="Recherche par :").pack(side='left', padx=5)
        ttk.Entry(search_frame, textvariable=self.rechercher_var, width=25).pack(side='left', padx=5)

        ttk.Button(search_frame, text="RECHERCHER", command=self.rechercher_etudiant).pack(side='left', padx=5)

        ttk.Button(search_frame, text="EFFACER RECHERCHE", command=self.vider_recherche).pack(side='left', padx=5)

        # --- Tableau (Treeview) ---
        self.tree_frame = ttk.Frame(self, padding="10")
        columns = ("Matricule", "Nom", "Post-Nom", "Prénom", "Sexe", "Département")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=120)

        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.bind("<<TreeviewSelect>>", self.selectionner_etudiant)

    def vider_recherche(self):
        """ Vide le champ de recherche et masque le tableau. """
        self.rechercher_var.set("")
        self.afficher_etudiants(self.etudiants)
        self.afficher_tableau(show=False)

    def afficher_tableau(self, show=True):
        """ Gère l'affichage/masquage du cadre du tableau. """
        if show:
            self.tree_frame.pack(fill='both', expand=True)
            self.tree_frame.lift()
        else:
            self.tree_frame.pack_forget()

    # 1. Correction du message d'enregistrement
    def enregistrer_etudiant(self):
        """ Ajoute un nouvel étudiant. """
        matricule = self._get_next_matricule()
        nom = self.nom_var.get().strip()
        postnom = self.postnom_var.get().strip()
        prenom = self.prenom_var.get().strip()
        sexe = self.sexe_var.get()
        departement = self.departement_var.get().strip()

        if not all([nom, postnom, prenom, departement]):
            messagebox.showerror("Erreur de Saisie",
                                 "Veuillez remplir tous les champs (Nom, Post-Nom, Prénom, Département).")
            self.dernier_matricule -= 1
            return

        full_name_new = (nom.upper(), postnom.upper(), prenom.upper())
        if any((e[1].upper(), e[2].upper(), e[3].upper()) == full_name_new for e in self.etudiants):
            messagebox.showerror("Erreur de Redondance", "Un étudiant avec ce Nom, Post-Nom et Prénom existe déjà.")
            self.dernier_matricule -= 1
            return

        nouvel_etudiant = (matricule, nom, postnom, prenom, sexe, departement)
        self.etudiants.append(nouvel_etudiant)
        self.sauvegarder_donnees()
        self.vider_champs()
        # Message corrigé : inclut le nom de l'étudiant
        messagebox.showinfo("Succès",
                            f"L'étudiant : {nom} {prenom} : a été enregistré avec succès.")
        self.afficher_tableau(show=False)

    # 1. Correction du message de modification
    def action_modifier(self):
        """ Gère l'affichage de la sélection et la logique de modification. """
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Attention",
                                   "Veuillez d'abord consulter les données et sélectionner un étudiant à modifier.")
            self.consulter_afficher_tout()
            return
        self.modifier_etudiant_logic(selected_item)

    def modifier_etudiant_logic(self, selected_item):
        """ La logique réelle de modification. """
        ancienne_matricule = self.tree.item(selected_item, 'values')[0]
        nouveau_nom = self.nom_var.get().strip()
        nouveau_postnom = self.postnom_var.get().strip()
        nouveau_prenom = self.prenom_var.get().strip()
        nouveau_sexe = self.sexe_var.get()
        nouveau_departement = self.departement_var.get().strip()

        if not all([nouveau_nom, nouveau_postnom, nouveau_prenom, nouveau_departement]):
            messagebox.showerror("Erreur de Saisie", "Veuillez remplir tous les champs.")
            return

        for i, etudiant in enumerate(self.etudiants):
            if etudiant[0] == ancienne_matricule:
                self.etudiants[i] = (
                    ancienne_matricule, nouveau_nom, nouveau_postnom, nouveau_prenom, nouveau_sexe, nouveau_departement)
                self.sauvegarder_donnees()
                self.vider_champs()
                self.afficher_tableau(show=False)
                # Message corrigé : inclut le nom de l'étudiant
                messagebox.showinfo("Succès",
                                    f"Les informations de : {nouveau_nom} {nouveau_prenom} : ont été modifiées avec succès.")
                return
        messagebox.showerror("Erreur", "Erreur lors de la modification.")

    # 1. Correction du message de suppression
    def action_supprimer(self):
        """ Gère la suppression. """
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Attention",
                                   "Veuillez consulter les données et sélectionner un étudiant à supprimer.")
            self.consulter_afficher_tout()
            return

        values = self.tree.item(selected_item, 'values')
        prenom_complet = f"{values[1]} {values[3]}"
        matricule_a_supprimer = values[0]

        reponse = messagebox.askyesno("Confirmation",
                                      f"Êtes-vous sûr de vouloir supprimer l'étudiant {prenom_complet}  ?")

        if reponse:
            self.etudiants = [e for e in self.etudiants if e[0] != matricule_a_supprimer]
            self.sauvegarder_donnees()
            self.vider_champs()
            self.afficher_tableau(show=False)
            # Message corrigé : inclut le nom de l'étudiant
            messagebox.showinfo("Succès", f"L'étudiant : {prenom_complet}: a été supprimé avec succès.")

    def consulter_afficher_tout(self):
        """ Affiche le tableau avec toutes les informations. """
        self.vider_champs()
        self.afficher_etudiants(self.etudiants)
        self.afficher_tableau(show=True)

    def selectionner_etudiant(self, event):
        """ Affiche les détails de l'étudiant sélectionné dans les champs de saisie. """
        selected_item = self.tree.focus()
        if not selected_item:
            return
        values = self.tree.item(selected_item, 'values')
        if values:
            self.matricule_var.set(values[0])
            self.nom_var.set(values[1])
            self.postnom_var.set(values[2])
            self.prenom_var.set(values[3])
            self.sexe_var.set(values[4])
            self.departement_var.set(values[5])

    # 2. Correction de la logique de recherche : priorité au Prénom si non-numérique
    def rechercher_etudiant(self):
        """ Recherche unifiée par Matricule (si numérique) ou par Prénom/Nom (sinon). """
        terme_recherche = self.rechercher_var.get().strip()
        terme_recherche_upper = terme_recherche.upper()

        if not terme_recherche:
            messagebox.showwarning("Attention", "Veuillez entrer un terme pour la recherche.")
            self.afficher_tableau(show=False)
            return

        resultats = []

        if terme_recherche.isdigit():
            # Recherche par Matricule (index 0)
            index_recherche = 0
            # Recherche exacte du matricule
            resultats = [e for e in self.etudiants if e[index_recherche] == terme_recherche]
            critere = "Matricule"
        else:
            # Recherche par Prénom, puis Nom et Post-Nom
            critere = "Prénom, Nom ou Post-Nom"

            # Index : 1=Nom, 2=Post-Nom, 3=Prénom
            for etudiant in self.etudiants:
                # Priorité : Prénom
                if terme_recherche_upper in etudiant[3].upper():
                    resultats.append(etudiant)
                # Secondaire : Nom ou Post-Nom (pour s'assurer que si l'utilisateur met le nom de famille, ça marche aussi)
                elif terme_recherche_upper in etudiant[1].upper() or \
                        terme_recherche_upper in etudiant[2].upper():
                    resultats.append(etudiant)

            # Éliminer les doublons si la même personne correspondait à plusieurs critères
            resultats = list(set(resultats))

        if resultats:
            self.afficher_etudiants(resultats)
            self.afficher_tableau(show=True)
            messagebox.showinfo("Recherche", f"{len(resultats)} étudiant(s) trouvé(s) ")
        else:
            messagebox.showinfo("Recherche", f"Aucun étudiant trouvé avec le terme '{terme_recherche}'.")
            self.afficher_etudiants([])
            self.afficher_tableau(show=True)

    # --- Méthodes de Persistance et d'Affichage du Tableau (inchangées) ---
    def sauvegarder_donnees(self):
        """ Sauvegarde les données des étudiants dans le fichier CSV. """
        try:
            with open(FICHIER_DONNEES, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(self.etudiants)
            self.matricule_var.set(str(self.dernier_matricule + 1))
        except Exception as e:
            messagebox.showerror("Erreur de Sauvegarde", f"Impossible d'écrire dans le fichier CSV : {e}")

    def on_fermeture(self):
        self.sauvegarder_donnees()
        self.destroy()

    def afficher_etudiants(self, liste_etudiants):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for etudiant in liste_etudiants:
            self.tree.insert('', 'end', values=etudiant)


if __name__ == "__main__":
    app = GestionEtudiants()
    app.mainloop()
