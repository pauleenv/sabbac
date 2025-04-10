import random

class Carte:
    def __init__(self, valeur, type_carte="normal", couleur="Sable"):
        self.valeur = valeur
        self.type_carte = type_carte
        self.couleur = couleur  # 'Sable' ou 'Sang'

    def __repr__(self):
        return f"{self.valeur} ({self.type_carte}, {self.couleur})"

class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.main = []
        self.jetons = 8  # Réduit à 8 jetons

    def recevoir_carte(self, carte):
        if len(self.main) < 2:
            self.main.append(carte)
        else:
            # Remplace la carte de même couleur
            if carte.couleur == "Sable":
                self.main[0] = carte
            elif carte.couleur == "Sang":
                self.main[1] = carte

    def piocher_carte(self, pioches, defausses, est_bot=False):
        if self.jetons > 0:
            # Vérifier si le joueur a déjà une paire
            if self.a_une_paire():
                if self.valeur_main() <= 2 and not self.a_pur_sabacc():
                    print(f"{self.nom} a une paire faible et ne pioche pas.")
                    return

            self.jetons -= 1  # Déduit un jeton

            if est_bot:
                # Stratégie pour les bots
                carte_sable = self.main[0] if self.main and self.main[0].couleur == "Sable" else None
                carte_sang = self.main[1] if self.main and self.main[1].couleur == "Sang" else None

                # Choisir la carte à remplacer
                if carte_sable and carte_sang:
                    if carte_sable.valeur > carte_sang.valeur:
                        couleur_a_remplacer = "Sable"
                    else:
                        couleur_a_remplacer = "Sang"
                elif carte_sable:
                    couleur_a_remplacer = "Sable"
                else:
                    couleur_a_remplacer = "Sang"

                # Vérifier la défausse pour une carte plus faible
                if defausses[couleur_a_remplacer]:
                    meilleure_carte = min(defausses[couleur_a_remplacer], key=lambda c: c.valeur)
                    if meilleure_carte.valeur < (carte_sable.valeur if couleur_a_remplacer == "Sable" else carte_sang.valeur):
                        nouvelle_carte = meilleure_carte
                        defausses[couleur_a_remplacer].remove(nouvelle_carte)
                    else:
                        nouvelle_carte = pioches[couleur_a_remplacer].pop()
                else:
                    nouvelle_carte = pioches[couleur_a_remplacer].pop()
            else:
                choix_couleur = input(f"{self.nom}, voulez-vous piocher une carte 'Sable' ou 'Sang' ? (s/a): ").strip().lower()
                choix_source = input(f"Voulez-vous piocher depuis la pioche ou la défausse ? (p/d): ").strip().lower()

                choix_couleur = 'Sable' if choix_couleur == 's' else 'Sang'
                choix_source = 'pioche' if choix_source == 'p' else 'defausse'

                if choix_source == 'pioche':
                    if pioches[choix_couleur]:
                        nouvelle_carte = pioches[choix_couleur].pop()
                    else:
                        print(f"La pioche '{choix_couleur}' est vide !")
                        return
                elif choix_source == 'defausse':
                    if defausses[choix_couleur]:
                        nouvelle_carte = defausses[choix_couleur].pop()
                    else:
                        print(f"La défausse '{choix_couleur}' est vide !")
                        return
                else:
                    print("Choix invalide !")
                    return

            self.recevoir_carte(nouvelle_carte)
        else:
            print(f"{self.nom} n'a pas assez de jetons pour piocher une carte.")

    def a_une_paire(self):
        if len(self.main) == 2:
            return self.main[0].valeur == self.main[1].valeur
        return False

    def a_pur_sabacc(self):
        if len(self.main) == 2:
            return self.main[0].type_carte == "Sylop" and self.main[1].type_carte == "Sylop"
        return False

    def valeur_main(self):
        valeurs = [carte.valeur for carte in self.main]
        if any(carte.type_carte == "Sylop" for carte in self.main):
            # Si un Sylop est présent, il prend la valeur de l'autre carte
            sylop_carte = next(carte for carte in self.main if carte.type_carte == "Sylop")
            autre_carte = next(carte for carte in self.main if carte.type_carte != "Sylop")
            return autre_carte.valeur
        return abs(valeurs[0] - valeurs[1]) if len(valeurs) == 2 else float('inf')

    def somme_main(self):
        valeurs = [carte.valeur for carte in self.main]
        return sum(valeurs) if len(valeurs) == 2 else float('inf')

    def ameliore_main(self, nouvelle_carte):
        # Vérifier si la nouvelle carte améliore la main
        nouvelle_main = self.main[:]
        nouvelle_main[0 if nouvelle_carte.couleur == "Sable" else 1] = nouvelle_carte
        nouvelle_valeur_main = self.calculer_valeur_main(nouvelle_main)
        nouvelle_somme_main = self.calculer_somme_main(nouvelle_main)

        if nouvelle_valeur_main < self.valeur_main() or (nouvelle_valeur_main == self.valeur_main() and nouvelle_somme_main < self.somme_main()):
            return True
        return False

    def calculer_valeur_main(self, main):
        valeurs = [carte.valeur for carte in main]
        if any(carte.type_carte == "Sylop" for carte in main):
            # Si un Sylop est présent, il prend la valeur de l'autre carte
            sylop_carte = next(carte for carte in main if carte.type_carte == "Sylop")
            autre_carte = next(carte for carte in main if carte.type_carte != "Sylop")
            return autre_carte.valeur
        return abs(valeurs[0] - valeurs[1]) if len(valeurs) == 2 else float('inf')

    def calculer_somme_main(self, main):
        valeurs = [carte.valeur for carte in main]
        return sum(valeurs) if len(valeurs) == 2 else float('inf')

    def appliquer_imposteur(self):
        if any(carte.type_carte == "Imposteur" for carte in self.main):
            print(f"{self.nom} utilise un Imposteur !")
            if self.nom == "Joueur 1":
                des1 = random.randint(1, 6)
                des2 = random.randint(1, 6)
                print(f"Dés lancés : {des1} et {des2}")
                choix_des = int(input(f"{self.nom}, choisissez un résultat de dé (1 pour {des1}, 2 pour {des2}) : ").strip())
                if choix_des == 1:
                    nouvelle_valeur = des1
                else:
                    nouvelle_valeur = des2
            else:
                # Logique pour les bots
                des1 = random.randint(1, 6)
                des2 = random.randint(1, 6)
                print(f"{self.nom} a lancé les dés : {des1} et {des2}")
                nouvelle_valeur1 = min(des1, des2)
                des1 = random.randint(1, 6)
                des2 = random.randint(1, 6)
                print(f"{self.nom} a lancé les dés une deuxième fois : {des1} et {des2}")
                nouvelle_valeur2 = min(des1, des2)

            for i, carte in enumerate(self.main):
                if carte.type_carte == "Imposteur":
                    if i == 0:
                        self.main[i].valeur = nouvelle_valeur1
                    else:
                        self.main[i].valeur = nouvelle_valeur2
                    break

    def __repr__(self):
        return f"{self.nom}: {self.main}, Jetons: {self.jetons}"

