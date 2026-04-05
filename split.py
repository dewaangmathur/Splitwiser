# from collections import defaultdict

# def minimize_transactions(expenses, custom_debts=None):
#     """
#     Calculate balances and minimize transactions.
    
#     Args:
#         expenses: List of expense groups with equal splits
#         custom_debts: List of custom debts (unequal dues)
    
#     Returns:
#         transactions: List of simplified payment instructions
#         balance: Dictionary of final balances for each person
#     """
#     balance = defaultdict(float)
    
#     if custom_debts is None:
#         custom_debts = []

#     # Step 1: Calculate balances from equal split expenses
#     for exp in expenses:
#         payers = exp["payers"]
#         participants = exp["participants"]
#         total_amount = sum(payers.values())
#         split_share = total_amount / len(participants)

#         # Each payer contributes positively
#         for payer, amt in payers.items():
#             balance[payer] += amt - split_share

#         # Non-payers owe their share
#         for person in participants:
#             if person not in payers:
#                 balance[person] -= split_share
    
#     # Step 2: Add custom debts (unequal dues)
#     for debt in custom_debts:
#         balance[debt["from"]] -= debt["amount"]
#         balance[debt["to"]] += debt["amount"]

#     # Step 3: Separate debtors and creditors
#     debtors = [[p, round(-amt, 2)] for p, amt in balance.items() if amt < -1e-6]
#     creditors = [[p, round(amt, 2)] for p, amt in balance.items() if amt > 1e-6]

#     i, j = 0, 0
#     transactions = []

#     # Step 4: Greedy settle algorithm
#     while i < len(debtors) and j < len(creditors):
#         owed = debtors[i][1]
#         to_receive = creditors[j][1]
#         settle = round(min(owed, to_receive), 2)

#         if settle > 0:
#             transactions.append(f"{debtors[i][0]} pays ₹{settle} to {creditors[j][0]}")

#         debtors[i][1] = round(debtors[i][1] - settle, 2)
#         creditors[j][1] = round(creditors[j][1] - settle, 2)

#         # Floating point tolerance check
#         if abs(debtors[i][1]) < 1e-6:
#             i += 1
#         if abs(creditors[j][1]) < 1e-6:
#             j += 1

#     return transactions, balance


# def main():
#     print("💰 FairSplit - Smart Group Expense Splitter")
#     print("=" * 60)

#     n = int(input("Enter number of people: "))
#     members = input("Enter names separated by space: ").split()

#     # Equal split expense groups
#     g = int(input("\nEnter number of expense groups (equal splits): "))
#     expenses = []

#     for i in range(g):
#         print(f"\n🧾 Expense Group #{i+1}")
#         participants = input("Who participated? (names separated by space): ").split()

#         num_payers = int(input("How many people paid in this group? "))
#         payers = {}

#         for _ in range(num_payers):
#             payer_name = input("Enter payer name: ").strip()
#             amount_paid = float(input(f"Amount paid by {payer_name} (₹): "))
#             description = input(f"Description for {payer_name}'s payment: ").strip()
#             payers[payer_name] = amount_paid

#         expenses.append({
#             "payers": payers,
#             "participants": set(participants)
#         })

#     # Custom debts (unequal dues)
#     print("\n" + "=" * 60)
#     custom_debts = []
#     add_custom = input("\nDo you want to add custom debts (unequal dues)? (y/n): ").lower()
    
#     if add_custom == 'y':
#         num_debts = int(input("How many custom debts to add? "))
        
#         for i in range(num_debts):
#             print(f"\n💸 Custom Debt #{i+1}")
#             from_person = input("From (who owes): ").strip()
#             to_person = input("To (who receives): ").strip()
#             amount = float(input("Amount (₹): "))
#             description = input("Description (optional): ").strip()
            
#             if from_person != to_person and amount > 0:
#                 custom_debts.append({
#                     "from": from_person,
#                     "to": to_person,
#                     "amount": amount,
#                     "description": description if description else "No description"
#                 })

#     # Display summary
#     print("\n" + "=" * 60)
#     print("📊 EXPENSE SUMMARY")
#     print("=" * 60)
    
#     for idx, exp in enumerate(expenses):
#         print(f"\n💡 Group #{idx+1}")
#         for payer, amt in exp["payers"].items():
#             print(f"   {payer} paid ₹{amt:.2f}")
#         print(f"   Participants: {', '.join(exp['participants'])}")
    
#     if custom_debts:
#         print("\n💸 Custom Debts:")
#         for debt in custom_debts:
#             print(f"   {debt['from']} owes {debt['to']} ₹{debt['amount']:.2f} → {debt['description']}")

