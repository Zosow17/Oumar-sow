import re
import pandas as pd
from collections import Counter
# Ouvrir le fichier en mode lecture
with open('DumpFile.txt', 'r') as f:
    # Lire le contenu du fichier
    text = f.read()
    # Compiler l'expression régulière pour détecter les adresses IP
    pattern = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
    # Trouver toutes les occurences d'adresses IP dans le contenu
    matches = pattern.findall(text)
    # Utiliser Counter pour compter le nombre d'occurrences de chaque adresse IP
    counts = dict(Counter(matches))
    # Convertir les résultats en DataFrame
    df = pd.DataFrame(counts.items(), columns=['Adresse IP', 'Occurences'])
    # Enregistrer le DataFrame dans un fichier Excel
    df.to_excel('resultats.xlsx', index=False)
    print("Les données ont été exportées vers le fichier resultats.xlsx")

