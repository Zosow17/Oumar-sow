import csv
import webbrowser
import matplotlib.pyplot as plt
import numpy as np
import html

# Ouvrir et lire le fichier non traité
try:
    with open("DumpFile.txt", "r", encoding="utf8") as fichier:
        # Création des listes pour stocker les données
        ipsr = []  # IP source
        ipde = []  # IP destination
        longueur = []  # Longueur des trames
        flag = []  # Drapeaux
        seq = []  # Numéros de séquence
        heure = []  # Heure des trames

        # Compteurs
        flagcounterP = 0  # Compteur de drapeaux [P]
        flagcounterS = 0  # Compteur de drapeaux [S]
        flagcounter = 0  # Compteur de drapeaux [.]
        framecounter = 0  # Compteur de trames
        requestcounter = 0  # Compteur de requêtes
        replycounter = 0  # Compteur de réponses
        seqcounter = 0  # Compteur de séquences
        ackcounter = 0  # Compteur d'acquittements
        wincounter = 0  # Compteur de fenêtres

        # Parcourir chaque ligne du fichier
        for ligne in fichier:
            # Séparer la ligne en mots
            split = ligne.split(" ")

            # Filtrer les lignes contenant "IP"
            if "IP" in ligne:
                framecounter += 1

                # Remplir la liste des drapeaux
                if "[P.]" in ligne:
                    flag.append("[P.]")
                    flagcounterP += 1
                if "[.]" in ligne:
                    flag.append("[.]")
                    flagcounter += 1
                if "[S]" in ligne:
                    flag.append("[S]")
                    flagcounterS += 1

                # Remplir la liste des séquences
                if "seq" in ligne:
                    seqcounter += 1
                    seq.append(split[8])

                # Compter les fenêtres
                if "win" in ligne:
                    wincounter += 1

                # Compter les acquittements
                if "ack" in ligne:
                    ackcounter += 1

                # Remplir la liste des IP sources
                ipsr.append(split[2])

                # Remplir la liste des IP destinations
                ipde.append(split[4])

                # Remplir la liste des heures
                heure.append(split[0])

                # Remplir la liste des longueurs
                if "length" in ligne:
                    if "HTTP" in ligne:
                        longueur.append(split[-2])
                    else:
                        longueur.append(split[-1])

                # Détecter les requêtes et réponses ICMP
                if "ICMP" in ligne:
                    if "request" in ligne:
                        requestcounter += 1
                    if "reply" in ligne:
                        replycounter += 1

        # Nettoyer les adresses IP sources et destinations
        ipsource2 = []
        ipdesti2 = []
        ipdestifinale = []

        for i in ipsr:
            if not "." in i:
                ipsource2.append(i)
            elif "ssh" in i or len(i) > 15 or "B" in i:
                ports = i.split(".")
                del ports[-1]
                delim = "."
                delim = delim.join(ports)
                ipsource2.append(delim)
            else:
                ipsource2.append(i)

        for j in ipde:
            if not "." in j:
                ipdesti2.append(j)
            elif "ssh" in j or len(j) > 15 or "B" in j:
                ports = j.split(".")
                del ports[-1]
                delim = "."
                delim = delim.join(ports)
                ipdesti2.append(delim)
            else:
                ipdesti2.append(j)

        for l in ipdesti2:
            if not ":" in l:
                ipdestifinale.append(l)
            else:
                deuxp = l.split(":")
                ipdestifinale.append(deuxp[0])

        # Calculer les pourcentages des drapeaux
        globalflagcounter = flagcounter + flagcounterP + flagcounterS
        P = flagcounterP / globalflagcounter
        S = flagcounterS / globalflagcounter
        A = flagcounter / globalflagcounter

        # Calculer les pourcentages des requêtes et réponses
        globalreqrepcounter = replycounter + requestcounter
        req = requestcounter / globalreqrepcounter
        rep = replycounter / globalreqrepcounter

        # Convertir les compteurs en listes pour l'exportation CSV
        flagcounter = [flagcounter]
        flagcounterP = [flagcounterP]
        flagcounterS = [flagcounterS]
        framecounter = [framecounter]
        requestcounter = [requestcounter]
        replycounter = [replycounter]
        seqcounter = [seqcounter]
        ackcounter = [ackcounter]
        wincounter = [wincounter]

        # Créer des graphiques avec matplotlib
        # Graphique circulaire pour les drapeaux
        name = ['Flag [.]', 'Flag [P]', 'Flag [S]']
        data = [A, P, S]
        explode = (0, 0, 0)
        plt.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
        plt.axis('equal')
        plt.savefig("graphe1.png")
        plt.show()

        # Graphique circulaire pour les requêtes et réponses
        name2 = ['Request', 'Reply']
        data2 = [req, rep]
        explode = (0, 0)
        plt.pie(data2, explode=explode, labels=name2, autopct='%1.1f%%', startangle=90, shadow=True)
        plt.savefig("graphe2.png")
        plt.show()

        # Contenu de la page HTML
        htmlcontenu = '''
        <html>
           <head>
              <meta charset="utf-8">
              <title> Traitement des données </title>
              <style>
              body{
                  background-color:#3498DB;
                  }
              </style>
           </head>

           <body>
               <center><h2>Projet SAE 15</h2></center>
               <center><p>Sur cette page web on va vous présenter les informations et données pertinentes qu'on a trouvé dans le fichier à traiter.</p></center>
               <center><h3> Nombre total des trames échangées</h3> %s</center>
               <br>
               <center><h3> Drapeaux (Flags)<h3></center>
               <center>Nombre de flags [P] (PUSH) = %s
               <br>Nombre de flags [S] (SYN) = %s  
               <br>Nombre de flags [.] (ACK) = %s
               <br>
               <br>
               <img src="graphe1.png">
               <h3> Nombre des requêtes et réponses </h3>
               Requêtes = %s 
               <br>
               Réponses = %s
               <br>
               <br>
               <img src="graphe2.png">
               <h3>Statistiques entre seq, win et ack </h3>
               Nombre de seq = %s
               <br>
               Nombre de win = %s
               <br>
               Nombre de ack = %s
           </body>
        </html>
        ''' % (framecounter, flagcounterP, flagcounterS, flagcounter, requestcounter, replycounter, seqcounter, wincounter, ackcounter)

        # Exporter les données dans un fichier CSV
        with open('données.csv', 'w', newline='', encoding="utf8") as fichiercsv:
            writer = csv.writer(fichiercsv)
            writer.writerow(['Heure', 'IP source', 'IP destination', 'Flag', 'Seq', 'Length'])
            writer.writerows(zip(heure, ipsr, ipde, flag, seq, longueur))

        # Exporter les statistiques dans un fichier CSV
        with open('Stats.csv', 'w', newline='', encoding="utf8") as fichier2:
            writer = csv.writer(fichier2)
            writer.writerow(['Flag[P] (PUSH)', 'Flag[S] (SYN)', 'Flag[.] (ACK)', 'Nombre total de trames', "Nombre de requêtes", "Nombre de réponses", "Nombre de séquences", "Nombre d'acquittements", "Nombre de fenêtres"])
            writer.writerows(zip(flagcounterP, flagcounterS, flagcounter, framecounter, requestcounter, replycounter, seqcounter, ackcounter, wincounter))

        # Créer une page HTML avec les informations et statistiques
        with open("data.html", "w", encoding="utf8") as html:
            html.write(htmlcontenu)
            print("Page web créée avec succès.")

except FileNotFoundError:
    print(f"Le fichier n'existe pas: DumpFile.txt")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")