#     # Compute settlements
#     transactions, balance = minimize_transactions(expenses, custom_debts)

#     print("\n" + "=" * 60)
#     print("⚖ FINAL BALANCES")
#     print("=" * 60)
#     for p in members:
#         amt = round(balance[p], 2)
#         if amt > 0:
#             print(f"{p}: gets ₹{amt}")
#         elif amt < 0:
#             print(f"{p}: owes ₹{-amt}")
#         else:
#             print(f"{p}: settled up")

#     print("\n" + "=" * 60)
#     print("💳 SIMPLIFIED SETTLEMENTS (Minimum Transactions)")
#     print("=" * 60)
#     if transactions:
#         for t in transactions:
#             print(t)
#     else:
#         print("All settled up! 🎉")

#     print("\n✅ Calculation Complete!")


# if __name__ == "__main__":
#     main()


































from collections import defaultdict
from datetime import date


def minimize_transactions(expenses, custom_debts=None, already_paid=None):
    """
    Calculate balances and minimize transactions.

    Args:
        expenses:      List of expense groups with equal splits
        custom_debts:  List of global custom debts (unequal dues)
        already_paid:  List of already-paid entries

    Returns:
        transactions: List of simplified payment instructions
        balance:      Dictionary of final balances for each person
    """
    balance = defaultdict(float)

    if custom_debts is None:
        custom_debts = []
    if already_paid is None:
        already_paid = []

    # Step 1: Equal split expenses
    for exp in expenses:
        payers = exp["payers"]
        participants = exp["participants"]
        total_amount = sum(payers.values())
        split_share = total_amount / len(participants)

        for payer, amt in payers.items():
            balance[payer] += amt - split_share

        for person in participants:
            if person not in payers:
                balance[person] -= split_share

    # Step 2: Custom debts (from owes to)
    for debt in custom_debts:
        balance[debt["from"]] -= debt["amount"]
        balance[debt["to"]]   += debt["amount"]

    # Step 3: Already paid
    # from already paid to → from's balance UP, to's balance DOWN
    for ap in already_paid:
        balance[ap["from"]] += ap["amount"]
        balance[ap["to"]]   -= ap["amount"]

    # Step 4: Separate debtors and creditors
    
    # debtors   = [[p, round(-amt, 2)] for p, amt in balance.items() if amt < -1e-6]
    # creditors = [[p, round( amt, 2)] for p, amt in balance.items() if amt >  1e-6]

    # AFTER:
    debtors   = sorted([[p, round(-amt, 2)] for p, amt in balance.items() if amt < -1e-6], key=lambda x: -x[1])
    creditors = sorted([[p, round( amt, 2)] for p, amt in balance.items() if amt >  1e-6], key=lambda x: -x[1])

    i, j = 0, 0
    transactions = []

    # Step 5: Greedy settle
    while i < len(debtors) and j < len(creditors):
        settle = round(min(debtors[i][1], creditors[j][1]), 2)
        if settle > 0:
            transactions.append(
                f"{debtors[i][0]} pays ₹{settle} to {creditors[j][0]}"
            )
        debtors[i][1]   = round(debtors[i][1]   - settle, 2)
        creditors[j][1] = round(creditors[j][1] - settle, 2)
        if abs(debtors[i][1])   < 1e-6: i += 1
        if abs(creditors[j][1]) < 1e-6: j += 1

    return transactions, balance


def input_date(prompt, default=None):
    """Prompt for a date in DD/MM/YYYY format. Enter to use default."""
    default_str = default or date.today().strftime("%d/%m/%Y")
    val = input(f"  {prompt} [default: {default_str}]: ").strip()
    return val if val else default_str


def get_already_paid():
    """Prompt user to enter already-paid entries."""
    already_paid = []
    add = input("\nDo you want to add already-paid entries? (y/n): ").strip().lower()
    if add != 'y':
        return already_paid

    print("(From = who already paid | To = who received the payment)")
    n = int(input("How many already-paid entries? "))
    for i in range(n):
        print(f"\n✅ Already Paid #{i+1}")
        from_person = input("  From (already paid): ").strip()
        to_person   = input("  To   (received):     ").strip()
        amount      = float(input("  Amount (₹): "))
        description = input("  Description (optional): ").strip()
        entry_date  = input_date("Date (DD/MM/YYYY)")

        if from_person != to_person and amount > 0:
            already_paid.append({
                "from":        from_person,
                "to":          to_person,
                "amount":      amount,
                "description": description if description else "Already paid",
                "date":        entry_date,
            })
        else:
            print("  ⚠️  Skipped: same person or zero amount.")

    return already_paid


