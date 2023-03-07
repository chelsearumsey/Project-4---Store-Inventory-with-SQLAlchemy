
from models import (Base, session,
                    Product, engine)
import csv
import datetime
from datetime import date
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
                \rPlease choose a valid menu option. 
                \rPress enter to try again.
                ''')


def clean_product_id(id_str):
    try:
        clean_product_id = int(id_str)
    except ValueError:
        input('''
            \n****** ID ERROR ******
            \rThe id should be a number.
            \rPress enter to try again.
            \r************************''')
        return
    else:
        return clean_product_id
        

def clean_product_price(price_str):
    clean_product_price = float(price_str.split('$')[1])
    try:
        clean_product_price
    except ValueError:
        input('''
            \n****** PRICE ERROR ******
            \rThe price should be a number without a currency symbol.
            \rExample: 6.99
            \rPress enter to try again.
            \r************************''')
    else:
        return int(clean_product_price * 100)
    

def clean_new_product_price(price_str):
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
        return int(price_float *100)


def clean_product_quantity(quantity_str):
    try:
        clean_product_quantity = int(quantity_str)
    except ValueError:
        input('''
            \n****** QUANTITY ERROR ******
            \rThe quantity should be a number.
            \rPress enter to try again.
            \r************************''')
    else:
        return clean_product_quantity

    
def clean_date_updated(date_str):
    clean_date_updated = date_str.split('/')
    try:
        month = int(clean_date_updated[0])
        day = int(clean_date_updated[1])
        year = int(clean_date_updated[2])
        clean_date_updated = datetime.date(year, month, day)
    except ValueError:
        input('''
            \n****** DATE ERROR ******
            \rThe date format should include a valid numeric Month/Day/Year.
            \rExample: 12/14/2022
            \rPress enter to try again.
            \r************************''')
        return
    else:
        return clean_date_updated


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
                quantity = clean_product_quantity(row[2])
                date = clean_date_updated(row[3])
                new_product = Product(product_name=product, product_price=price, 
                                        product_quantity=quantity, date_updated=date)
                session.add(new_product)
            else:
                if product_in_db.date_updated < clean_date_updated(row[3]):
                    product_in_db.product_name = row[0]
                    product_in_db.product_price = clean_product_price(row[1])
                    product_in_db.product_quantity = clean_product_quantity(row[2])
                    product_in_db.date_updated = clean_date_updated(row[3])
        session.commit()


def view_by_product_id(chosen_id):
    id_options = []
    for product in session.query(Product):
        if product.product_id > 1:
            id_options.append(product.product_id)
    if chosen_id not in id_options:
        id_error = True
        while id_error:
            chosen_id = input(f'''
                \nThe product id you entered does not exist. 
                \rId Options: {id_options}
                \rProduct id: ''')
            chosen_id = clean_product_id(chosen_id)
            if type(chosen_id) == int and chosen_id in id_options:
                id_error = False
    chosen_product = session.query(Product).filter(Product.product_id==chosen_id).first()
   #Referenced https://www.enthought.com/no-zero-padding-with-strftime/
    print(f'''
        \n{chosen_product.product_name}
        \rPrice: ${chosen_product.product_price / 100}
        \rQuantity: {chosen_product.product_quantity}
        \rDate Updated: {chosen_product.date_updated.strftime("%#m/%#d/%Y")}''')
    

def add_backup_csv():
    with open('backup.csv', 'w', newline='') as csvfile:
        fieldnames = ['product_name', 'product_price', 'product_quantity',
                      'date_updated']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for product in session.query(Product).all():
            writer.writerow({
                'product_name': product.product_name,
                'product_price': '$' + str(product.product_price / 100),
                'product_quantity': product.product_quantity,
                'date_updated': product.date_updated.strftime("%m/%d/%Y")
                })
           

def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            chosen_id = input("Enter the id of the product you'd like to view. ")
            chosen_id = clean_product_id(chosen_id)
            view_by_product_id(chosen_id)
            time.sleep(1.5)
            input('Press enter to return to the main menu.')
        elif choice == 'a':
            product_name = input('Product: ')
            price_error = True
            while price_error: 
                product_price = input('Price (Example: 9.99): ')
                new_product_price = clean_new_product_price(product_price)
                if type(new_product_price) == int:
                    price_error = False
            quantity_error = True
            while quantity_error:
                product_quantity = input('Quantity (Enter a whole number): ')
                quantity = clean_product_quantity(product_quantity)
                if type(quantity) == int:
                    quantity_error = False
            current_date = date.today() 
            product_in_db = session.query(Product).filter(Product.product_name==product_name).one_or_none()
            if product_in_db == None:
                new_product = Product(product_name=product_name, product_quantity=quantity, 
                                product_price=new_product_price, date_updated=current_date)
                session.add(new_product) 
                print('Product added!')
            else:
                if product_in_db.date_updated < current_date:
                    product_in_db.product_name = product_name
                    product_in_db.product_price = new_product_price
                    product_in_db.product_quantity = quantity
                    product_in_db.date_updated = current_date
                    print('Product updated!')
            session.commit()
            time.sleep(1.5)
        elif choice == 'b':
            add_backup_csv()
            time.sleep(1.5)
            print('Backup completed!')
        elif choice =='e':
            print('THANKS FOR CHECKING THE INVENTORY!')
            app_running = False    


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
    add_backup_csv()
    
