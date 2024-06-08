from flask import Flask, render_template, request, jsonify, redirect, url_for
from random import randint
import mysql.connector
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Database Configuration
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="food"
)
db_cursor = db_connection.cursor()

# HTML Template for Signup Page
signup_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Signup</title>
</head>
<body>
    <h1>Signup</h1>
    <form action="/signup" method="post">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br>
        <button type="submit">Signup</button>
    </form>
</body>
</html>
"""
# login template 
login_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>THE INDIAN BISTRO</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600&family=Oswald:wght@600&display=swap" rel="stylesheet">
   
    <!-- <link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet"> -->
    <link rel="stylesheet" href="css/tailwind.css">
    <link rel="stylesheet" href="css/tooplate-antique-cafe.css">
    
<!--

Tooplate 2126 Antique Cafe

https://www.tooplate.com/view/2126-antique-cafe

-->
</head>
<body>    
    <!-- Intro -->
    <div id="intro" class="parallax-window" data-parallax="scroll" data-image-src="img/antique-cafe-bg-01.jpg">
        <div class="container mx-auto px-2 tm-intro-width">
            <div class="sm:pb-60 sm:pt-48 py-20">
                <div class="bg-black bg-opacity-70 p-12 mb-5 text-center">
                    <h1 class="text-white text-5xl tm-logo-font mb-5">THE INDIAN BISTRO</h1>
                    <p class="tm-text-gold tm-text-2xl">where every bite tells a story!</p>
                    <div class="Login"><button id="loginBtn">Login</button></div>
                    <div class="login-container hidden" id="loginContainer">
                        <h2>Login</h2>
                        <form id="loginForm" action="login.php" method="post">
                            <div class="input-group">
                                <label for="username">Username:</label>
                                <input type="text" id="username" name="username" required>
                            </div>
                            <div class="input-group">
                                <label for="password">Password:</label>
                                <input type="password" id="password" name="password" required>
                            </div>
                            <button type="submit">Login</button>
                        </form>
                    </div>
                </div>                                         
            </div>
        </div>        
    </div>


    <script src="script.js"></script>
</div>
</div>        
</div>



    <script src="js/jquery-3.6.0.min.js"></script>
    <script src="js/parallax.min.js"></script>
    <script src="js/jquery.singlePageNav.min.js"></script>
    <script>

        function checkAndShowHideMenu() {
            if(window.innerWidth < 768) {
                $('#tm-nav ul').addClass('hidden');                
            } else {
                $('#tm-nav ul').removeClass('hidden');
            }
        }

        $(function(){
            var tmNav = $('#tm-nav');
            tmNav.singlePageNav();

            checkAndShowHideMenu();
            window.addEventListener('resize', checkAndShowHideMenu);

            $('#menu-toggle').click(function(){
                $('#tm-nav ul').toggleClass('hidden');
            });

            $('#tm-nav ul li').click(function(){
                if(window.innerWidth < 768) {
                    $('#tm-nav ul').addClass('hidden');
                }                
            });

            $(document).scroll(function() {
                var distanceFromTop = $(document).scrollTop();

                if(distanceFromTop > 100) {
                    tmNav.addClass('scroll');
                } else {
                    tmNav.removeClass('scroll');
                }
            });
            
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();

                    document.querySelector(this.getAttribute('href')).scrollIntoView({
                        behavior: 'smooth'
                    });
                });
            });
        });
    </script>

</body>
</html>
"""

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
        self.create_status_table()

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

    def create_status_table(self):
        # SQL command to create the "order" table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `track` (
            `order_id` INT,
            `status` VARCHAR(255) DEFAULT 'Preparing'
        )
        """
        self.db_cursor.execute(create_table_query)
        self.db_connection.commit()

    def insert_order_data(self, item, quantity ):
        # SQL command to insert order data into the "order" table
        insert_query = """
        INSERT INTO `order` (item_name, quantity)
        VALUES (%s, %s)
        """
        order_data = (item,quantity)
        self.db_cursor.execute(insert_query, order_data)
        self.db_connection.commit()

    def insert_bill_data(self,order_id, item, quantity ):
        # SQL command to insert order data into the "order" table
        insert_query = """
        INSERT INTO `data` (order_id, items, quantity)
        VALUES (%s,%s, %s)
        """
        bill_data = (order_id, item,quantity)
        self.db_cursor.execute(insert_query, bill_data)
        self.db_connection.commit()

    def insert_order_status(self, order_id, status):
        # SQL command to insert order status data into the "track" table
        insert_query = """
        INSERT INTO `track` (order_id, status)
        VALUES (%s, %s)
        """
        status_data = (order_id, status)
        self.db_cursor.execute(insert_query, status_data)
        self.db_connection.commit()

    def insert_cost_data(self,order_id,total ):
        # SQL command to insert order data into the "order" table
        insert_query = """
        INSERT INTO `bill` (order_id,total_cost)
        VALUES (%s, %s)
        """
        cost_data = (order_id,total)
        self.db_cursor.execute(insert_query,cost_data)
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
    
    def remove_order_item(self, item, quantity=None):
        if item in self.cart:
            if quantity is None or quantity >= self.cart[item]:
                del self.cart[item]
                return f"Removed all {item} from the order."
            else:
                self.cart[item] -= quantity
                return f"Removed {quantity} {item} from the order."
        else:
            return f"{item} is not in the order."
    
    def display_cart(self):
        if not self.cart:
            return "Your cart is empty."
        cart_items = "\n".join([f"{item.capitalize()}: {quantity}" for item, quantity in self.cart.items()])
        return f"Your cart:\n{cart_items}"
    
    def calculate_total(self):
        total = sum([self.menu[item]['price'] * quantity for item, quantity in self.cart.items()])
        return total 
    
    def place_order(self):
        if not self.cart:
            return "Your cart is empty. Please add items before placing the order."
        for item, quantity in self.cart.items():
            self.insert_order_data(item, quantity)
            
        order_id = randint(10, 999)  # Random 2 to 3 digit order ID
        total_cost = self.calculate_total()
        self.insert_cost_data(order_id,total_cost)
        self.insert_bill_data(order_id,item,quantity)
        self.insert_order_status(order_id,'perparing')
        self.cart.clear()
        return f"Your order has been placed. Order ID: #{order_id}. Thank you!"
        
            
    def final_order(self):
       total_cost = self.calculate_total()  # Calculate total cost
       order_summary = self.display_cart() + "\n" + "Your cost is: $" + str(total_cost) + "\n" + self.place_order()  # Convert total_cost to string
    # Assuming self.place_order() stores the order data in the database
       self.place_order()  # Call the place_order function to store data in the database
       return order_summary

    def track_order(self):
        # Assuming a simple tracking mechanism
        return "Your order is being prepared. It will be delivered shortly."
    
    def chat(self, user_input):
        response = ""
        if any(greeting in user_input for greeting in ["hi", "hello", "hey"]):
            response = "Hello! How can I assist you today?"
        elif user_input == "bye" or user_input == "goodbye":
            response = "Goodbye! Have a great day!"
        elif user_input in ["display menu", "menu", "show menu", "give menu"]:
            response = self.display_menu()
        elif user_input.startswith("add"):
            parts = user_input.split()
            if len(parts) == 3 and parts[1] == "to" and parts[2] == "menu":
                response = self.add_to_menu(parts[0], 0)  # Assuming price is not specified
            else:
                response = "Invalid input. Please use the format: 'add <item> to menu'."
        elif user_input.startswith("order"):
            parts = user_input.split()
            if len(parts) == 2:
                response = self.order(parts[1])
            elif len(parts) == 3 and parts[2].isdigit():
                response = self.order(parts[1], int(parts[2]))
            else:
                response = "Invalid input. Please use the format: 'order <item> [quantity]'."
        
        elif user_input.startswith("remove"):
            parts = user_input.split()
            if len(parts) == 2:
                response = self.remove_order_item(parts[1])
            elif len(parts) == 3 and parts[2].isdigit():
                response = self.remove_order_item(parts[1], int(parts[2]))
            else:
                response = "Invalid input. Please use the format: 'remove <item> [quantity]'."
            
            # Code for removing items from cart
        elif user_input in ["show cart", "display cart", "cart", "my orders"]:
            response = self.display_cart()
        elif user_input in ["calculate total", "total", "total price", "show bill", "bill"]:
            response = self.calculate_total()
        elif user_input in ["final order"]:
            response = self.final_order()
        elif user_input in ["track order", "where is my order", "check my order"]:
            response = self.track_order()
        elif user_input in ["track order status", "order status"]:
            response = "Sorry, we don't have a detailed tracking system at the moment."
        else:
            response = "I'm sorry, I didn't understand that. How can I assist you?"
        
        return response

chatbot = FoodChatbot()
@app.route('/')
def start():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password)
        
        # Check if the username already exists in the database
        db_cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = db_cursor.fetchone()
        
        if existing_user:
            return "Username already exists! Please choose a different username."
        else:
            # Insert the new user into the database
            insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            user_data = (username, hashed_password)
            db_cursor.execute(insert_query, user_data)
            db_connection.commit()
            
            return redirect(url_for('login'))  # Redirect to login page after signup
    else:
        return signup_template
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username exists in the database
        db_cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = db_cursor.fetchone()
        
        if user:
            # Verify the password
            stored_hashed_password = user[1]  # Assuming the hashed password is in the second column
            if check_password_hash(stored_hashed_password, password):
                # Password is correct
                if username == "admin1" and password == "123":  # Check for admin credentials
                    return redirect(url_for('admin_page'))  # Redirect to admin page
                else:
                    return redirect(url_for('chat_page'))  # Redirect to chat page for regular users
            else:
                return "Incorrect password. Please try again."
        else:
            return "Username not found. Please sign up."
    else:
        return render_template('login.html')



@app.route('/admin')
def admin_page():
    # Fetch user data from the database
    return render_template('admin.html')

@app.route('/admin_user')
def admin_user():
    db_cursor.execute("SELECT username FROM users")
    users = db_cursor.fetchall()
    return render_template('admin_user.html', users=users)

@app.route('/admin_orders')
def admin_orders_page():
    # Fetch data from the database
    db_cursor.execute("SELECT order_id, items, quantity FROM data")
    data = db_cursor.fetchall()
    return render_template('admin_orders.html', data=data)

@app.route('/admin_status')
def admin_status_page():
    # Fetch order IDs from the track table
    db_cursor.execute("SELECT order_id FROM track")
    orders = db_cursor.fetchall()
    return render_template('admin_status.html', orders=orders)

@app.route('/update_status', methods=['POST'])
def update_status():
    if request.method == 'POST':
        order_id = request.form['order_id']
        status = request.form['status']
        # Update status in the database (track table)
        update_query = "UPDATE track SET status = %s WHERE order_id = %s"
        db_cursor.execute(update_query, (status, order_id))
        db_connection.commit()
        return "Status updated successfully."
    else:
        return "Method not allowed"

@app.route('/chat', methods=['GET', 'POST'])
def chat_page():
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = chatbot.chat(user_input)
        return jsonify({'response': response})
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)