import csv

def writefile(fic, sow, header=None):
    """
    Écrit les données dans un fichier CSV ou Markdown.
    :param fic: Nom du fichier de sortie.
    :param sala: Liste des données à écrire.
    :param header: En-tête pour le fichier CSV (optionnel).
    """
    with open(fic, "w", encoding="utf8", newline='') as file:
        if fic.endswith(".csv"):  # Si c'est un fichier CSV
            csv_writer = csv.writer(file, delimiter=';')
            if header:  # Ajouter l'en-tête si fourni
                csv_writer.writerow(header)
            for frame in sow:
                csv_writer.writerow(frame.split(";"))  # Écrire chaque ligne
        else:  # Si c'est un fichier Markdown ou autre
            for frame in sow:
                file.write(frame + "\n")  # Écrire chaque ligne

def process_file(input_file, output_csv, output_md, filter_string=None):
    """
    Traite un fichier texte, extrait les données et les exporte en CSV et Markdown.
    :param input_file: Chemin du fichier d'entrée.
    :param output_csv: Chemin du fichier CSV de sortie.
    :param output_md: Chemin du fichier Markdown de sortie.
    :param filter_string: Chaîne pour filtrer les lignes (optionnel).
    """
    try:
        with open(input_file, "r", encoding="utf8") as fic:
            # Lire les lignes du fichier
            lines = fic.readlines()

            # Liste pour stocker les données extraites
            ma = []

            # Parcourir chaque ligne du fichier
            for frame in lines:
                frame = frame.strip()  # Supprimer les espaces et sauts de ligne
                if not frame:  # Ignorer les lignes vides
                    continue
                if filter_string and not frame.startswith(filter_string):  # Filtrer les lignes si nécessaire
                    continue

                # Initialiser une liste pour les données extraites
                data = ["."] * 9  # 9 champs : Heure, Protocole, Source, Destination, Flags, Seq, Ack, Win, Length

                # Séparer la ligne en mots
                separateur = frame.split()

                # Remplir les données extraites
                data[0] = separateur[0]  # Heure
                for index, info in enumerate(separateur):
                    if info == "IP":
                        data[1] = info  # Protocole IP
                    if info == ">":
                        data[2] = separateur[index - 1]  # Source (avant ">")
                        data[3] = separateur[index + 1]  # Destination (après ">")
                    if info == "flags":
                        data[4] = separateur[index + 1]  # Flags
                    if info == "seq":
                        data[5] = separateur[index + 1]  # Numéro de séquence (seq)
                    if info == "ack":
                        data[6] = separateur[index + 1]  # Numéro d'acquittement (ack)
                    if info == "win":
                        data[7] = separateur[index + 1]  # Taille de la fenêtre (win)
                    if info == "length":
                        data[8] = separateur[index + 1]  # Longueur (length)

                # Convertir la liste en une ligne CSV séparée par des points-virgules
                csvline = ";".join(data)
                ma.append(csvline)

        # En-tête pour le fichier CSV
        header = ["Heure", "Protocole", "Source", "Destination", "Flags", "Seq", "Ack", "Win", "Length"]

        # Écrire les données dans les fichiers
        writefile(output_csv, ma, header)
        writefile(output_md, ma)

        print(f"Les données ont été exportées avec succès dans {output_csv} et {output_md}.")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{input_file}' n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Exemple d'utilisation
input_file = r"C:\Users\userlocal\Desktop\R105\SEA1\sae105\DumpFile.txt"  # Chemin du fichier d'entrée
output_csv = "extraction3.csv"  # Fichier CSV de sortie
output_md = "markdown.md"  # Fichier Markdown de sortie
filter_string = "11:42"  # Filtrer les lignes commençant par "11:42" (optionnel)

process_file(input_file, output_csv, output_md, filter_string)