from flask import Flask, render_template, request
from random import randint
import mysql.connector

app = Flask(__name__)

class FoodChatbot:
    def __init__(self):
        self.menu = {
            "pizza": {"price": 10},
            "burger": {"price": 8},
            "salad": {"price": 6},
            "pasta": {"price": 12},
            "sandwich": {"price": 7},
            "sushi": {"price": 15},
            "steak": {"price": 20},
            "chicken": {"price": 14},
            "taco": {"price": 9},
            "burrito": {"price": 11},
            "soup": {"price": 5},
            "fries": {"price": 4},
            "ice cream": {"price": 6},
            "cake": {"price": 8},
            "smoothie": {"price": 5}
        }
        self.cart = {}
        
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="food"
        )
        self.db_cursor = self.db_connection.cursor()
        self.create_order_table()  # Call the method to create the table

    def create_order_table(self):
        # SQL command to create the "order" table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `order` (
            `item_name` VARCHAR(255),
            `quantity` INT
        )
        """
        self.db_cursor.execute(create_table_query)
        self.db_connection.commit()

    def insert_order_data(self, item, quantity):
        # SQL command to insert order data into the "order" table
        insert_query = """
        INSERT INTO `order` (item_name, quantity)
        VALUES (%s, %s)
        """
        order_data = (item, quantity)
        self.db_cursor.execute(insert_query, order_data)
        self.db_connection.commit()

    def welcome(self):
        return "Welcome to our food ordering service! How can I assist you today?"

    def display_menu(self):
        menu_list = "\n".join([f"{item.capitalize()}: ${details['price']}" for item, details in self.menu.items()])
        return f"Here's our menu:\n{menu_list}"

    def add_to_menu(self, item, price):
        self.menu[item.lower()] = {"price": price}
        return f"{item.capitalize()} has been added to the menu."

    def order(self, item, quantity=1):
        item = item.lower()
        if item in self.menu:
            if item in self.cart:
                self.cart[item] += quantity
            else:
                self.cart[item] = quantity
            return f"You've added {quantity} {item}(s) to your cart."
        else:
            return "Sorry, we don't have that item in our menu."

    def remove_order(self, item):
        item = item.lower()
        if item in self.cart:
            del self.cart[item]
            return f"{item.capitalize()} has been removed from your cart."
        else:
            return f"{item.capitalize()} is not in your cart."

    def display_cart(self):
        if not self.cart:
            return "Your cart is empty."
        cart_items = "\n".join([f"{item.capitalize()}: {quantity}" for item, quantity in self.cart.items()])
        return f"Your cart:\n{cart_items}"

    def calculate_total(self):
        total = sum([self.menu[item]['price'] * quantity for item, quantity in self.cart.items()])
        return f"Your total is ${total}."

    def place_order(self):
        if not self.cart:
            return "Your cart is empty. Please add items before placing the order."
        for item, quantity in self.cart.items():
            self.insert_order_data(item, quantity)
        order_id = randint(10, 999)  # Random 2 to 3 digit order ID
        self.cart.clear()
        return f"Your order has been placed. Order ID: #{order_id}. Thank you!"

    def final_order(self):
        print("Here's your final order:")
        print(self.display_cart())
        confirmation = input("Confirm your order? (yes/no): ").lower()
        if confirmation == "yes":
            print(self.place_order())
        else:
            print("Order not confirmed.")

    def track_order(self):
        # Assuming a simple tracking mechanism
        return "Your order is being prepared. It will be delivered shortly."

    def chat(self, user_input):
        if any(greeting in user_input for greeting in ["hi", "hello", "hey"]):
            return "Hello! How can I assist you today?"
        elif user_input == "bye" or user_input == "goodbye":
            return "Goodbye! Have a great day!"
        elif user_input in ["display menu", "menu", "show menu", "give menu"]:
            return self.display_menu()
        elif user_input in ["add items","add","add menu","let's order"]:
            item = input("Enter the name of the item: ").lower()
            price = float(input("Enter the price of the item: "))
            return self.add_to_menu(item, price)
        elif user_input.startswith("order"):
            item = input("Enter the name of the item: ").lower()
            quantity = int(input("Enter the quantity: "))
            return self.order(item, quantity)
        elif user_input.startswith("remove"):
            item = input("Enter the name of the item: ").lower()
            return self.remove_order(item)
        elif user_input in ["show cart","display cart","cart","my orders"]:
            return self.display_cart()
        elif user_input in ["calculate total","total","total price","show bill","bill"]:
            return self.calculate_total()
        elif user_input in ["final order"]:
            self.final_order()
        elif user_input in ["track order","where is my order","check my order"]:
            return self.track_order()
        elif user_input in ["track order status","order status"]:
            return "Sorry, we don't have a detailed tracking system at the moment."
        else:
            return "I'm sorry, I didn't understand that. How can I assist you?"

# Create an instance of the FoodChatbot
chatbot = FoodChatbot()

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = chatbot.chat(user_input)
    return response

if __name__ == '__main__':
    app.run(debug=True)
