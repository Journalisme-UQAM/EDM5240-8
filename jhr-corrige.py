# coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup

url = "http://www.contracts-contrats.hc-sc.gc.ca/cfob/mssid/contractdisc.nsf/WEBbypurposeF?OpenView&RP=2016-2017~1&Count=3000&lang=fra&#tphp"
fichier = "contrats-sante-JHR.csv"

entetes = {
    "User-Agent":"Jérémy Heintzmann - Pour ramasser des données pour un cours de journalisme à l'UQAM",
    "From":"jeremy.heintzmann@gmail.com"
}

contenu = requests.get(url, headers=entetes)
page = BeautifulSoup(contenu.text,"html.parser")

i = 0

for ligne in page.find_all("tr"):
    if i != 0:
        # print(ligne)
        lien = ligne.a.get("href")
        # print(lien)
        # hyperlien = "http://www.contracts-contrats.hc-sc.gc.ca/cfob/mssid/contractdisc.nsf/WEBbypurposeF" + lien # Ici, tu construis des hyperliens trop longs. La variable «lien» commence par «/cfob/mssid/...»; il suffit alors de la précéder par «http://www.contracts-contrats.hc-sc.gc.ca» pour construire la variable hyperlien
        hyperlien = "http://www.contracts-contrats.hc-sc.gc.ca" + lien
        # print(hyperlien)

        contenu2 = requests.get(hyperlien, headers=entetes)
        page2 = BeautifulSoup(contenu2.text, "html.parser")

        contrat = []
        contrat.append(hyperlien)

# Jusqu'ici, ton script fonctionne bien.
# Pour la suite, il ne moissonne plus rien, ce qui fait que le CSV produit ne contient que des URL des pages de contrats.
# Le site que tu as choisi est construit différemment de celui que je vous ai montré.
# Je vois que tu as examiné le code HTML puisque tu cherches à recueillir ce qui se trouve dans des éléments <p>.
# Alors ici, il faut d'abord recueillir seulement les <p> qui nous intéressent.

# Pour y parvenir, la formule est un peu plus compliquée.
# Les <p> qui nous intéressent se trouvent à l'intérieur d'un élément <div>, lui même se trouvant après un élément <div> avec un 'id' appelé "tools"
# La ligne suivante va donc chercher dans «page2» ce <div> dont le 'id' est égal à "tools", puis trouve le <div> suivant avec la méthode «.find_next», puis, là, recueille tous les <p> qui s'y trouvent avec la méthode «.find_all»
        for item in page2.find("div", id="tools").find_next("div").find_all("p"):
            # print(item.text)
            # J'ai adapté la condition suivante
            if item is not None:
                contrat.append(item.text)
            else:
                contrat.append(None)

        print(contrat)

        travail = open(fichier,"a")
        careyprice = csv.writer(travail)
        careyprice.writerow(contrat)

# Dans un des scripts que je vous ai envoyés, j'ai fait une erreur.
# Quand on écrit « =+1 », on dit «la variable est égale à (plus) 1».
# C'est « +=1 » qu'il faut écrire pour augmenter de 1 la valeur d'une variable dans une boucle.
    # i =+ 1
    i += 1