def creer_deck():
    valeurs = list(range(1, 7))  # Valeurs de 1 à 6
    couleurs = ["Sable", "Sang"]
    deck = {
        'Sable': [Carte(valeur, couleur='Sable') for valeur in valeurs for _ in range(3)],
        'Sang': [Carte(valeur, couleur='Sang') for valeur in valeurs for _ in range(3)]
    }
    deck['Sable'].append(Carte(0, "Sylop", "Sable"))
    deck['Sang'].append(Carte(0, "Sylop", "Sang"))
    deck['Sable'].extend([Carte(0, "Imposteur", "Sable") for _ in range(3)])
    deck['Sang'].extend([Carte(0, "Imposteur", "Sang") for _ in range(3)])

    for couleur in deck:
        random.shuffle(deck[couleur])

    return deck

def distribuer_cartes(pioches, joueurs):
    for joueur in joueurs:
        while len(joueur.main) < 2:
            if not joueur.main or joueur.main[0].couleur != "Sable":
                carte = pioches['Sable'].pop()
                joueur.recevoir_carte(carte)
            if len(joueur.main) < 2 or joueur.main[1].couleur != "Sang":
                carte = pioches['Sang'].pop()
                joueur.recevoir_carte(carte)

def jouer_tour(joueurs, pioches, defausses):
    for joueur in joueurs:
        print(joueur)
        if joueur.nom == "Joueur 1":  # Pour le joueur humain
            while True:
                action = input(f"{joueur.nom}, voulez-vous piocher une carte ? (o/n): ").strip().lower()
                if action in ['o', 'n']:
                    break
                print("Entrée invalide. Veuillez entrer 'o' pour oui ou 'n' pour non.")
            if action == 'o':
                joueur.piocher_carte(pioches, defausses)
        else:  # Pour les bots
            joueur.piocher_carte(pioches, defausses, est_bot=True)


def classer_joueurs(joueurs):
    # Classer les joueurs par paire, puis par valeur de la paire, puis par somme des cartes
    joueurs_pur_sabacc = [j for j in joueurs if j.a_pur_sabacc()]
    joueurs_prime_sabacc = [j for j in joueurs if j.a_une_paire() and j.valeur_main() == 1 and not j.a_pur_sabacc()]
    joueurs_paire = [j for j in joueurs if j.a_une_paire() and not j.a_pur_sabacc() and not j.valeur_main() == 1]
    joueurs_sans_paire = [j for j in joueurs if not j.a_une_paire()]

    joueurs_pur_sabacc.sort(key=lambda j: j.somme_main())
    joueurs_prime_sabacc.sort(key=lambda j: j.somme_main())
    joueurs_paire.sort(key=lambda j: (j.valeur_main(), j.somme_main()))
    joueurs_sans_paire.sort(key=lambda j: j.somme_main())

    return joueurs_pur_sabacc + joueurs_prime_sabacc + joueurs_paire + joueurs_sans_paire



def main():
    joueurs = [Joueur("Joueur 1"), Joueur("Bot 1"), Joueur("Bot 2"), Joueur("Bot 3")]
    pioches = creer_deck()
    defausses = {'Sable': [], 'Sang': []}
    distribuer_cartes(pioches, joueurs)

    for tour in range(3):
        print(f"\n--- Tour {tour + 1} ---")
        jouer_tour(joueurs, pioches, defausses)

    # Appliquer l'effet des Imposteurs avant le classement final
    for joueur in joueurs:
        joueur.appliquer_imposteur()

    # Appliquer l'effet des Sylops après les Imposteurs
    for joueur in joueurs:
        if any(carte.type_carte == "Sylop" for carte in joueur.main):
            sylop_carte = next(carte for carte in joueur.main if carte.type_carte == "Sylop")
            autre_carte = next(carte for carte in joueur.main if carte.type_carte != "Sylop")
            sylop_carte.valeur = autre_carte.valeur

    # Classement final
    classement = classer_joueurs(joueurs)
    print("\n--- Classement Final ---")
    for i, joueur in enumerate(classement, start=1):
        print(f"{i}. {joueur.nom} avec une main de valeur {joueur.valeur_main()} et une somme de {joueur.somme_main()}, Jetons restants: {joueur.jetons}")
        print(f"Main: {joueur.main}")

if __name__ == "__main__":
    main()
