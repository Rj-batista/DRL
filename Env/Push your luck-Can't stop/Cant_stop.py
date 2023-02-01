import random

print("Bienvenue dans le jeu Can't Stop!")
print("Le but du jeu est de faire avancer autant de dés que possible sur un tableau de 4 colonnes.")

def lancer_des():
    de1 = random.randint(1, 6)
    de2 = random.randint(1, 6)
    return de1, de2

def jouer_tour():
    resultats = [0, 0, 0, 0]
    for i in range(4):
        de1, de2 = lancer_des()
        resultats[i] = de1 + de2

    print("Résultats:", resultats)
    choix = input("Quelle colonne voulez-vous avancer? (1, 2, 3, 4) ou 'q' pour quitter")
    if choix == 'q':
        return False
    else:
        colonne = int(choix) - 1
        if resultats[colonne] == 10:
            print("Vous ne pouvez pas avancer cette colonne.")
            return False
        else:
            print("Vous avancez la colonne", colonne + 1)
            return True



while True:
    tour = jouer_tour()
    if not tour:
        break

print("Fin du jeu.")

