from flask import Flask, request, redirect

from datetime import date
from collections import defaultdict

app = Flask(__name__)

# =========================
# MODELS
# =========================

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


# =========================
# MAIN APP LOGIC
# =========================

class ExpenseSharingApp:
    def __init__(self):
        self.user_registry = {}
        self.group_registry = {}

    def register_user(self, user_id, name):
        if user_id in self.user_registry:
            return "User ID already exists"

        self.user_registry[user_id] = User(user_id, name)
        return f"User '{name}' registered successfully"

    def create_group(self, name):
        if name in self.group_registry:
            return "Group already exists"

        self.group_registry[name] = Group(name)
        return f"Group '{name}' created successfully"

    def add_member_to_group(self, group_name, user_id):
        group = self.group_registry.get(group_name)
        user = self.user_registry.get(user_id)

        if not group:
            return "Group not found"

        if not user:
            return "User not found"

        if user_id in group.members:
            return "User already exists in group"

        group.members.add(user_id)

        return f"{user.name} added to {group_name}"

    def record_expense(self, group_name, desc, total_amount, payer_id):
        group = self.group_registry.get(group_name)

        if not group:
            return "Group not found"

        if payer_id not in group.members:
            return "Payer is not in group"

        if len(group.members) < 2:
            return "Need at least 2 members"

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

        return "Expense recorded successfully"

    def get_report(self, user_id):

        user = self.user_registry.get(user_id)

        if not user:
            return "User not found"

        result = f"""
        <h2>Financial Report - {user.name}</h2>

        <p>Total Expenses Paid: {sum(e.amount for e in user.expense_history)}</p>

        <h3>Balances</h3>
        """

        for peer_id, value in user.ledger.items():

            peer_name = self.user_registry[peer_id].name

            if value > 0:
                result += f"<p>You owe {peer_name}: ${value:.2f}</p>"

            elif value < 0:
                result += f"<p>{peer_name} owes you: ${abs(value):.2f}</p>"

        return result


# =========================
# GLOBAL OBJECT
# =========================

expense_app = ExpenseSharingApp()


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    return """
    <h1>EXPENSE SHARING SYSTEM</h1>

    <hr>

    <h2>1. Register User</h2>

    <form action="/register" method="post">

        User ID:
        <input type="text" name="user_id">

        <br><br>

        Name:
        <input type="text" name="name">

        <br><br>

        <button type="submit">Register</button>

    </form>

    <hr>

    <h2>2. Create Group</h2>

    <form action="/create-group" method="post">

        Group Name:
        <input type="text" name="group_name">

        <br><br>

        <button type="submit">Create Group</button>

    </form>

    <hr>

    <h2>3. Add Member To Group</h2>

    <form action="/add-member" method="post">

        Group Name:
        <input type="text" name="group_name">

        <br><br>

        User ID:
        <input type="text" name="user_id">

        <br><br>

        <button type="submit">Add Member</button>

    </form>

    <hr>

    <h2>4. Record Expense</h2>

    <form action="/record-expense" method="post">

        Group Name:
        <input type="text" name="group_name">

        <br><br>

        Description:
        <input type="text" name="description">

        <br><br>

        Amount:
        <input type="number" step="0.01" name="amount">

        <br><br>

        Payer ID:
        <input type="text" name="payer_id">

        <br><br>

        <button type="submit">Record Expense</button>

    </form>

    <hr>

    <h2>5. View Report</h2>

    <form action="/report" method="get">

        User ID:
        <input type="text" name="user_id">

        <br><br>

        <button type="submit">View Report</button>

    </form>
    """


# =========================
# REGISTER USER
# =========================

@app.route("/register", methods=["POST"])
def register():

    user_id = request.form["user_id"]

    name = request.form["name"]

    message = expense_app.register_user(user_id, name)

    return f"""
    <h2>{message}</h2>

    <a href="/">Go Home</a>
    """


# =========================
# CREATE GROUP
# =========================

@app.route("/create-group", methods=["POST"])
def create_group():

    group_name = request.form["group_name"]

    message = expense_app.create_group(group_name)

    return f"""
    <h2>{message}</h2>

    <a href="/">Go Home</a>
    """


# =========================
# ADD MEMBER
# =========================

@app.route("/add-member", methods=["POST"])
def add_member():

    group_name = request.form["group_name"]

    user_id = request.form["user_id"]

    message = expense_app.add_member_to_group(group_name, user_id)

    return f"""
    <h2>{message}</h2>

    <a href="/">Go Home</a>
    """


# =========================
# RECORD EXPENSE
# =========================

@app.route("/record-expense", methods=["POST"])
def record_expense():

    group_name = request.form["group_name"]

    description = request.form["description"]

    amount = float(request.form["amount"])

    payer_id = request.form["payer_id"]

    message = expense_app.record_expense(
        group_name,
        description,
        amount,
        payer_id
    )

    return f"""
    <h2>{message}</h2>

    <a href="/">Go Home</a>
    """


# =========================
# REPORT
# =========================

@app.route("/report")
def report():

    user_id = request.args.get("user_id")

    return expense_app.get_report(user_id)


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
