# coding: utf-8

# Ce script vise à récolter des données dans la liste 
# des contrats d'une valeur de 10 000 $ ou plus 
# du Ministère de la Santé du Canada sur le 1er trimestre 2016-2017

# On importe les modules

import csv
import requests
from bs4 import BeautifulSoup

# On insère l'URL de départ

url = "http://www.contracts-contrats.hc-sc.gc.ca/cfob/mssid/contractdisc.nsf/WEBbypurposeF?OpenView&RP=2016-2017~1&Count=3000&lang=fra&#tphp"

# On donne un nom au fichier csv

fichier = "contrats-sante.csv"

# On rédige les entêtes

entetes = {
    "User-Agent":"Jérémy Heintzmann - Pour ramasser des données pour un cours de journalisme à l'UQAM",
    "From":"jeremy.heintzmann@gmail.com"
}

# On crée la variable contenu

contenu = requests.get(url, headers=entetes)

# On crée la variable page, dans laquelle on demande à BeautifulSoup
# de prendre le texte de ce contenu

page = BeautifulSoup(contenu.text,"html.parser")

# print(page)

# On crée une variable compteur afin d'éviter de moissonner
# la première ligne du tableau, qui décrit les colonnes

i = 0

# On utilise une boucle pour consulter chacun des éléments du tableau
# et on recueille les hyperliens qui nous intéressent

for ligne in page.find_all("tr"):
    if i != 0:
        # print(ligne)
        lien = ligne.a.get("href")
        # print(lien)
        hyperlien = "http://www.contracts-contrats.hc-sc.gc.ca/cfob/mssid/contractdisc.nsf/WEBbypurposeF" + lien
        print(hyperlien)
        
# On demande à BeautifulSoup d'aller chercher 
# chacune des pages contenant les détails d'un contrat

        contenu2 = requests.get(hyperlien, headers=entetes)
        page2 = BeautifulSoup(contenu2.text, "html.parser")

# On crée une liste vide dans laquelle on met les infos du contrat

        contrat = []
        
        contrat.append(hyperlien)

# On crée une autre boucle pour aller chercher les données de chaque contrat
        
        for item in page2.find_all("h2","p"):
            # print(item)
            
            if item.p is not None:
                contrat.append(item.p.text)
            else:
                contrat.append(None)
                
        print(contrat)

# On inscrit la liste contrat dans une ligne d'un fichier csv      

        travail = open(fichier,"a")
        careyprice = csv.writer(travail)
        careyprice.writerow(contrat)

# On augmente le compteur de 1

    i =+ 1
