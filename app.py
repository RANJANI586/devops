from flask import Flask
import random

app = Flask(__name__)

# ----------- Classes -----------

class User:
    def __init__(self, name, user_id, phone, pickup, destination, distance):
        self.name = name
        self.user_id = user_id
        self.phone_number = phone
        self.pickup_loc = pickup
        self.destination_loc = destination
        self.distance = distance


class Driver:
    def __init__(self, name, driver_id, phone):
        self.driver_name = name
        self.driver_id = driver_id
        self.phone_number = phone


class Booking:
    def __init__(self, booking_id, vehicle_id, user, driver):
        self.booking_id = booking_id
        self.vehicle_id = vehicle_id
        self.user = user
        self.driver = driver


class Payment:
    def __init__(self, booking_id, method, amount, payment_id):
        self.booking_id = booking_id
        self.method = method
        self.amount = amount
        self.payment_id = payment_id


# ----------- Route -----------

@app.route("/")
def home():

    # Predefined data
    users = [
        User("Ranjani", 101, 9876543210, "Chennai", "Trichy", 300),
        User("Vignesh", 102, 9123456780, "Madurai", "Salem", 200)
    ]

    drivers = [
        Driver("Shanthini", 1, 1111111111),
        Driver("Sameer", 2, 2222222222),
        Driver("Sanu", 3, 3333333333)
    ]

    payment_method = "UPI"

    # Booking logic
    selected_user = users[0]
    assigned_driver = random.choice(drivers)

    booking_id = random.randint(100, 999)
    vehicle_id = "TN" + str(booking_id)

    booking = Booking(booking_id, vehicle_id, selected_user, assigned_driver)

    cost_per_km = 10
    amount = selected_user.distance * cost_per_km

    payment = Payment(booking_id, payment_method, amount, random.randint(1000, 9999))

    # Return HTML (NOT print)
    return f"""
    <h2>🚕 Booking Confirmed</h2>
    <p><b>Booking ID:</b> {booking.booking_id}</p>
    <p><b>Vehicle ID:</b> {booking.vehicle_id}</p>
    <p><b>User:</b> {booking.user.name}</p>
    <p><b>Driver:</b> {booking.driver.driver_name}</p>
    <p><b>Driver Phone:</b> {booking.driver.phone_number}</p>
    <p><b>From:</b> {booking.user.pickup_loc}</p>
    <p><b>To:</b> {booking.user.destination_loc}</p>
    <p><b>Distance:</b> {booking.user.distance} km</p>
    <p><b>Amount:</b> ₹{payment.amount}</p>
    <p><b>Payment:</b> {payment.method}</p>
    """


# ----------- Run Server -----------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
