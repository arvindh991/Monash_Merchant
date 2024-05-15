import os
import pandas as pd

class Product:
    """
    Represents a product with all necessary attributes.

    Attributes:
        id (int): The unique identifier for the product.
        name (str): The name of the product.
        brand (str): The brand of the product.
        description (str): A description of the product.
        price (float): The price of the product.
        quantity (int): The available quantity of the product.
    """
    def __init__(self, id, name, brand, description, price, quantity):
        self.id = id
        self.name = name
        self.brand = brand
        self.description = description
        self.price = price
        self.quantity = quantity

class Cart:
    """
    Represents a shopping cart containing products.

    Attributes:
        store (Store): A reference to the store from which the cart can manipulate products.
        items (list): A list of tuples where each tuple contains a Product object and a quantity.
    """
    def __init__(self, store):
        self.items = []  # List to hold items in the cart.
        self.store = store  # Reference to the store for inventory management.

    def add_product(self, product, quantity):
        """
        Adds a product to the cart.

        Parameters:
            product (Product): The product to add to the cart.
            quantity (int): The quantity of the product to add.
        """
        if quantity <= 0:
            return  # Do not add if the quantity is non-positive.

        # Ensure there is sufficient stock before adding to cart.
        while quantity > product.quantity:
            print(f"Error: {product.name} is low on stock. Only {product.quantity} available.")
            try:
                new_quantity = int(input(f"Please enter a new quantity (available: {product.quantity}): "))
                if new_quantity <= 0:
                    continue  # Ensure new quantity is positive.
                quantity = new_quantity
            except ValueError:
                print("Invalid input. Please enter a valid integer for the quantity.")

        product.quantity -= quantity  # Decrement the stock.
        self.store.products_df.loc[
            self.store.products_df['product_id'] == product.id, 'product_quantity'] = product.quantity
        self.items.append((product, quantity))  # Add the product to the cart.
        print(f"\nAdded {quantity} of {product.name} to the cart.")

    def view_cart(self):
        """
        Displays the contents of the shopping cart.
        """
        if not self.items:
            print("Your cart is empty.")
            return

        product_info = {}
        for product, quantity in self.items:
            if product.name in product_info:
                product_info[product.name]['quantity'] += quantity
                product_info[product.name]['total_price'] += product.price * quantity
            else:
                product_info[product.name] = {
                    'quantity': quantity,
                    'total_price': product.price * quantity
                }
        total = sum(product.price * quantity for product, quantity in self.items)
        print("\nCart Contents:")
        for product_name, info in product_info.items():
            print(
                f"{info['quantity']} x {product_name} at ${info['total_price'] / info['quantity']:.2f} each (Total: ${info['total_price']:.2f})")
        print(f"Total due: ${total:.2f}")

    def checkout(self):
        """
        Processes the checkout by calculating the total and saving the product quantities back to the store.
        Allows the customer to choose between delivery and pickup options.

        Returns:
            bool: True if checkout is successful, False otherwise (e.g., if the cart is empty).
        """
        if not self.items:
            print("Your cart is empty. Please add some products before checking out.")
            return False

        self.view_cart()
        
        # Allow customer to choose between delivery and pickup
        while True:
            print("\nChoose an option to receive your order:")
            print("1. Delivery")
            print("2. Pickup")
            choice = input("Enter your choice (1 for Delivery, 2 for Pickup): ")

            if choice == '1':
                self.process_delivery()
                break
            elif choice == '2':
                self.process_pickup()
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        
        self.store.save_products()  # Save the updated product data.
        print("\nCheckout complete. Thank you for your purchase!")
        return True

    def process_delivery(self):
        """
        Handles the delivery option for checkout.
        """
        print("\nYou have selected Delivery.")
        # Simulate delivery process
        address = input("Please enter your delivery address: ")
        print(f"Your order will be delivered to: {address}")

    def process_pickup(self):
        """
        Handles the pickup option for checkout.
        """
        print("\nYou have selected Pickup.")
        # Simulate pickup process
        print("Your order will be ready for pickup at the store.")

