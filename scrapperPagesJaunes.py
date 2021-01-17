
#!/usr/bin/python3
# coding: utf-8
 
import requests
import csv
from lxml import html
import datetime
import argparse
import time
 



def cleanListOutput(listOutput):
    """
    nettoie la liste sortie afin de supprimer les caractères spéciaux \xa0 et \n.
    Supprime également les champs vides dans la liste
    """
    cleanListOutput=[]
    for output in listOutput:
        output = output.replace(u'\xa0', u' ')
        output = output.replace(u'\n', u' ')

        if output!="" and output!=" ":
            cleanListOutput.append(output)
    return (', '.join(cleanListOutput))


def sepMotscles(mots_cles,sep):
    """
    transforme la chaine en entrée en remplaçant les espaces par le séparateur donné en entrée 
    """
    return mots_cles.replace(u' ', sep)

def cleanSiteOutput(listOutput):
    """
    nettoie la liste de sites de sortie afin de supprimer les caractères spéciaux et d'enlever les parties qui ne correspondent pas à l'url du site.
    Supprime également les champs vides dans la liste
    """
    cleanListOutput=[]
    for output in listOutput:
        output = output.replace(u'\xa0', u' ')
        output = output.replace(u'\n', u' ')
        output = output.replace(u'Accéder à', u'')
        output = output.replace(u'nouvelle fenêtre', u'')
        if output!="" and output!=" ":
            cleanListOutput.append(output)
    return (', '.join(cleanListOutput))

def extract(mots_cles, path):
 
    """
    Export all Name/Phone from a (french) PagesJaunes Web Page
 
    Arguments:
         url (str):
            url of the aimed PagesJaunes Web Page
        path (str):
            path to the repository to save the .csv
 
    Return:
        .csv file
    """
 
    # INITIALISATION
    r = requests.session()
    start = datetime.datetime.now()
 
    # COLLECTE DU CODE SOURCE
 
    # on modifie les headers
    headers = {'Host': 'www.pagesjaunes.fr',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.pagesjaunes.fr/',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': '379',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
               }
 
    # url de pages jaunes
    baseUrl = "https://www.pagesjaunes.fr/recherche/departement/"
    endUrl = "&univers=pagesjaunes&idOu="
    
    # Liste des départements où effectuer la recherche
    liste_departement =[{'dep':'ain-01','nb_dep':'1'},{'dep':'aisne-02','nb_dep':'2'},{'dep':'allier-03','nb_dep':'3'}] 

    # CREATION DU CSV
    with open(path + '/extract.csv', "w",newline='') as f:
        fieldnames = ['Name', 'Phone','Site', 'Adresse', 'Activité']
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
    
        # scrapping de tous les départements de la liste
        for departement in liste_departement:
            # formation de l'url du département 
            url_departement = baseUrl + departement['dep'] + '/' + sepMotscles(mots_cles,"-") + "?quoiqui=" + sepMotscles(mots_cles,"+") + "&ou=" + departement['nb_dep'] +endUrl
            articles = ["begin"]
            page=1
            url = url_departement
        
        # recherche sur toutes les pages du département 
            while articles!=[]:
                #time.sleep(0.5)
                response = r.post(url=url)
                print('-- URL --')
                print(url)
                print("-- STATUS CODE --")
                print(response.status_code)
                tree = html.fromstring(response.text)
                articles = tree.xpath("//li[contains(@id, 'bi-bloc-')]")

                for article in articles:
                    # Parsing des différents champs
                    name = article.xpath(".//a[@class='denomination-links pj-lb pj-link']/text()")
                    phone = article.xpath(".//strong[@class='num']/text()")
                    adresse = article.xpath(".//a[@class='adresse pj-lb pj-link']/text()")
                    activite = article.xpath(".//a[@class='activites pj-lb pj-link']/text()")
                    site = article.xpath(".//li[@class='bi-site-internet']//a[@class='pj-lb pj-link']/@title")

                    # certains noms ne sont pas dans la même balise, il faut donc les récupérer différement
                    if name==[]:
                        name = article.xpath(".//a[@class='denomination-links pj-link']/text()")
                    
                    # de même pour les sites
                    if site ==[]:
                        hrefsite = article.xpath(".//li[@class='item hidden-phone site-internet SEL-internet']//a[@class='pj-lb pj-link']/@href")
                        if hrefsite !=[] and hrefsite!=['#']:
                            site = hrefsite

                    values = [cleanListOutput(name), cleanListOutput(phone), cleanSiteOutput(site), cleanListOutput(adresse), cleanListOutput(activite)]
                    dict_row = dict(zip(fieldnames, values))
                    writer.writerow(dict_row)
                page+=1
                url = url_departement+"&page="+str(page)

 
    # TEMPS PASSE
    end = datetime.datetime.now()
    time_elapsed = str(end-start)
    print('\n')
    print('-- TIME ELAPSED --')
    print(time_elapsed)
 
 
if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('url', help='PagesJaunes URLs')
    argparser.add_argument('path', help='Path to csv')
 
    args = argparser.parse_args()
    # URL
    mots_cles = args.url
    # CHEMIN DE SAUVEGARDE DU CSV P
    path = args.path
 
    # ON LANCE LA FONCTION
    extract(mots_cles, path)