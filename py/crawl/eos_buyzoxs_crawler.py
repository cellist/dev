#!/usr/bin/env python3
import argparse
import controller
import database
import views

def main() -> None:
    parser = argparse.ArgumentParser(description="BuyZOXS x /e/OS Compatibility Crawler")
    parser.add_argument("--min-score", type=int, default=80, help="Minimum fuzzy-match score")
    parser.add_argument("--json", action="store_true", help="Also save results to eos_results.json")
    parser.add_argument("--ods", action="store_true", help="Also create eos_results.ods spreadsheet")
    args = parser.parse_args()

    # 1. Initialize Database & Load History
    database.init_db()
    previous_state = database.load_previous_state()

    # 2. Run Core Business Logic (Controller)
    results = controller.run_crawler(threshold=args.min_score)
    views.print_report(results)

    # 3. Enrichment & Export (if requested)
    if args.ods or args.json:
        print("\n[*] Fetching /e/OS Android versions from doc.e.foundation...")
        controller.enrich_with_versions(results)
        
        print("\n[*] Fetching prices and conditions from buyzoxs.de...")
        updated_results, changes_log = controller.enrich_with_prices_and_conditions(results, previous_state)
        
        views.print_changes(changes_log)
        print(f"\n  {len(updated_results)} device(s) remain after condition filtering.")
        
        # 4. Persist new state
        print("\n[*] Saving updated state to SQLite database...")
        database.save_to_db(updated_results)
        print("  Database updated successfully.")

        # 5. Generate Outputs (View)
        if args.json:
            views.save_json(updated_results)
        if args.ods:
            views.save_ods(updated_results)

if __name__ == "__main__":
    main()
