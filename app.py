from flask import Flask

app=Flask(__name__)

@app.route("/")
def home():
    from datetime import date
from collections import defaultdict

class Expense:
    def __init__(self, description, amount, payer_id, participant_ids):
        self.description = description
        self.amount = amount
        self.payer_id = payer_id
        self.participant_ids = participant_ids
        self.date = date.today()


class User:
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name
        self.ledger = defaultdict(float)
        self.expense_history = []


class Group:
    def __init__(self, name):
        self.group_name = name
        self.members = set()
        self.expenses = []


class ExpenseSharingApp:
    def __init__(self):
        self.user_registry = {}
        self.group_registry = {}

    def register_user(self, user_id, name):
        if user_id in self.user_registry:
            print("! Error: User ID already exists.")
            return
        self.user_registry[user_id] = User(user_id, name)
        print(f"√ User '{name}' registered.")

    def list_all_groups(self):
        if not self.group_registry:
            print("(No groups created yet)")
            return
        print("Current Groups:", ", ".join(sorted(self.group_registry.keys())))

    def create_group(self, name):
        if name in self.group_registry:
            print("! Error: Group name already exists.")
        else:
            self.group_registry[name] = Group(name)
            print(f"√ Group '{name}' created successfully.")
        self.list_all_groups()

    def add_member_to_group(self, group_name, user_id):
        group = self.group_registry.get(group_name)
        user = self.user_registry.get(user_id)

        if not group:
            print("! Error: Group not found.")
            self.list_all_groups()
            return
        if not user:
            print("! Error: User ID not found.")
            return

        if user_id in group.members:
            print("! Notice: User already in group.")
        else:
            group.members.add(user_id)
            print(f"√ {user.name} added to {group_name}")

    def record_expense(self, group_name, desc, total_amount, payer_id):
        group = self.group_registry.get(group_name)

        if not group or payer_id not in group.members:
            print("! Error: Transaction failed.")
            return

        if len(group.members) < 2:
            print("! Error: Need at least 2 members.")
            return

        share = total_amount / len(group.members)
        participants = list(group.members)

        expense = Expense(desc, total_amount, payer_id, participants)
        group.expenses.append(expense)
        self.user_registry[payer_id].expense_history.append(expense)

        for member_id in participants:
            if member_id == payer_id:
                continue

            payer = self.user_registry[payer_id]
            debtor = self.user_registry[member_id]

            payer.ledger[member_id] -= share
            debtor.ledger[payer_id] += share

        print(f"√ Expense of ${total_amount:.2f} split among {len(group.members)} members.")

    def settle_balance(self, from_id, to_id, amount):
        from_user = self.user_registry.get(from_id)
        to_user = self.user_registry.get(to_id)

        if from_user and to_user:
            from_user.ledger[to_id] -= amount
            to_user.ledger[from_id] += amount
            print(f"√ Settlement of ${amount} recorded.")
        else:
            print("! Error: Invalid user IDs.")

    def print_user_report(self, user_id):
        user = self.user_registry.get(user_id)

        if not user:
            print("! Error: User not found.")
            return

        print("\n" + "=" * 40)
        print(f"FINANCIAL REPORT: {user.name.upper()}")
        print("=" * 40)

        group_count = sum(1 for g in self.group_registry.values() if user_id in g.members)
        total_paid = sum(e.amount for e in user.expense_history)
        total_owed = sum(v for v in user.ledger.values() if v > 0)

        current_month = date.today().month
        monthly_sum = sum(e.amount for e in user.expense_history if e.date.month == current_month)

        print(f"• Active Groups    : {group_count}")
        print(f"• Total Paid Out   : ${total_paid:.2f}")
        print(f"• Debt to Others   : ${total_owed:.2f}")
        print(f"• Spent This Month : ${monthly_sum:.2f}")

        print("\nDETAILED BALANCES:")
        has_balance = False

        for peer_id, value in user.ledger.items():
            if abs(value) > 0.01:
                has_balance = True
                peer_name = self.user_registry[peer_id].name
                if value > 0:
                    print(f"[!] You owe {peer_name}: ${value:.2f}")
                else:
                    print(f"[S] {peer_name} owes you: ${abs(value):.2f}")

        if not has_balance:
            print("(All settled up!)")

        print("=" * 40)


def main():
    app = ExpenseSharingApp()

    print("EXPENSE SHARING SYSTEM v1.0")

    while True:
        print("\nMain Menu:")
        print("1. Register User  2. Create Group  3. Add Member")
        print("4. Record Expense 5. Settle Balance 6. View Report")
        print("7. Exit")

        try:
            choice = int(input("Action > "))

            if choice == 1:
                user_id = input("User ID: ")
                name = input("Name: ")
                app.register_user(user_id, name)

            elif choice == 2:
                name = input("New Group Name: ")
                app.create_group(name)

            elif choice == 3:
                app.list_all_groups()
                group_name = input("Target Group: ")
                user_id = input("User ID to Add: ")
                app.add_member_to_group(group_name, user_id)

            elif choice == 4:
                group = input("Group Name: ")
                desc = input("Description: ")
                amount = float(input("Total Amount: "))
                payer = input("Payer ID: ")
                app.record_expense(group, desc, amount, payer)

            elif choice == 5:
                from_id = input("Your ID: ")
                to_id = input("Recipient ID: ")
                amount = float(input("Amount Settled: "))
                app.settle_balance(from_id, to_id, amount)

            elif choice == 6:
                user_id = input("Enter User ID: ")
                app.print_user_report(user_id)

            elif choice == 7:
                print("System shutting down...")
                break

            else:
                print("! Invalid selection.")

        except Exception:
            print("! Error: Please enter valid data.")


if __name__ == "__main__":
    main()
app.run(host="0.0.0.0",port=5001)
