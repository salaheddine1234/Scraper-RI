# Scraper-RI

## Description
Analyse automatisée de la performance d’un OPCVM sur 3 ans à partir de données financières récupérées en ligne.

## Fonctionnement
1. Collecte : Téléchargement de l’historique des prix via Yahoo Finance.
2. Calculs : Application des formules suivantes :
   - Performance (%) : ![equation](https://latex.codecogs.com/svg.latex?\text{Perf}%20=%20\frac{\text{Prix%20final}%20-%20\text{Prix%20initial}}{\text{Prix%20initial}}%20\times%20100)

   - Rendement quotidien : ![equation](https://latex.codecogs.com/svg.latex?r_t%20=%20%5Cfrac%7BP_t%7D%7BP_%7Bt-1%7D%7D%20-%201)
   - Volatilité annualisée (%) : ![equation](https://latex.codecogs.com/svg.latex?%5Csigma_%7Bann%7D%20=%20%5Ctext%7B%C3%89cart-type%7D(r)%20%5Ctimes%20%5Csqrt%7B252%7D%20%5Ctimes%20100)
   - Rendement espéré annualisé (%) : ![equation](https://latex.codecogs.com/svg.latex?%5Cmu_%7Bann%7D%20=%20%5Ctext%7BMoyenne%7D(r)%20%5Ctimes%20252%20%5Ctimes%20100)
   - Max Drawdown (%) : ![equation](https://latex.codecogs.com/svg.latex?%5Cmax%5Cleft(%5Cfrac%7B%5Ctext%7BCreux%7D%20-%20%5Ctext%7BPic%7D%7D%7B%5Ctext%7BPic%7D%7D%5Cright)%20%5Ctimes%20100)
3. Rapport : Résultats affichés, exportables en CSV/JSON.
## Fichiers
- scraping.py : Collecte des données.
- calcul.py : Calcul des indicateurs.
- analyse.py : Orchestration du processus.
- requirements.txt : Dépendances Python

## Limitations éventuelles
### Qualité des données
- Dépendance aux APIs externes : Risque d'indisponibilité ou de changement de format
- Symboles multiples : L'ETF est coté sur plusieurs bourses, risque de divergence de prix

### Fréquence et actualisation
- Pas de mise à jour automatique : Nécessite une exécution manuelle du script
- Limites API : Yahoo Finance peut limiter le nombre de requêtes


