#!/usr/bin/env python3
import argparse
import controller
import database
import views

def main() -> None:
    parser = argparse.ArgumentParser(description="AfB Shop x /e/OS Tablet Compatibility Crawler")
    parser.add_argument("--json", action="store_true", help="Also save results to afb_eos_results.json")
    parser.add_argument("--ods", action="store_true", help="Also create afb_eos_results.ods spreadsheet")
    args = parser.parse_args()

    database.init_db()
    previous_state = database.load_previous_state()

    results = controller.run_crawler()
    views.print_report(results)

    if args.ods or args.json:
        print("\n[*] Fetching /e/OS Android versions from doc.e.foundation...")
        controller.enrich_with_versions(results)
        
        print("\n[*] Comparing with previous state...")
        updated_results, changes_log = controller.enrich_with_prices_and_conditions(results, previous_state)
        
        views.print_changes(changes_log)
        
        print("\n[*] Saving updated state to SQLite database...")
        database.save_to_db(updated_results)
        print("  Database updated successfully.")

        if args.json:
            views.save_json(updated_results)
        if args.ods:
            views.save_ods(updated_results)

if __name__ == "__main__":
    main()
