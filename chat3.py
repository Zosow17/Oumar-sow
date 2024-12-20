import re

def lire_fichier_et_classer(chemin_fichier):
    """Lit un fichier et classe les mots en fonction de leur type (alpha, num, alphanum, autre)."""
    # Dictionnaires pour stocker les mots dans différentes catégories
    groupes = {
        'alpha': [],
        'numerique': [],
        'alphanum': [],
        'autre': []
    }

    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            # Lire le contenu ligne par ligne
            for ligne in fichier:
                # Séparer la ligne en mots
                mots = ligne.split()

                # Analyser chaque mot et le classer dans le bon groupe
                for mot in mots:
                    if mot.isalpha():  # Si le mot est composé uniquement de lettres
                        groupes['alpha'].append(mot)
                    elif mot.isdigit():  # Si le mot est composé uniquement de chiffres
                        groupes['numerique'].append(mot)
                    elif re.match(r'^[a-zA-Z0-9]+$', mot):  # Si le mot est alphanumérique
                        groupes['alphanum'].append(mot)
                    else:  # Si le mot contient des caractères spéciaux
                        groupes['autre'].append(mot)

        # Afficher les résultats de classification
        print("Mots alphabétiques (lettres uniquement) :")
        print(groupes['alpha'])
        print("\nMots numériques (chiffres uniquement) :")
        print(groupes['numerique'])
        print("\nMots alphanumériques (lettres et chiffres) :")
        print(groupes['alphanum'])
        print("\nAutres mots (avec symboles spéciaux ou autres caractères) :")
        print(groupes['autre'])

    except FileNotFoundError:
        print(f"Le fichier '{chemin_fichier}' n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Remplacez par le chemin de votre fichier
chemin_fichier = r"C:\Users\userlocal\Desktop\R105\SEA1\test(1).csv"
lire_fichier_et_classer(chemin_fichier)
