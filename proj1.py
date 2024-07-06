class Product:
    '''This class represents a product in the inventory'''
    def __init__(self, id, name, category, price, quantity):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def update_quantity(self, quantity):
        ''' This method is to update the quantity in Products '''
        self.quantity += quantity

    def update_price(self, price):
        ''' This method is to update the quantity in Products '''
        self.price = price

    def __str__(self):
        return f"Product [ID: {self.id}, Name: {self.name}, Category: {self.category}, Price: {self.price}, Quantity: {self.quantity}]"


class Inventory:
    ''' This class is used to store the items and do add, update, remove, get and list the product '''
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product.id] = product

    def update_product(self, id, name=None, category=None, price=None, quantity=None):
        if id in self.products:
            if name is not None:
                self.products[id].name = name
            if category is not None:
                self.products[id].category = category
            if price is not None:
                self.products[id].price = price
            if quantity is not None:
                self.products[id].quantity = quantity
        else:
            print(f"Product with ID {id} does not exist.")

    def remove_product(self, id):
        if id in self.products:
            del self.products[id]
        else:
            print(f"Product with ID {id} does not exist.")

    def get_product(self, id):
        return self.products.get(id, None)

    def list_products(self):
        return list(self.products.values())


from datetime import datetime

class Transaction:
    ''' This class is to do transactions '''
    def __init__(self, transaction_id, product, quantity):
        self.transaction_id = transaction_id
        self.product = product
        self.quantity = quantity
        self.date = datetime.now()

    def process(self):
        raise NotImplementedError("Subclass must implement abstract method")


class Sale(Transaction):
    ''' this class is to represent the quantity of the product '''
    def process(self):
        if self.product.quantity >= self.quantity:
            self.product.update_quantity(-self.quantity)
        else:
            print(f"Not enough stock for Product ID {self.product.id}")


class Return(Transaction):
    ''' this class is to represents the returning the product '''
    def process(self):
        self.product.update_quantity(self.quantity)


from fpdf import FPDF
''' importing the PDF files from FPDF '''
class Invoice:
    ''' this class is used to create invoice '''
    def __init__(self, invoice_id, transactions):
        self.invoice_id = invoice_id
        self.transactions = transactions
        self.date = datetime.now()

    def generate_pdf(self, filename):
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Invoice ID: {self.invoice_id}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Date: {self.date}", ln=True, align="L")
        pdf.cell(200, 10, txt="", ln=True, align="L")

        for transaction in self.transactions:
            product = transaction.product
            quantity = transaction.quantity
            pdf.cell(200, 10, txt=f"Product: {product.name}, Quantity: {quantity}, Total: {quantity * product.price}", ln=True, align="L")

        pdf.output(filename)


# Create inventory and add products
inventory = Inventory()
product1 = Product(1, "Laptop", "Electronics", 1000, 50)
product2 = Product(2, "Mouse", "Electronics", 20, 200)
inventory.add_product(product1)
inventory.add_product(product2)

# Process a sale
sale1 = Sale(1, product1, 5)
sale1.process()

# Process a return
return1 = Return(2, product2, 10)
return1.process()

# Generate an invoice
invoice = Invoice(1, [sale1, return1])
invoice.generate_pdf("invoice_1.pdf")

# List all products
for product in inventory.list_products():
    print(product)
    
import csv
## to generate csv report
headers = ["Name", "Price", "Quantity"]
fp = open('report.csv', 'w')
w=csv.writer(fp)
w.writerow(headers)
for p in inventory.list_products():
    w.writerow([p.name, p.price, p.quantity])
