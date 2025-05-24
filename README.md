# Scraper-RI

## Vue d'ensemble du projet
Ce projet analyse l'OPCVM iShares Core MSCI World UCITS ETF (ISIN: IE0002XZSHO1) en collectant des données historiques et en calculant des indicateurs financiers clés sur différentes périodes temporelles.

## Méthodologie pour la collecte des données
### Sources de données
Le système utilise une approche multi-sources avec fallback automatique :

1. Yahoo Finance API (source principale)
   
   - Symboles testés : IWDA.AS, IWDA.L, IWDA.DE, IWDA.MI
   - Endpoint : https://query1.finance.yahoo.com/v8/finance/chart/
   - Intervalle : données quotidiennes (1d)
   - Période : 3 ans d'historique (1095 jours)
2. Investing.com (source alternative)
   
   - Scraping HTML des données historiques
   - ID ETF : 997650 (IWDA)
   - Format : données quotidiennes
3. Alpha Vantage API (source de secours)
   
   - Fonction : TIME_SERIES_DAILY
   - Symbole : IWDA.LON
   - Nécessite une clé API gratuite
### Processus de collecte
- Période d'analyse : 3 ans d'historique maximum
- Fréquence : Données quotidiennes (prix de clôture)
- Format de stockage : JSON avec structure {date, price, source}
- Gestion d'erreurs : Système de fallback entre sources
- Headers HTTP : Simulation de navigateur pour éviter le blocage
