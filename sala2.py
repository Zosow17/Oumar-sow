import re
import pandas as pd
from collections import Counter

# Ouvrir le fichier en mode lecture
try:
    with open('DumpFile.txt', 'r', encoding='utf8') as f:
        # Lire le contenu du fichier
        text = f.read()

        # Compiler l'expression régulière pour détecter les adresses IP
        pattern = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')

        # Trouver toutes les occurrences d'adresses IP dans le contenu
        matches = pattern.findall(text)

        # Utiliser Counter pour compter le nombre d'occurrences de chaque adresse IP
        counts = Counter(matches)

        # Convertir les résultats en DataFrame
        df = pd.DataFrame(counts.items(), columns=['Adresse IP', 'Occurrences'])

        # Enregistrer le DataFrame dans un fichier Excel
        df.to_excel('resultats.xlsx', index=False)

        print("Les données ont été exportées vers le fichier resultats.xlsx")

except FileNotFoundError:
    print(f"Le fichier n'existe pas: {os.path.abspath('DumpFile.txt')}")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")