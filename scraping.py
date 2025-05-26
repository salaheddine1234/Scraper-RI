"""
Scraper pour récupérer les données de l'OPCVM IE0002XZSHO1

"""
import requests
import json
from datetime import datetime, timedelta
import time
import csv

class OPCVMScraper:
    def __init__(self, isin="IE0002XZSHO1"):
        self.isin = isin
        self.session = requests.Session()
        # Headers pour éviter le blocage
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        self.timeout = 15
    
    def scrape_yahoo_finance(self):
        """
        Méthode 1: Yahoo Finance API 
        """
        print("Tentative avec Yahoo Finance...")
        
        # Symboles possibles pour cet ETF
        symbols = ["IWDA.AS", "IWDA.L", "IWDA.DE", "IWDA.MI"]
        
        for symbol in symbols:
            try:
                print(f"   Essai du symbole: {symbol}")
                
                # Récupération des données historiques (3 ans = 1095 jours)
                end_time = int(time.time())
                start_time = int((datetime.now() - timedelta(days=1095)).timestamp())
                
                url = "https://query1.finance.yahoo.com/v8/finance/chart/" + symbol
                params = {
                    'period1': start_time,
                    'period2': end_time,
                    'interval': '1d',
                    'includePrePost': 'false'
                }
                
                response = self.session.get(url, params=params, timeout=self.timeout)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('chart', {}).get('result'):
                        result = data['chart']['result'][0]
                        
                        # Extraction des données
                        timestamps = result.get('timestamp', [])
                        prices_data = result.get('indicators', {}).get('quote', [{}])[0]
                        closes = prices_data.get('close', [])
                        
                        # Formatage des données
                        historical_data = []
                        for i, timestamp in enumerate(timestamps):
                            if i < len(closes) and closes[i] is not None:
                                historical_data.append({
                                    'date': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d'),
                                    'price': round(float(closes[i]), 4),
                                    'source': f'Yahoo Finance ({symbol})'
                                })
                        
                        if historical_data:
                            print(f"Données trouvées: {len(historical_data)} points")
                            print(f"   Période: {historical_data[0]['date']} à {historical_data[-1]['date']}")
                            return historical_data
                
            except Exception as e:
                print(f"   Erreur avec {symbol}: {e}")
                continue
        
        print("Échec Yahoo Finance")
        return None
    
    def scrape_investing_com(self):
        """
        Méthode 2: Investing.com 
        
        """
        print(" Tentative avec Investing.com...")
        
        try:
            # URL pour l'ETF IWDA sur Investing.com
            base_url = "https://www.investing.com/etfs/ishares-msci-world-ucits-etf-dist-historical-data"
            
            headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': base_url
            }
            
            # Paramètres pour récupérer les données historiques 
            data = {
                'curr_id': '997650',  # ID de l'ETF IWDA
                'smlID': '300004',
                'header': 'IWDA Historical Data',
                'st_date': (datetime.now() - timedelta(days=1095)).strftime('%m/%d/%Y'),
                'end_date': datetime.now().strftime('%m/%d/%Y'),
                'interval_sec': 'Daily',
                'sort_col': 'date',
                'sort_ord': 'DESC',
                'action': 'historical_data'
            }
            
            response = self.session.post(
                "https://www.investing.com/instruments/HistoricalDataAjax",
                data=data,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                # Parse HTML response (simplifié)
                content = response.text
                if 'table' in content and 'data-test="historical-data-table"' in content:
                    print("Données HTML récupérées d'Investing.com")
                    # Ici on pourrait parser le HTML, mais c'est plus complexe
                    return []
            
        except Exception as e:
            print(f"Erreur Investing.com: {e}")
        
        return None
    
    
    def get_fund_info(self):
        """
        Récupère les informations de base du fonds
        """
        
        fund_info = {
            'isin': self.isin,
            'nom': 'iShares Core MSCI World UCITS ETF',
            'ticker_principal': 'IWDA',
            'gestionnaire': 'BlackRock',
            'type': 'ETF',
            'devise_base': 'USD',
            'periode_historique': '3 ans',
            'date_recuperation': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return fund_info
    
    def scrape_all_sources(self):
        """
        Essaie toutes les sources et retourne la première qui fonctionne
        """
        print(f"Début du scraping pour l'ISIN: {self.isin}")
        print("="*60)
        
        # Informations du fonds
        fund_info = self.get_fund_info()
        
        # Essai des différentes sources
        sources = [
            self.scrape_yahoo_finance,
            self.scrape_investing_com
        ]
        
        for source_func in sources:
            try:
                data = source_func()
                if data and len(data) > 10:  # Au moins 10 points de données
                    # Vérification de la période couverte
                    dates = [datetime.strptime(d['date'], '%Y-%m-%d') for d in data]
                    oldest_date = min(dates)
                    newest_date = max(dates)
                    period_covered = (newest_date - oldest_date).days
                    
                    print(f"Scraping réussi!")
                    print(f"Période couverte: {period_covered} jours ({period_covered/365:.1f} ans)")
                    
                    return {
                        'fund_info': fund_info,
                        'historical_data': sorted(data, key=lambda x: x['date']),
                        'date_debut': oldest_date.strftime('%Y-%m-%d'),
                        'date_fin': newest_date.strftime('%Y-%m-%d'),
                        'periode_jours': period_covered,
                        'periode_annees': round(period_covered/365, 1)
                    }
            except Exception as e:
                print(f"Erreur avec une source: {e}")
                continue
        
        print("Échec de toutes les sources")
        return None
    
    def save_to_csv(self, result, filename="opcvm_data.csv"):
        """
        Sauvegarde les données en CSV
        """
        if not result or not result.get('historical_data'):
            print("Aucune donnée à sauvegarder")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['date', 'price', 'source']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for row in result['historical_data']:
                    writer.writerow(row)
            
            print(f"Données sauvées dans {filename}")
            
        except Exception as e:
            print(f"Erreur sauvegarde CSV: {e}")
    
    def save_to_json(self, result, filename="opcvm_data.json"):
        """
        Sauvegarde les données en JSON
        """
        if not result:
            print("Aucune donnée à sauvegarder")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(result, jsonfile, indent=2, ensure_ascii=False)
            
            print(f"Données enregsitées dans {filename}")
            
        except Exception as e:
            print(f"Erreur sauvegarde JSON: {e}")

def main():
    """
    Fonction principale de test
    """
    print("SCRAPER OPCVM")
    print("="*60)
    
    # Création du scraper
    scraper = OPCVMScraper("IE0002XZSHO1")
    
    # Scraping des données
    result = scraper.scrape_all_sources()
    
    if result:
        print("\n RÉSULTATS:")
        print(f"   Fonds: {result['fund_info']['nom']}")
        print(f"   ISIN: {result['fund_info']['isin']}")
        print(f"   Période: {result['date_debut']} à {result['date_fin']}")
        print(f"   Durée: {result['periode_jours']} jours ({result['periode_annees']} ans)")
        print(f"   Source: {result['historical_data'][0]['source']}")
        
        
        # Sauvegarde
        scraper.save_to_csv(result)
        scraper.save_to_json(result)
        
        print("\n Scraping terminé avec succès!")
        
    else:
        print("\n Impossible de récupérer les données")

if __name__ == "__main__":
    main()