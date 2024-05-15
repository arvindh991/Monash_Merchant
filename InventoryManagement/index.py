import pandas as pd
from pathlib import Path

class ProductManager:
    def __init__(self):
        self.data_dir = Path("data")
        self.categories_file = self.data_dir / "categories.csv"
        self.subcategories_file = self.data_dir / "subcategories.csv"
        self.products_file = self.data_dir / "products.csv"

        self.initialize_files()

    def initialize_files(self):
        self.data_dir.mkdir(exist_ok=True)

        
        if not self.products_file.exists():
            pd.DataFrame(columns=["product_id", "product_name", "product_brand", 
                                  "product_description", "product_price", 
                                  "product_member_price", "product_quantity", 
                                  "product_category", "product_sub_category", 
                                  "product_expiry", "product_ingridients", 
                                  "product_storage_instructions", "product_allergens"]).to_csv(self.products_file, index=False)

        if not self.categories_file.exists():
            pd.DataFrame(columns=["category_id", "category_name"]).to_csv(self.categories_file, index=False)

        if not self.subcategories_file.exists():
            pd.DataFrame(columns=["subcategory_id", "subcategory_name"]).to_csv(self.subcategories_file, index=False)
    
    def user_interface(self):
        while True:
            print("\nProduct Management System")
            print("1. Add Category")
            print("2. Add Sub-Category")
            print("3. Add Product")
            print("4. Display Products")
            print("5. Update Product")
            print("6. Delete Product")
            print("7. Exit")
            choice = input("Choose an action: ")
            if choice == '1':
                category_name = input("Enter new Category Name (or X to cancel): ")
                if category_name.lower() != 'x':
                    self.add_category(category_name)
            elif choice == '2':
                subcategory_name = input("Enter new Sub-Category Name (or X to cancel): ")
                if subcategory_name.lower() != 'x':
                    self.add_subcategory(subcategory_name)
            elif choice == '3':
                self.add_product_ui()
            elif choice == '4':
                self.display_products()
            elif choice == '5':
                self.update_product()
            elif choice == '6':
                self.delete_product()
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")

    def add_category(self, category_name):
        df = pd.read_csv(self.categories_file)
        if category_name in df['category_name'].values:
            print('Category already exists!!')
            return
        new_row = pd.DataFrame({'category_id': [df['category_id'].max() + 1 if not df.empty else 1], 'category_name': [category_name]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.categories_file, index=False)
        print(f"Successfully added category: {category_name}")

    def add_subcategory(self, subcategory_name):
        df = pd.read_csv(self.subcategories_file)
        if subcategory_name in df['subcategory_name'].values:
            print('Sub-Category already exists!!')
            return
        new_row = pd.DataFrame({'subcategory_id': [df['subcategory_id'].max() + 1 if not df.empty else 1], 'subcategory_name': [subcategory_name]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.subcategories_file, index=False)
        print(f"Successfully added sub-category: {subcategory_name}")

    def add_product_ui(self):
        print('----------------')
        print("Add a new Product")
        print('----------------\n\n')

        product_info = {}
        is_food = input('Is Product sub-category food? (Y/n): ')
        print('\n')
        
        while is_food.lower() not in {'y', 'n', 'yes', 'no'}:
            print('PLEASE ENTER A VALID RESPONSE (Y/n)')
            is_food = input('Is Product sub-category food? (Y/n): ')
            print('\n')

        # General product information
        product_info['product_name'] = input('Enter Product Name (or X to cancel): ')
        if product_info['product_name'].lower() == 'x': return
        product_info['product_brand'] = input('Enter Product Brand (or X to cancel): ')
        if product_info['product_brand'].lower() == 'x': return
        product_info['product_description'] = input('Enter Product Description (or X to cancel): ')
        if product_info['product_description'].lower() == 'x': return
        product_info['product_price'] = input('Enter Product Price (or X to cancel): ')
        if product_info['product_price'].lower() == 'x': return
        product_info['product_member_price'] = input('Enter Product Member Price (or X to cancel): ')
        if product_info['product_member_price'].lower() == 'x': return
        product_info['product_quantity'] = input('Enter Product Quantity (or X to cancel): ')
        if product_info['product_quantity'].lower() == 'x': return
        product_info['product_category'] = input('Enter Product Category (or X to cancel): ')
        if product_info['product_category'].lower() == 'x': return

        
        if is_food.lower() in {'y', 'yes'}:
            product_info['product_sub_category'] = 'food'
            product_info['product_expiry'] = input('Enter Product Expiry Date (or X to cancel): ')
            if product_info['product_expiry'].lower() == 'x': return
            product_info['product_ingredients'] = input('Enter Product Ingredients (or X to cancel): ')
            if product_info['product_ingredients'].lower() == 'x': return
            product_info['product_storage_instructions'] = input('Enter Product Storage Instructions (or X to cancel): ')
            if product_info['product_storage_instructions'].lower() == 'x': return
            product_info['product_allergens'] = input('Enter Product Allergens (if any) or X to cancel: ')
            if product_info['product_allergens'].lower() == 'x': return
        else:
            product_info['product_sub_category'] = input('Enter Product Sub-Category (or X to cancel): ')
            if product_info['product_sub_category'].lower() == 'x': return
         
            product_info['product_expiry'] = product_info['product_ingredients'] = product_info['product_storage_instructions'] = product_info['product_allergens'] = ''

        self.add_product(product_info)


    def add_product(self, product_info):
        df = pd.read_csv(self.products_file)
        if product_info['product_name'] in df['product_name'].values:
            print('Product already exists!')
            return
        product_info['product_id'] = df['product_id'].max() + 1 if not df.empty else 1
        new_row = pd.DataFrame([product_info])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.products_file, index=False)
        print(f"Successfully added product: {product_info['product_name']}")

    def display_products(self):
        df = pd.read_csv(self.products_file)
        if df.empty:
            print('No products available.')
            return
        print("\nAvailable Products:\n-------------------")
        for index, row in df.iterrows():
            print(f"ID: {row['product_id']}")
            print(f"Name: {row['product_name']}")
            print(f"Brand: {row['product_brand']}")
            print(f"Description: {row['product_description']}")
            print(f"Price: {row['product_price']}")
            print(f"Member Price: {row['product_member_price']}")
            print(f"Quantity: {row['product_quantity']}")
            print(f"Category: {row['product_category']}")
            print(f"Sub-Category: {row['product_sub_category']}")
            print(f"Expiry: {row['product_expiry']}")
            print(f"Ingredients: {row.get('product_ingredients', '')}")
            print(f"Storage Instructions: {row.get('product_storage_instructions', '')}")
            print(f"Allergens: {row.get('product_allergens', '')}")
            print("-------------------\n")

    def update_product(self):
        self.display_products()
        product_id = input('Enter the Product ID you want to update (or X to cancel): ')
        if product_id.lower() == 'x': return
        df = pd.read_csv(self.products_file)
        product_id = int(product_id)
        if not product_id in df['product_id'].values:
            print('Product ID does not exist.')
            return
            
        print("Enter the name of the field you want to update (or X to cancel): ")
        for column in df.columns:
            print(column)
        field_name = input().strip()
        if field_name.lower() == 'x' or field_name not in df.columns:
            print('Operation cancelled or incorrect field name.')
            return
        
        new_value = input(f'Enter new value for {field_name} (or X to cancel): ')
        if new_value.lower() == 'x': return
        
        df.loc[df['product_id'] == product_id, field_name] = new_value
        df.to_csv(self.products_file, index=False)
        print(f"Product with ID {product_id} has been updated.")

    def delete_product(self):
        self.display_products()
        product_id = input('Enter the Product ID you want to delete (or X to cancel): ')
        if product_id.lower() == 'x': return
        df = pd.read_csv(self.products_file)
        product_id = int(product_id)
        if not product_id in df['product_id'].values:
            print('Product ID does not exist.')
            return
        df = df[df['product_id'] != product_id]
        df.to_csv(self.products_file, index=False)
        print(f'Product with ID {product_id} has been deleted.')


