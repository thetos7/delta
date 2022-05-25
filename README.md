# Δelta δata

### Analyse de données ouvertes

L'exercice consiste à prendre des données ouvertes et à les mettre en forme pour aider à l'analyse. Cela peut se faire sous forme d'articles avec des graphiques (voir les feuilles Jupyter dans le dépôt) ou de graphiques interactifs (voir  https://delta.lrde.epita.fr/).

### Code source

Ce dépôt GitHub propose des pages Jupyter et des service Dash pour analyser des données ouvertes. Les sous-dépôts sont :

* [Natalité / revenus](https://github.com/oricou/delta/tree/main/population) : exemple classique qui montre la chute de natalité à travers le monde et la croissance des revenus
* [Prix de l'énergie](https://github.com/oricou/delta/tree/main/energies) : compare le prix grand public de différentes énergies en France

Note : le choix du français est volontaire, il s'agit de promouvoir l'usage
       des données ouvertes auprès du grand public en France. Cela étant il
       est possible d'en faire une version dans une autre langue.


### Données pour la partie cancer

Les données que nous récupérons dans la partie cancer proviennent du site https://ci5.iarc.fr/CI5I-X/Default.aspx CI5 pour Cancer Incidence in 5 Continents et IARC pour International Agency for Research on Cancer.
On trouve les CSV que nous avons utilisés en suivant ce lien https://ci5.iarc.fr/CI5I-X/Pages/download.aspx (le volume X en cliquant sur le lien 'detailed data').
Ces CSV, bien que très complets, était très codifiés. En effet, chaque fichier était nommé avec un identifiant à 8 chiffres, qui correspondaient en fait à des zones géographiques qui était répertoriées dans un fichier texte. Pour simplifier notre tâche, nous avons créé à la main un nouveau dossier CI5_treated_data contenant des sous-dossiers nommés selon les différents continents. Chaque sous-dossier contient lui-même de nombreux sous-dossiers correspondants aux pays du continent en question. Nous avons alors copié chaque CSV dans le sous-dossier de pays qui le concernait selon sa zone géographique.
Cela nous a été très utile car nous voulions dans notre dataset global l'information du continent mais également du pays, pour pouvoir ensuite filtrer selon ses composantes-là.