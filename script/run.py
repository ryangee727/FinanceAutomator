#!/usr/bin/env python
import os, sys
import pandas as pd
import argparse

# Adds the sources directory to Python Path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.conscious_spending_plan import ConsciousSpendingPlan
from utils.a_r_expenses import ARExpenses
from utils.bank_export_retriever import BankExportRetriever


parser = argparse.ArgumentParser(description='A CSV to Google Doc ETL that automates Monthly Finance Workflow.')
parser.add_argument('--step2', dest='step2', action='store_true',
                    help='Activates Step 2 of Workflow (After Manually Entering Shared Expenses)')
parser.add_argument('--skip_next_month', dest='skip_next_month', action='store_true',
                    help='Do not add a new worksheet for the next month.')
args = parser.parse_args()

csp = ConsciousSpendingPlan()
if not args.step2:
    print("Starting Step 1...")
    bank_exports = BankExportRetriever('../data/').get_bank_exports()
    merged = pd.concat(bank_exports, ignore_index=True)
    if not args.skip_next_month:
        csp.add_next_months_worksheet()
    csp.import_df(merged)
elif args.step2:
    print("Starting Step 2...")
    csp.update_worksheet_with_split_shared()
    ARExpenses = ARExpenses()
    ARExpenses.import_df(csp.export_shared_only_df())
    if not args.skip_next_month:
        ARExpenses.add_next_months_worksheet()
print("Finished!")