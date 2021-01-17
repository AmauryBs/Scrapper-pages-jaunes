# Scrapper-pages-jaunes
Petit programme permettant de scrapper le site des  pages jaunes afin de récupérer différents champs. Le programme récupères toutes les pages de la recherche et peut être lancé sur plusieurs département.  

# Sources
Je suis parti de ce tuto que j'ai amélioré et réadapté: https://lobstr.io/index.php/2018/11/21/comment-scraper-les-coordonnees-sur-pagesjaunes-fr-avec-python-3-et-requests/

# Lancement
Pour lancer il suffit de se mettre dans une console et de faire:  ```python .\scrapperPajesJaunes.py "poids lourds" ./ ```
Le premier paramètre correspond au mot clé recherché et le deuxième au chemin ou le csv sera enregistré.

# Changement de département
il suffit de rajouter des département en gardant la même syntaxe que ci-dessous dans le fichier scrapperPajesJaunes.py  
    ```python
        liste_departement =[{'dep':'ain-01','nb_dep':'1'},{'dep':'aisne-02','nb_dep':'2'}]
    ```
