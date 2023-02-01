import random

print("Bienvenue dans le jeu Push Your Luck!")
print("Le but du jeu est de faire un score maximum sans dépasser 21.")

score = 0
while score < 21:
    choix = input("Voulez-vous tirer une carte? (o/n)")
    if choix == 'o':
        carte = random.randint(1, 11)
        print("Vous avez pioché une carte de valeur", carte)
        score += carte
        print("Votre score actuel est de", score)
    elif choix == 'n':
        print("Vous avez choisi de ne pas tirer de carte.")
        break
    else:
        print("Entrée non valide.")

if score > 21:
    print("Vous avez perdu! Votre score final est de", score)
else:
    print("Vous avez gagné! Votre score final est de", score)