def main():
    print("💰 FairSplit - Smart Group Expense Splitter")
    print("=" * 60)

    n = int(input("Enter number of people: "))
    members   = input("Enter names separated by space: ").split()
    trip_date = input_date("Trip / Group Date (DD/MM/YYYY)")

    # ── Equal split expense groups ────────────────────────────────
    g = int(input("\nEnter number of expense groups (equal splits): "))
    expenses = []

    for i in range(g):
        print(f"\n🧾 Expense Group #{i+1}")
        participants = input("  Who participated? (names separated by space): ").split()

        num_payers = int(input("  How many people paid in this group? "))
        payers      = {}
        payer_meta  = {}   # stores desc + date per payer for display

        for _ in range(num_payers):
            payer_name  = input("  Enter payer name: ").strip()
            amount_paid = float(input(f"  Amount paid by {payer_name} (₹): "))
            description = input(f"  Description for {payer_name}'s payment: ").strip() or "No description"
            entry_date  = input_date("Date for this payment (DD/MM/YYYY)")
            payers[payer_name] = amount_paid
            payer_meta[payer_name] = {"desc": description, "date": entry_date}

        expenses.append({
            "payers":      payers,
            "payer_meta":  payer_meta,
            "participants": set(participants),
        })

    # ── Custom debts ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    custom_debts = []
    add_custom = input("\nDo you want to add global custom debts (unequal dues)? (y/n): ").lower()

    if add_custom == 'y':
        print("(From = person who owes | To = person who receives)")
        num_debts = int(input("How many custom debts to add? "))

        for i in range(num_debts):
            print(f"\n💸 Custom Debt #{i+1}")
            from_person = input("  From (who owes):     ").strip()
            to_person   = input("  To   (who receives): ").strip()
            amount      = float(input("  Amount (₹): "))
            description = input("  Description (optional): ").strip()
            entry_date  = input_date("Date (DD/MM/YYYY)")

            if from_person != to_person and amount > 0:
                custom_debts.append({
                    "from":        from_person,
                    "to":          to_person,
                    "amount":      amount,
                    "description": description if description else "No description",
                    "date":        entry_date,
                })

    # ── Already paid ──────────────────────────────────────────────
    already_paid = get_already_paid()

    # ── Display summary ───────────────────────────────────────────
    print("\n" + "=" * 60)
    print("📊 EXPENSE SUMMARY")
    print("=" * 60)
    print(f"📅 Trip / Group Date: {trip_date}")

    for idx, exp in enumerate(expenses):
        print(f"\n💡 Group #{idx+1}")
        for payer, amt in exp["payers"].items():
            meta = exp["payer_meta"].get(payer, {})
            desc = meta.get("desc", "No description")
            dt   = meta.get("date", "")
            date_str = f" ({dt})" if dt else ""
            print(f"   {payer} paid ₹{amt:.2f} → {desc}{date_str}")
        print(f"   Participants: {', '.join(exp['participants'])}")

    if already_paid:
        print("\n✅ Already Paid:")
        for ap in already_paid:
            date_str = f" ({ap['date']})" if ap.get('date') else ""
            print(f"   {ap['from']} → {ap['to']}: ₹{ap['amount']:.2f} ({ap['description']}){date_str}")

    if custom_debts:
        print("\n💸 Custom Debts:")
        for debt in custom_debts:
            date_str = f" ({debt['date']})" if debt.get('date') else ""
            print(f"   {debt['from']} owes {debt['to']} ₹{debt['amount']:.2f} → {debt['description']}{date_str}")

    # ── Compute settlements ───────────────────────────────────────
    transactions, balance = minimize_transactions(expenses, custom_debts, already_paid)

    print("\n" + "=" * 60)
    print("⚖  FINAL BALANCES")
    print("=" * 60)
    for p in members:
        amt = round(balance[p], 2)
        if amt > 0:
            print(f"  {p}: gets ₹{amt}")
        elif amt < 0:
            print(f"  {p}: owes ₹{-amt}")
        else:
            print(f"  {p}: settled up ✅")

    print("\n" + "=" * 60)
    print("💳 SIMPLIFIED SETTLEMENTS (Minimum Transactions)")
    print("=" * 60)
    if transactions:
        for t in transactions:
            print(" ", t)
    else:
        print("  All settled up! 🎉")

    print("\n✅ Calculation Complete!")


if __name__ == "__main__":
    main()