class Store:
    def __init__(self):
        """
        Represents a store which manages products and a shopping cart.

        Attributes:
            filepath (str): The path to the product data file.
            products_df (DataFrame): A pandas DataFrame containing product data.
            products (list): A list of Product objects.
            cart (Cart): A shopping cart associated with the store.
        """
        self.filepath = self.prompt_for_filepath()  # Initialize file path on creation.
        self.products_df = self.load_products()  # Load products from the file.
        # Initialize products list by parsing data frame.
        self.products = [
            Product(row['product_id'], row['product_name'], row['product_brand'], row['product_description'],
                    row['product_price'], row['product_quantity']) for index, row in self.products_df.iterrows()]
        self.cart = Cart(self)  # Associate a cart with the store.

    def prompt_for_filepath(self):
        """
        Prompts the user to enter a valid file path for the products.csv file.

        Returns:
            str: A valid file path entered by the user.
        """
        while True:
            filepath = input("Enter the file path for products.csv: ")
            # Remove surrounding quotes and normalize path to be OS-independent
            cleaned_filepath = filepath.strip('\'"')  # Remove single and double quotes
            normalized_filepath = os.path.normpath(cleaned_filepath)

            # Check if the file path ends with 'products.csv'
            if not normalized_filepath.endswith('products.csv'):
                print("Error: File path must end with 'products.csv'. Please try again.")
                continue

            if os.path.exists(normalized_filepath):
                return normalized_filepath
            else:
                print("Error: The file path specified does not exist. Please try again.")

    def load_products(self):
        """
        Loads products from a CSV file into a DataFrame.

        Returns:
            DataFrame: The loaded product data.
        """
        try:
            df = pd.read_csv(self.filepath)
            df.columns = [col.strip() for col in df.columns]
            return df
        except FileNotFoundError:
            print("Error: The file path specified does not exist.")
            return pd.DataFrame()
        except Exception as e:
            print(f"Unexpected error loading products: {e}")
            return pd.DataFrame()

    def save_products(self):
        """
        Saves the updated product quantities back to the CSV file.
        """
        self.products_df.to_csv(self.filepath, index=False)  # Save the DataFrame to CSV.
        print("\nProduct quantities updated.")

    def display_products(self):
        """
        Displays all products available in the store.
        """
        print("\nAvailable Products:")
        for product in self.products:
            print(
                f"{product.id}. {product.name} - Brand: {product.brand} - Description: {product.description} - Price: ${product.price} - Available: {product.quantity}")

    def run(self):
        """
        Runs the main menu loop, allowing the user to add products to the cart, view the cart, or proceed to checkout.
        """
        # Main menu loop to manage store operations.
        while True:
            self.display_products()
            print("\nMenu:")
            print("1. Add a product to your cart")
            print("2. View your cart")
            print("3. Proceed to checkout")
            print("4. Return to Main Menu")
            user_input = input("\nEnter the number of your choice: ")

            if user_input == '1':
                # Product addition logic with input validation.
                while True:
                    try:
                        product_id = int(input("\nEnter the product ID: "))
                        break  # Break the loop if conversion to int succeeds
                    except ValueError:
                        print("Invalid input. Please enter a valid integer for the product ID.")

                # Quantity addition logic.
                while True:
                    try:
                        quantity = int(input("Enter the quantity: "))
                        break  # Break the loop if conversion to int succeeds
                    except ValueError:
                        print("Invalid input. Please enter a valid integer for the quantity.")

                product = next((p for p in self.products if p.id == product_id), None)
                if product:
                    self.cart.add_product(product, quantity)
                else:
                    print("Product not found.")

            elif user_input == '2':
                self.cart.view_cart()

            elif user_input == '3':
                # Checkout decision logic.
                while True:
                    print
