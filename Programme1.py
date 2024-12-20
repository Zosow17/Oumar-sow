import re
from collections import Counter

# Étape 1 : Lecture du fichier
def lire_fichier(C:\Users\userlocal\Desktop\R105\SEA1\evenementSAE_15.ics):
    with open(C:\Users\userlocal\Desktop\R105\SEA1\evenementSAE_15.ics 'r', encoding='utf-8') as fichier:
        return fichier.readlines()

# Étape 2 : Extraction des données utiles
def extraire_erreurs(lignes):
    erreurs = []
    pattern = r"(ERROR|FAIL|TIMEOUT|connection refused)"
    for ligne in lignes:
        if re.search(pattern, ligne, re.IGNORECASE):
            erreurs.append(ligne)
    return erreurs

# Étape 3 : Analyse des données
def analyser_erreurs(erreurs):
    types_erreurs = Counter()
    for erreur in erreurs:
        if "timeout" in erreur.lower():
            types_erreurs["Timeout"] += 1
        elif "connection refused" in erreur.lower():
            types_erreurs["Connection Refused"] += 1
        else:
            types_erreurs["Autres Erreurs"] += 1
    return types_erreurs

# Étape 4 : Générer un rapport
def generer_rapport(erreurs, types_erreurs):
    print("=== Rapport d'erreurs ===")
    print(f"Total des erreurs détectées : {len(erreurs)}")
    print("Détails :")
    for type_erreur, count in types_erreurs.items():
        print(f"- {type_erreur} : {count}")
    print("\nErreurs identifiées :")
    for erreur in erreurs[:5]:  # Afficher les 5 premières erreurs pour exemple
        print(f"- {erreur.strip()}")

# Utilisation du script
chemin_fichier = "logs_reseau.txt"
lignes = lire_fichier(chemin_fichier)
erreurs = extraire_erreurs(lignes)
types_erreurs = analyser_erreurs(erreurs)
generer_rapport(erreurs, types_erreurs)
