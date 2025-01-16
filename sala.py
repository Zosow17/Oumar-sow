# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 09:54:13 2023

@author: Lenovo
"""

import numpy as np
import datetime
import os
import csv
import typing

try:
    with open("DumpFile.txt", encoding="utf8") as fh:
        res=fh.read()
except:
        print("Le fichier n'existe pas %s", os.path.abspath('fichieratraiter.txt'))
ress=res.split('\n')

tableau_evenements=np.array([])
fic=open("Salamata.csv", "w")#test est le fichier d'arrivée des extractions
#définir une variable avec le caractère ":" (qui nous sera utile pour la suite)
for event in ress:
        if event.startswith('11:42'): #évenement qui commence par "11:42" (ils commencent tous par 11:42)
            #déclaration variables et remise à zéro
            seq = ""
            heure1 = ""
            nomip = ""
            port = ""
            flag = ""
            ack = ""
            win = ""
            options = ""
            length = ""
            #Pour la date de l'évenement (première colonne)
            texte=event.split(" ")
            heure1=texte[0]
            #Pour la source (2ème colonne) 
            texte=event.split(" ")
            nomip1=texte[2].split(".")
            if len(nomip1) == 2:
                nomip=nomip1[0]
            if len(nomip1) == 3:
                nomip=nomip1[0]+ "." +nomip1[1]
            if len(nomip1) == 4:
                nomip=nomip1[0]+ "." +nomip1[1]+ "." +nomip1[2] 
            if len(nomip1) == 5:
                nomip=nomip1[0]+ "." +nomip1[1]+ "." +nomip1[2]+ "." +nomip1[3]
            if len(nomip1) == 6:
                nomip=nomip1[0]+ "." +nomip1[1]+ "." +nomip1[2]+ "."+nomip1[3]+"."+ nomip1[4]
            #port
            if len(texte) > 1: 
                port1=texte[2].split(".")
                port=port1[-1]
            #Pour la destination (3ème colonne)
            texte=event.split(" ")
            nomip2=texte[4]
            # Flag
            texte=event.split("[") #On coupe à partir du crochet
            if len(texte) > 1: #s'il y a plus de une partie à partir du crochet
                flag1=texte[1].split("]") #on prend après le premier crochet et on coupe au deuxième crochet
                flag=flag1[0]#pourquoi 0 ? Car on prend la partie de gauche du deuxième crochet (ce qu'on recherche)
            #seq
            texte=event.split(",")#on coupe à la virgule
            if len(texte) > 1: #s'il y a plus de 1 partie à partir du crochet
                if texte[1].startswith(" seq"): #Si le texte [1] commence par " seq"
                    seq1=texte[1].split(" ") #on coupe à l'espace et on prend le texte juste après
                    seq=seq1[2] #On a 2 parties entre le split ',' et ce que je recherche
            #ack
            if len(texte) > 2: #
                if texte[2].startswith(" ack"): #Si le texte [2] commence par "ack"
                    ack1=texte[2].split(" ") #on coupe à l'espace et on prend le texte juste après
                    ack=ack1[2] #On a 2 parties entre le split ',' et ce que je recherche
                #si la partie "seq" est absente :
                if texte[1].startswith(" ack"): #Si le texte [1] commence par " ack"
                    ack1=texte[1].split(" ") #on coupe à l'espace et on prend le texte juste après
                    ack=ack1[2] #On a 2 parties entre le split ',' et ce que je recherche
            #win
            if len(texte) > 3: #si le nombre de partie est supérieur à 3
                #si "ack" est présent 
                if texte[3].startswith(" win"): #Si le texte [3] commence par " win"
                    win1=texte[3].split(" ") #on coupe à l'espace et on prend le texte juste après
                    win=win1[2] #On prend le texte après l'espace (la partie qu'on retrouvera dans le tableau)
                #si "ack" n'est pas présent
                if texte[2].startswith(" win"): #Si le texte [2] commence par " win"
                    win1=texte[2].split(" ") #on coupe à l'espace et on prend le texte juste après
                    win=win1[2]#On prend le texte après l'espace (la partie qu'on retrouvera dans le tableau
            #options
            texte=event.split("[") #On coupe à partir du crochet
            if len(texte) > 2: #
                options1=texte[2].split("]") #On part du premier "[" et on a texte [2] pour arriver à ce qu'on souhaite récupérer 
                options=options1[0]#pourquoi 0 ? Car on prend la partie à gauche du deuxième crochet "]"
            
            #length (avec option)
            texte=event.split("]") 
            if len(texte) > 2: #vérifier le nombre de partie (split au crochet)
                    length1=texte[2].split(" ") #on part du premier "[" et ce qu'on recherche est bien dans texte [2]. On split à l'espace pour avoir que le nombre
                    length=length1[2] #On veut bien le "2" pour avoir que le nombre (il y a une partie avant l'espace + une autre après).
            #length (sans option)
            texte=event.split(",")
            if len(texte) > 3:
                if texte[3].startswith(" length"): #Si ça commence par " length" et on recherche dans le texte [3]
                    length1=texte[3].split(" ") #on coupe à l'espace
                    length=length1[2] ##On veut bien le "2" pour avoir que le nombre (texte [1] avant l'espace c'est le mot "length").
                    length = length.replace(characters,"")#remplacement du "characters" en " " (pour éviter que le tableur écrit sous forme de date)
            if event.startswith("11:42:55.536521") : #dès que le programme arrive à la dernière ligne du fichier texte
                prog=0 #il ne fait plus de tour, il s'arrete
            evenement=heure1+";"+nomip+ ";" +port+ ";" + nomip2+ ";"+flag+ ";" +seq+ ";" +ack+ ";" +win+ ";" +options+ ";" +length
            fic.write(evenement + "\n") #on écrire "evenement" dans le csv et \n pour revenir à la ligne (pour ne pas écrire sur la même ligne)
fic.close()
