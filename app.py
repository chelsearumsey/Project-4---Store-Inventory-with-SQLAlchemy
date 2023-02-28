
from models import (Base, session,
                    Product, engine)
import csv
import datetime
import time


def menu():
    while True:
        print('''
            \nPRODUCT INVENTORY
            \r* Enter "v" to view specific product details
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


def clean_product_id(id_str, options):
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
        if product_id in options:
            return product_id
        else:
            input(f'''
            \n****** ID ERROR ******
            \rOptions: {options}
            \rPress enter to try again.
            \r************************''')
            return

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
    try:
        price_float = float(price_str)
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
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
            \n****** DATE ERROR ******
            \rThe date format should include a valid Month, Day, Year.
            \rExample: December 14, 2022
            \rPress enter to try again.
            \r************************''')
        return
    else:
        return return_date


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                product = row[0]
                quantity = row[1]
                price = clean_product_price(row[2])
                date = clean_date_updated(row[3])
                new_product = Product(product_name=product, product_quantity=quantity, product_price=price, date_updated=date)
                session.add(new_product)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            for product in session.query(Product):
                print(f'{product.product_id} | {product.product_name} | {product.product_quantity} | {product.product_price} | {product.date_updated}')
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
                date_updated = input('Date Updated: (Example: February 27, 2023): ')
                date = clean_date_updated(date_updated)
                if type(date) == datetime.date:
                    date_updated_error = False
            new_product = Product(product_name=product, product_quantity=quantity, product_price=price, date_updated=date)
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