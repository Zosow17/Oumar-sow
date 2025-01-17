# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 09:54:13 2023

@author: Lenovo
"""

import os
import csv

try:
    # Ouvrir le fichier texte en mode lecture
    with open("DumpFile.txt", encoding="utf8") as fh:
        res = fh.read()
except FileNotFoundError:
    print(f"Le fichier n'existe pas: {os.path.abspath('DumpFile.txt')}")
    exit(1)  # Quitter le programme si le fichier n'existe pas

# Séparer le contenu du fichier par lignes
ress = res.split('\n')

# Ouvrir le fichier CSV en mode écriture
with open("Salamata.csv", "w", encoding="utf8", newline='') as fic:
    writer = csv.writer(fic, delimiter=';')
    # Écrire l'en-tête du fichier CSV
    writer.writerow(["Heure", "Source", "Port", "Destination", "Flag", "Seq", "Ack", "Win", "Options", "Length"])

    # Parcourir chaque ligne du fichier
    for event in ress:
        if event.startswith('11:42'):  # Filtrer les lignes qui commencent par "11:42"
            # Initialiser les variables
            seq = ""
            heure1 = ""
            nomip = ""
            port = ""
            flag = ""
            ack = ""
            win = ""
            options = ""
            length = ""

            # Extraire l'heure (première colonne)
            texte = event.split(" ")
            heure1 = texte[0]

            # Extraire la source (2ème colonne)
            nomip1 = texte[2].split(".")
            nomip = ".".join(nomip1[:-1])  # Concaténer toutes les parties sauf la dernière (port)

            # Extraire le port
            if len(texte) > 1:
                port1 = texte[2].split(".")
                port = port1[-1]  # Le port est la dernière partie après le point

            # Extraire la destination (3ème colonne)
            nomip2 = texte[4]

            # Extraire le flag
            texte_flag = event.split("[")
            if len(texte_flag) > 1:
                flag1 = texte_flag[1].split("]")
                flag = flag1[0]

            # Extraire le numéro de séquence (Seq)
            texte_seq = event.split(",")
            if len(texte_seq) > 1 and texte_seq[1].startswith(" seq"):
                seq1 = texte_seq[1].split(" ")
                seq = seq1[2]

            # Extraire le numéro d'acquittement (Ack)
            if len(texte_seq) > 2 and texte_seq[2].startswith(" ack"):
                ack1 = texte_seq[2].split(" ")
                ack = ack1[2]
            elif len(texte_seq) > 1 and texte_seq[1].startswith(" ack"):
                ack1 = texte_seq[1].split(" ")
                ack = ack1[2]

            # Extraire la taille de la fenêtre (Win)
            if len(texte_seq) > 3 and texte_seq[3].startswith(" win"):
                win1 = texte_seq[3].split(" ")
                win = win1[2]
            elif len(texte_seq) > 2 and texte_seq[2].startswith(" win"):
                win1 = texte_seq[2].split(" ")
                win = win1[2]

            # Extraire les options
            texte_options = event.split("[")
            if len(texte_options) > 2:
                options1 = texte_options[2].split("]")
                options = options1[0]

            # Extraire la longueur (Length)
            texte_length = event.split("]")
            if len(texte_length) > 2:
                length1 = texte_length[2].split(" ")
                length = length1[2]

            # Gérer le cas où la longueur est spécifiée dans une autre partie
            if len(texte_seq) > 3 and texte_seq[3].startswith(" length"):
                length1 = texte_seq[3].split(" ")
                length = length1[2]
                length = length.replace("characters", "")  # Supprimer le mot "characters"

            # Écrire la ligne dans le fichier CSV
            writer.writerow([heure1, nomip, port, nomip2, flag, seq, ack, win, options, length])

print("Les données ont été exportées avec succès vers Salamata.csv.")