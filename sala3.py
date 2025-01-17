import csv

# Ouvrir le fichier texte en mode lecture
try:
    with open(r"C:\Users\userlocal\Desktop\R105\SEA1\sae105/DumpFile.txt", "r", encoding="utf8") as fic:
        # Lire les lignes du fichier et les stocker dans une liste
        lines = fic.read()
        resultat = lines.split('\n')

        # Liste pour stocker les données extraites
        ma = []

        # Parcourir chaque ligne du fichier
        for frame in resultat:
            if frame.startswith("11:42"):  # Filtrer les lignes qui commencent par "11:42"
                data = ["."] * 13  # Initialiser une liste de 13 éléments avec des points par défaut

                # Séparer la ligne en mots
                separateur = frame.split(" ")

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

    # Fonction pour écrire les données dans un fichier
    def writefile(fic, sala):
        with open(fic, "w", encoding="utf8", newline='') as file:
            if fic.endswith(".csv"):  # Si c'est un fichier CSV
                csv_writer = csv.writer(file, delimiter=';')
                csv_writer.writerow(["Heure", "Protocole", "Source", "Destination", "Flags", "Seq", "Ack", "Win", "Length"])  # En-tête
                for frame in sala:
                    csv_writer.writerow(frame.split(";"))  # Écrire chaque ligne
            else:  # Si c'est un fichier Markdown ou autre
                for frame in sala:
                    file.write(frame + "\n")  # Écrire chaque ligne

    # Écrire les données dans les fichiers
    writefile("extraction3.csv", ma)
    writefile("markdown3.md", ma)

    print("Les données ont été exportées avec succès.")

except FileNotFoundError:
    print(f"Le fichier n'existe pas: C:/Users/Lenovo/PycharmProjects/HELLO WORLD/DumpFile.txt")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")