import matplotlib.pyplot as plt

def detect_anomalies(input_file, output_html="anomalies.html", output_graph="graphe_anomalies.png"):
    """
    Détecte les anomalies dans un fichier texte et génère une page HTML avec les résultats.
    :param input_file: Chemin du fichier d'entrée.
    :param output_html: Chemin du fichier HTML de sortie.
    :param output_graph: Chemin du fichier graphique de sortie.
    """
    try:
        with open(input_file, "r", encoding="utf8") as fichier:
            # Compteurs d'anomalies
            anomaly_counter = 0
            anomaly_types = {
                "Longueur inhabituelle": 0,
                "Drapeau suspect": 0,
                "IP suspecte": 0
            }

            # Parcourir chaque ligne du fichier
            for ligne in fichier:
                ligne = ligne.strip()  # Supprimer les espaces et sauts de ligne
                if not ligne:  # Ignorer les lignes vides
                    continue

                # Séparer la ligne en mots
                split = ligne.split()

                # Filtrer les lignes contenant "IP"
                if "IP" in ligne:
                    # 1. Détection de longueur inhabituelle
                    if "length" in ligne and "HTTP" not in ligne:
                        length_value = split[-1]  # Prendre la dernière valeur
                        length_value = ''.join(filter(str.isdigit, length_value))  # Nettoyer la valeur
                        if length_value:  # Vérifier si la valeur nettoyée n'est pas vide
                            try:
                                length_value = int(length_value)
                                if length_value < 50 or length_value > 1500:  # Exemple de seuils
                                    anomaly_counter += 1
                                    anomaly_types["Longueur inhabituelle"] += 1
                            except ValueError:
                                pass  # Ignorer les erreurs de conversion

                    # 2. Détection de drapeau suspect
                    if "[P.]" in ligne or "[S]" in ligne:  # Exemple de drapeaux suspects
                        anomaly_counter += 1
                        anomaly_types["Drapeau suspect"] += 1

                    # 3. Détection d'IP suspecte
                    if len(split) > 4 and (split[2].startswith("192.168.") or split[4].startswith("192.168.")):
                        anomaly_counter += 1
                        anomaly_types["IP suspecte"] += 1

            # Générer le graphique
            anomaly_labels = list(anomaly_types.keys())
            anomaly_counts = list(anomaly_types.values())
            plt.bar(anomaly_labels, anomaly_counts, color=['red', 'blue', 'green'])
            plt.title('Répartition des anomalies détectées')
            plt.xlabel('Types d\'anomalies')
            plt.ylabel('Nombre d\'anomalies')
            plt.savefig(output_graph)
            plt.close()

            # Créer la page HTML
            htmlcontenu = f'''
            <html>
               <head>
                  <meta charset="utf-8">
                  <title>Traitement des données</title>
                  <style>
                  body {{
                      background-color: #3498DB;
                      font-family: Arial, sans-serif;
                      color: white;
                  }}
                  h2, h3 {{
                      color: #2C3E50;
                  }}
                  </style>
               </head>
               <body>
                   <center><h2>Projet SAE 15</h2></center>
                   <center><p>Sur cette page web, on va vous présenter les anomalies détectées dans le fichier à traiter.</p></center>
                   <center><h3>Anomalies détectées</h3>
                   Nombre total d'anomalies = {anomaly_counter}
                   <br>
                   <img src="{output_graph}" alt="Graphique des anomalies">
               </body>
            </html>
            '''

            # Écrire la page HTML
            with open(output_html, "w", encoding="utf8") as html:
                html.write(htmlcontenu)
                print(f"Page web créée avec succès : {output_html}")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{input_file}' n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Exemple d'utilisation
input_file = "DumpFile.txt"  # Chemin du fichier d'entrée
output_html = "anomalies.html"  # Fichier HTML de sortie
output_graph = "graphe_anomalies.png"  # Fichier graphique de sortie

detect_anomalies(input_file, output_html, output_graph)