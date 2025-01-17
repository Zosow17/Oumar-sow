import csv

# Ouvrir le fichier .ics en mode lecture
try:
    with open('C:/Users/Lenovo/Downloads/evenementSAE_15GroupeA1.ics', 'r', encoding='utf8') as g:
        # Lire le contenu du fichier
        h = g.read()

        # Initialiser les variables pour stocker les informations de l'événement
        uid = ""
        dtstart = ""
        dtend = ""
        summary = ""

        # Parcourir chaque ligne du fichier
        for line in h.split("\n"):
            # Séparer la ligne en deux parties (clé et valeur)
            parts = line.split(":")
            if len(parts) < 2:
                continue  # Ignorer les lignes vides ou mal formatées

            key = parts[0]
            value = ":".join(parts[1:])  # Gérer les valeurs contenant des ":"

            # Extraire les informations de l'événement
            if key == "UID":
                uid = value
            elif key == "DTSTART":
                dtstart = value
            elif key == "DTEND":
                dtend = value
            elif key == "SUMMARY":
                summary = value

        # Créer un tableau avec les informations extraites
        tableau_evnmnt = [uid, dtstart, dtend, summary]
        print(tableau_evnmnt)

        # Écrire les informations dans un fichier CSV
        with open('C:/Users/Lenovo/Downloads/events.csv', 'w', encoding='utf8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            # Écrire l'en-tête du fichier CSV
            writer.writerow(["UID", "DTSTART", "DTEND", "SUMMARY"])
            # Écrire les données de l'événement
            writer.writerow(tableau_evnmnt)

        print("Les données ont été exportées avec succès vers events.csv.")

except FileNotFoundError:
    print(f"Le fichier n'existe pas: C:/Users/Lenovo/Downloads/evenementSAE_15GroupeA1.ics")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")