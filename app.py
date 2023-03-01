
from models import (Base, session,
                    Product, engine)
import csv
import datetime
import time


def menu():
    while True:
        print('''
            \nPRODUCT INVENTORY
            \r* Enter "v" to view specific product details by product ID
            \r* Enter "a" to add a new product to the inventory
            \r* Enter "b" to make a backup of the entire inventory contents
            \r* Enter "e" to exit product inventory
            ''')
        choice = input('What would you like to do? ').lower()
        if choice in ['v', 'a', 'b', 'e']:
            return choice
        else:
            input('''
                \rPlease choose one of the options above. 
                \rPress enter to try again.
                ''')


def clean_product_id(id_str):
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
            \n****** ID ERROR ******
            \rThe id should be a number.
            \rPress enter to try again.
            \r************************''')
        return
    else:
        return product_id
        
def view_by_product_id(chosen_id):
    id_options = []
    for product in session.query(Product):
        id_options.append(product.product_id)
    id_error = True
    while id_error:   
        chosen_id = input(f'''
            \nId Options: {id_options}
            \rProduct id: ''')
        chosen_id = clean_product_id(chosen_id)
        if type(chosen_id) == int:
            id_error = False
    chosen_product = session.query(Product).filter(Product.id==chosen_id).first()
    print(f'''
        \n{chosen_product.product_name}
        \rQuantity: {chosen_product.product_quantity}
        \rPrice: ${chosen_product.product_price / 100}
        \rDate Updated: {chosen_product.date_updated}''')

def clean_product_quantity(quantity_str):
    try:
        product_quantity = int(quantity_str)
    except ValueError:
        input('''
            \n****** QUANTITY ERROR ******
            \rThe quantity should be a number.
            \rPress enter to try again.
            \r************************''')
    else:
        return int(product_quantity)

def clean_product_price(price_str):
    price_float = float(price_str.split('$')[1])
    try:
        price_float
    except ValueError:
        input('''
            \n****** PRICE ERROR ******
            \rThe price should be a number without a currency symbol.
            \rExample: 6.99
            \rPress enter to try again.
            \r************************''')
    else:
        return int(price_float * 100)
    
def clean_date_updated(date_str):
    clean_date = date_str.split('/')
    try:
        month = int(clean_date[0])
        day = int(clean_date[1])
        year = int(clean_date[2])
        clean_date = datetime.date(year, month, day)
    except ValueError:
        input('''
            \n****** DATE ERROR ******
            \rThe date format should include a valid numeric Month/Day/Year.
            \rExample: 12/14/2022
            \rPress enter to try again.
            \r************************''')
        return
    else:
        return clean_date


def add_csv():
    with open('inventory.csv', 'r', newline='') as csvfile:
        product_data = csv.reader(csvfile)
        # Referenced https://stackoverflow.com/questions/14674275/skip-first-linefield-in-loop-using-csv-file
        next(product_data)
        for row in product_data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                product = row[0]
                price = clean_product_price(row[1])
                quantity = row[2]
                date = clean_date_updated(row[3])
                new_product = Product(product_name=product, product_quantity=quantity, product_price=price, date_updated=date)
                session.add(new_product)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            chosen_id = input("Enter the id of the product you'd like to view. ")
            chosen_id = clean_product_id(chosen_id)
            view_by_product_id(chosen_id)
            input('Press enter to return to the main menu.')
        elif choice == 'a':
            product_name = input('Product: ')
            quantity_error = True
            while quantity_error:
                product_quantity = input('Quantity (Enter a whole number): ')
                quantity = clean_product_quantity(product_quantity)
                if type(quantity) == int:
                    quantity_error = False
            price_error = True
            while price_error:
                product_price = input('Price (Example: 9.99): ')
                price = clean_product_price(product_price)
                if type(price) == int:
                    price_error = False
            date_updated_error = True
            while date_updated_error:
                date_updated = input('Date Updated: (Example: 2/27/2023): ')
                date = clean_date_updated(date_updated)
                if type(date) == datetime.date:
                    date_updated_error = False
            new_product = Product(product_name=product_name, product_quantity=quantity, product_price=price, date_updated=date)
            session.add(new_product)
            session.commit()
            print('Product added!')
            time.sleep(1.5)
        elif choice == 'b':
            pass
        else:
            print('THANKS FOR CHECKING THE INVENTORY!')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()