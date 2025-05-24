"""
Script complet pour analyser l'OPCVM IE0002XZSHO1
Combine le scraping et l'analyse financière
"""
import json
from scraping import OPCVMScraper
from calcul import FinancialCalculator

def load_data_from_file(filename="opcvm_data.json"):
    """
    Charge les données depuis un fichier JSON existant
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('historical_data', [])
    except FileNotFoundError:
        print(f"❌ Fichier {filename} non trouvé")
        return None
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        return None

def main():
    """
    Fonction principale - Analyse complète de l'OPCVM
    """
    print("🏦 ANALYSE COMPLÈTE OPCVM - IE0002XZSHO1")
    print("🎯 iShares Core MSCI World UCITS ETF")
    print("=" * 70)
    
    # Option 1: Charger depuis un fichier existant
    print("🔍 Recherche de données existantes...")
    historical_data = load_data_from_file("opcvm_data.json")
    
    # Option 2: Scraper de nouvelles données si nécessaire
    if not historical_data:
        print("📡 Scraping de nouvelles données...")
        
        scraper = OPCVMScraper("IE0002XZSHO1")
        result = scraper.scrape_all_sources()
        
        if result and result.get('historical_data'):
            historical_data = result['historical_data']
            print(f"✅ {len(historical_data)} points de données récupérés")
        else:
            print("❌ Impossible de récupérer les données")
            return
    else:
        print(f"✅ Données chargées: {len(historical_data)} points")
    
    # Analyse financière
    print("\n" + "="*70)
    print("🧮 ANALYSE FINANCIÈRE")
    print("="*70)
    
    try:
        # Création du calculateur
        calculator = FinancialCalculator(historical_data)
        
        # Analyse de toutes les périodes
        results = calculator.analyze_all_periods()
        
        if results:
            print("\n")
            # Affichage du tableau de résultats
            calculator.display_results_table(results)
            
            # Analyse détaillée par période
            print("\n📋 ANALYSE DÉTAILLÉE PAR PÉRIODE")
            print("="*50)
            
            for period, metrics in results.items():
                print(f"\n🔸 {period} ({metrics['date_debut']} → {metrics['date_fin']})")
                print(f"   💰 Prix: {metrics['prix_debut']}€ → {metrics['prix_fin']}€")
                print(f"   📈 Performance: {metrics['performance']:.2f}%")
                print(f"   📊 Volatilité: {metrics['volatilite']:.2f}%")
                print(f"   🎯 Rendement espéré: {metrics['rendement_espere']:.2f}%")
                print(f"   📉 Max Drawdown: {metrics['max_drawdown']:.2f}%")
                print(f"   📅 Période: {metrics['nb_points']} jours de données")
                
                # Interprétation simple
                if metrics['performance'] > 0:
                    print(f"   ✅ Performance positive (+{metrics['performance']:.2f}%)")
                else:
                    print(f"   ❌ Performance négative ({metrics['performance']:.2f}%)")
                
                if metrics['volatilite'] < 15:
                    print(f"   🟢 Volatilité faible ({metrics['volatilite']:.2f}%)")
                elif metrics['volatilite'] < 25:
                    print(f"   🟡 Volatilité modérée ({metrics['volatilite']:.2f}%)")
                else:
                    print(f"   🔴 Volatilité élevée ({metrics['volatilite']:.2f}%)")
            
            # Export des résultats
            print(f"\n📁 EXPORT DES RÉSULTATS")
            print("="*30)
            calculator.export_to_csv(results, "analyse_opcvm_complete.csv")
            calculator.export_to_json(results, "analyse_opcvm_complete.json")
            
            # Résumé final
            print(f"\n🎉 RÉSUMÉ EXÉCUTIF")
            print("="*30)
            
            # Performance 1 an si disponible
            if '1Y' in results:
                perf_1y = results['1Y']['performance']
                vol_1y = results['1Y']['volatilite']
                dd_1y = results['1Y']['max_drawdown']
                
                print(f"📊 Performance 1 an: {perf_1y:.2f}%")
                print(f"📊 Volatilité 1 an: {vol_1y:.2f}%")
                print(f"📊 Pire chute: {dd_1y:.2f}%")
                
                # Ratio de Sharpe approximatif (sans taux sans risque)
                if vol_1y > 0:
                    sharpe_approx = perf_1y / vol_1y
                    print(f"📊 Ratio risque/rendement: {sharpe_approx:.2f}")
            
            print("\n✅ Analyse complète terminée!")
            print("📁 Fichiers générés:")
            print("   - analyse_opcvm_complete.csv")
            print("   - analyse_opcvm_complete.json")
            
        else:
            print("❌ Aucun résultat d'analyse généré")
    
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()