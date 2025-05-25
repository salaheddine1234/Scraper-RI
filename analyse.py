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
        print(f"Fichier {filename} non trouvé")
        return None
    except Exception as e:
        print(f"Erreur lecture fichier: {e}")
        return None

def main():
    """
    Fonction principale - Analyse complète de l'OPCVM
    """
    print("ANALYSE COMPLÈTE OPCVM - IE0002XZSHO1")
    print("=" * 70)
    
    # Option 1: Charger depuis un fichier existant 
    historical_data = load_data_from_file("opcvm_data.json")
    
    # Option 2: Scraper de nouvelles données si nécessaire
    if not historical_data:
        print("Scraping de nouvelles données...")
        
        scraper = OPCVMScraper("IE0002XZSHO1")
        result = scraper.scrape_all_sources()
        
        if result and result.get('historical_data'):
            historical_data = result['historical_data']
            print(f"{len(historical_data)} points de données récupérés")
        else:
            print("Impossible de récupérer les données")
            return
    else:
        print(f"Données chargées: {len(historical_data)} lignes")
    
    # Analyse financière
    print("\n" + "="*70)
    print("ANALYSE FINANCIÈRE")
    print("="*70)
    
    try:
        # Création du calculateur
        calculator = FinancialCalculator(historical_data)
        
        # Analyse de toutes les périodes
        results = calculator.analyze_all_periods()
        
        if results:   
            # Export des résultats
            print(f"\n EXPORT DES RÉSULTATS")
            print("="*30)
            calculator.export_to_csv(results, "analyse_opcvm.csv")
            calculator.export_to_json(results, "analyse_opcvm.json")
            
            # Résumé final
            print(f"\n RÉSUMÉ EXÉCUTIF")
            print("="*30)
            
    
    except Exception as e:
        print(f" Erreur lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()