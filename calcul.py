"""
Calculateur de métriques financières pour OPCVM
Calcule Performance, Volatilité, Rendement espéré et Max Drawdown
"""
import json
import csv
from datetime import datetime, timedelta
import math

class FinancialCalculator:
    def __init__(self, data):
        """
        Initialise le calculateur avec les données historiques
        data: liste de dictionnaires avec 'date' et 'price'
        """
        if not data:
            raise ValueError("Aucune donnée fournie")
        
        # Conversion des dates si nécessaire et tri
        self.data = []
        for item in data:
            if isinstance(item['date'], str):
                date_obj = datetime.strptime(item['date'], '%Y-%m-%d')
            else:
                date_obj = item['date']
            
            self.data.append({
                'date': date_obj,
                'price': float(item['price'])
            })
        
        # Tri par date croissante
        self.data.sort(key=lambda x: x['date'])
        
        print(f"📊 Données chargées: {len(self.data)} points")
        print(f"   Période: {self.data[0]['date'].strftime('%Y-%m-%d')} → {self.data[-1]['date'].strftime('%Y-%m-%d')}")
    
    def get_period_dates(self):
        """
        Définit les dates de début pour chaque période d'analyse
        """
        today = datetime.now()
        current_year = today.year
        
        periods = {
            'YTD': datetime(current_year, 1, 1),        # Début d'année
            '3M': today - timedelta(days=90),           # 3 mois
            '6M': today - timedelta(days=180),          # 6 mois
            '1Y': today - timedelta(days=365),          # 1 an
            '3Y': today - timedelta(days=1095)          # 3 ans
        }
        
        return periods
    
    def filter_data_by_period(self, start_date):
        """
        Filtre les données à partir d'une date de début
        """
        filtered = [item for item in self.data if item['date'] >= start_date]
        return filtered
    
    def calculate_performance(self, period_data):
        """
        Calcule la performance totale en pourcentage
        Performance = ((Prix_final / Prix_initial) - 1) × 100
        """
        if len(period_data) < 2:
            return 0.0
        
        prix_initial = period_data[0]['price']
        prix_final = period_data[-1]['price']
        
        if prix_initial <= 0:
            return 0.0
        
        performance = ((prix_final / prix_initial) - 1) * 100
        return round(performance, 2)
    
    def calculate_daily_returns(self, period_data):
        """
        Calcule les rendements quotidiens
        """
        if len(period_data) < 2:
            return []
        
        daily_returns = []
        for i in range(1, len(period_data)):
            prix_precedent = period_data[i-1]['price']
            prix_actuel = period_data[i]['price']
            
            if prix_precedent > 0:
                rendement = (prix_actuel / prix_precedent) - 1
                daily_returns.append(rendement)
        
        return daily_returns
    
    def calculate_volatility(self, period_data):
        """
        Calcule la volatilité annualisée en pourcentage
        Volatilité = Écart-type des rendements quotidiens × √252 × 100
        (252 = nombre de jours de trading par an)
        """
        daily_returns = self.calculate_daily_returns(period_data)
        
        if len(daily_returns) < 2:
            return 0.0
        
        # Calcul de l'écart-type
        moyenne = sum(daily_returns) / len(daily_returns)
        variance = sum((r - moyenne) ** 2 for r in daily_returns) / len(daily_returns)
        ecart_type = math.sqrt(variance)
        
        # Annualisation (252 jours de trading)
        volatilite_annualisee = ecart_type * math.sqrt(252) * 100
        
        return round(volatilite_annualisee, 2)
    
    def calculate_expected_return(self, period_data):
        """
        Calcule le rendement espéré annualisé en pourcentage
        Rendement espéré = Moyenne des rendements quotidiens × 252 × 100
        """
        daily_returns = self.calculate_daily_returns(period_data)
        
        if len(daily_returns) == 0:
            return 0.0
        
        # Moyenne des rendements quotidiens
        moyenne_quotidienne = sum(daily_returns) / len(daily_returns)
        
        # Annualisation
        rendement_espere_annuel = moyenne_quotidienne * 252 * 100
        
        return round(rendement_espere_annuel, 2)
    
    def calculate_max_drawdown(self, period_data):
        """
        Calcule le Maximum Drawdown en pourcentage
        Max DD = Plus grande baisse depuis un pic précédent
        """
        if len(period_data) < 2:
            return 0.0
        
        prices = [item['price'] for item in period_data]
        
        # Calcul du drawdown à chaque point
        peak = prices[0]  # Premier pic
        max_drawdown = 0.0
        
        for price in prices:
            # Nouveau pic
            if price > peak:
                peak = price
            
            # Calcul du drawdown actuel
            current_drawdown = ((price / peak) - 1) * 100
            
            # Mise à jour du max drawdown (plus négatif)
            if current_drawdown < max_drawdown:
                max_drawdown = current_drawdown
        
        return round(max_drawdown, 2)
    
    def analyze_period(self, period_name, start_date):
        """
        Analyse complète d'une période
        """
        print(f"   📈 Analyse {period_name}...")
        
        # Filtrage des données
        period_data = self.filter_data_by_period(start_date)
        
        if len(period_data) < 2:
            print(f"      ⚠️  Données insuffisantes pour {period_name}")
            return None
        
        # Calcul des métriques
        metrics = {
            'performance': self.calculate_performance(period_data),
            'volatilite': self.calculate_volatility(period_data),
            'rendement_espere': self.calculate_expected_return(period_data),
            'max_drawdown': self.calculate_max_drawdown(period_data)
        }
        
        # Informations complémentaires
        metrics.update({
            'nb_points': len(period_data),
            'date_debut': period_data[0]['date'].strftime('%Y-%m-%d'),
            'date_fin': period_data[-1]['date'].strftime('%Y-%m-%d'),
            'prix_debut': round(period_data[0]['price'], 2),
            'prix_fin': round(period_data[-1]['price'], 2)
        })
        
        return metrics
    
    def analyze_all_periods(self):
        """
        Analyse toutes les périodes définies
        """
        print("🔬 DÉBUT DE L'ANALYSE FINANCIÈRE")
        print("=" * 50)
        
        periods = self.get_period_dates()
        results = {}
        
        for period_name, start_date in periods.items():
            metrics = self.analyze_period(period_name, start_date)
            
            if metrics:
                results[period_name] = metrics
                print(f"      ✅ Performance: {metrics['performance']:.2f}%")
                print(f"      ✅ Volatilité: {metrics['volatilite']:.2f}%")
                print(f"      ✅ Rendement espéré: {metrics['rendement_espere']:.2f}%")
                print(f"      ✅ Max Drawdown: {metrics['max_drawdown']:.2f}%")
                print()
        
        return results
    
    def display_results_table(self, results):
        """
        Affiche les résultats sous forme de tableau
        """
        if not results:
            print("❌ Aucun résultat à afficher")
            return
        
        print("📊 TABLEAU DE RÉSULTATS")
        print("=" * 80)
        
        # En-tête du tableau
        print(f"{'Période':<8} {'Performance':<12} {'Volatilité':<12} {'Rdt Espéré':<12} {'Max DD':<10} {'Prix Début':<11} {'Prix Fin':<10}")
        print("-" * 80)
        
        # Données
        for period, metrics in results.items():
            print(f"{period:<8} "
                  f"{metrics['performance']:>10.2f}% "
                  f"{metrics['volatilite']:>10.2f}% "
                  f"{metrics['rendement_espere']:>10.2f}% "
                  f"{metrics['max_drawdown']:>8.2f}% "
                  f"{metrics['prix_debut']:>10.2f} "
                  f"{metrics['prix_fin']:>9.2f}")
        
        print("=" * 80)
    
    def export_to_csv(self, results, filename="analyse_financiere.csv"):
        """
        Exporte les résultats vers un fichier CSV
        """
        if not results:
            print("❌ Aucune donnée à exporter")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                # Colonnes
                fieldnames = ['periode', 'performance', 'volatilite', 'rendement_espere', 
                             'max_drawdown', 'nb_points', 'date_debut', 'date_fin', 
                             'prix_debut', 'prix_fin']
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                # Données
                for period, metrics in results.items():
                    row = {'periode': period}
                    row.update(metrics)
                    writer.writerow(row)
            
            print(f"💾 Résultats exportés vers {filename}")
            
        except Exception as e:
            print(f"❌ Erreur export CSV: {e}")
    
    def export_to_json(self, results, filename="analyse_financiere.json"):
        """
        Exporte les résultats vers un fichier JSON
        """
        if not results:
            print("❌ Aucune donnée à exporter")
            return
        
        try:
            # Création du rapport complet
            rapport = {
                'analyse_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'donnees_source': {
                    'nb_points_total': len(self.data),
                    'periode_complete': f"{self.data[0]['date'].strftime('%Y-%m-%d')} → {self.data[-1]['date'].strftime('%Y-%m-%d')}"
                },
                'metriques_par_periode': results,
                'definitions': {
                    'performance': 'Rendement total en % ((Prix_fin/Prix_début)-1)*100',
                    'volatilite': 'Volatilité annualisée en % (écart-type quotidien * √252)',
                    'rendement_espere': 'Rendement espéré annualisé en % (moyenne quotidienne * 252)',
                    'max_drawdown': 'Plus grande perte en % depuis un pic précédent'
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(rapport, jsonfile, indent=2, ensure_ascii=False)
            
            print(f"💾 Rapport complet exporté vers {filename}")
            
        except Exception as e:
            print(f"❌ Erreur export JSON: {e}")

