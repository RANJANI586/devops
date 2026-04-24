from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory database
bills_db = []

# 🔌 Bill Calculation Logic (Realistic Slabs)
def calculate_bill(units):
    if units <= 100:
        amount = units * 1.5
    elif units <= 200:
        amount = (100 * 1.5) + (units - 100) * 2.5
    elif units <= 300:
        amount = (100 * 1.5) + (100 * 2.5) + (units - 200) * 4
    else:
        amount = (100 * 1.5) + (100 * 2.5) + (100 * 4) + (units - 300) * 6

    tax = amount * 0.05  # 5% tax
    total = amount + tax

    return round(total, 2)

# 🟢 Generate Bill
@app.route('/generate-bill', methods=['POST'])
def generate_bill():
    data = request.json

    name = data.get("name")
    units = data.get("units")

    if not name or units is None:
        return jsonify({"error": "Name and units required"}), 400

    total_amount = calculate_bill(units)

    bill = {
        "bill_id": str(uuid.uuid4()),
        "customer_name": name,
        "units_consumed": units,
        "total_amount": total_amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    bills_db.append(bill)

    return jsonify({
        "message": "Bill generated successfully",
        "bill": bill
    })

# 🟢 Get all bills
@app.route('/bills', methods=['GET'])
def get_bills():
    return jsonify(bills_db)

# 🟢 Get bill by ID
@app.route('/bill/<bill_id>', methods=['GET'])
def get_bill(bill_id):
    for bill in bills_db:
        if bill["bill_id"] == bill_id:
            return jsonify(bill)

    return jsonify({"error": "Bill not found"}), 404

# 🟢 Delete bill
@app.route('/bill/<bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    global bills_db
    bills_db = [b for b in bills_db if b["bill_id"] != bill_id]

    return jsonify({"message": "Bill deleted successfully"})

# 🟢 Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=True)
