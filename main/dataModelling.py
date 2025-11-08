from faker import Faker
from typing import List
from datetime import timedelta, datetime
import json, random


fake = Faker(locale='en_US')
Faker.seed(42)
fake.seed_instance(123)

def time_created_updated(start_date:str='2y', end_date:str='now', start_day:int=0, end_day:int= 365):
    created_at = fake.date_time_between(start_date=f'-{start_date}', end_date=f'{end_date}')
    updateed_at = created_at + timedelta(days=random.randint(start_day, end_day))
    return created_at, updateed_at

def generate_sku(category:int, supplier:int):
    number = random.randint(1000, 9999)
    return f"{category}-{supplier}-{number}"



def category_data(num:int):
    material:List = ['Human hair', "Synthetic", 'Fibre']
    category_type:list = ['Closure', 'Frontal']
    category = [
        {
            'id': i+1,
            'style': fake.color_name(),
            'category_type': random.choice(category_type),
            'material': random.choice(material),
            'description': fake.text(20),
            'created-at': fake.date_between(start_date='-1y', end_date='today').isoformat()
        } for i in range(num+1)
    ]
    return category

def generate_suppliers_json(num_suppliers):
    created_at = fake.date_time_between(start_date='-2y', end_date='now')
    updated_at = created_at + timedelta(days=random.randint(0, 365))
    suppliers = [
        {
            "id": i+1,
            "name": fake.company(),
            "contact_person": fake.name(),
            "email": fake.company_email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat(),
            "items": [],      # Empty for now, can be filled with Item data
            "purchases": []   # Empty for now, can be filled with Purchase data
        }
        for i in range(num_suppliers)
    ]
    return suppliers

def warehouse_data(nums:int=3):
    created_at = fake.date_time_between(start_date='-2y', end_date='now')
    updated_at = created_at + timedelta(days=random.randint(0, 365))
    warehouse:List[dict] = [
        {
            "id": i+1,
            "name": f"{fake.city()} Warehouse",
            "location": fake.address(),
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat(),
            "purchases": [],        # Can be linked to Purchase data later
            "sales": [],            # Can be linked to Sale data later
            "stock_movements": []   # Can be linked to StockMovement data later
        } for i in range(nums)
    ]
    return warehouse

def customer_data(nums:int):
    created_at, updated_at = time_created_updated()
    customers = [
        {
            "id": i+1,
            "name": fake.name(),
            "email": fake.unique.email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "customer_type": random.choice(["single", "corporate", "wholesale"]),
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat()
        } for i in range(nums)
    ]
    return customers

def items_data(nums:int):
    created_at, updated_at = time_created_updated()
    category_ids = [i for i in range(1, nums+1)]
    supplier_ids = [i for i in range(1, nums+1)]
    products = [
        {
            "id": i+1,
            "name": fake.unique.word().title(),
            "sku": f"SKU-{fake.unique.random_int(min=1000, max=9999)}",
            "description": fake.sentence(nb_words=10),
            "category_id": random.choice(category_ids),
            "supplier_id": random.choice(supplier_ids),
            "unit_price": float(round(random.uniform(5.0, 1500.0), 2)),
            "quantity": random.randint(0, 100),
            "reorder_level": random.randint(5, 20),
            "status": random.choice(["active", "inactive"]),
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat()
        } for i in range(nums)
    ]
    return products

def transaction_data(nums:int=5):
    created_at, updated_at = time_created_updated('6M', 'now', 0, 30)
    item_ids = [i+1 for i in range(nums)]
    warehouse_ids= [i+1 for i in range(3)]
    movemnt = [
        {
            "id": i+1,
            "item_id": random.choice(item_ids),
            "warehouse_id": random.choice(warehouse_ids),
            "movement_type": random.choice(["IN", "OUT"]),
            "quantity": random.randint(1, 50),
            "reference": fake.sentence(nb_words=6),
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat()
        } for i in range(nums)
    ]
    return movemnt

def sales_data(nums:int = 10):
    created_at, updated_at = time_created_updated('6m', 'now', 0, 30)
    total_amount = round(random.uniform(50.0, 5000.0), 2)
    customer_ids = [i for i in range(1, nums+1)]
    warehouse_ids = [i for i in range(1, 4)]
    sale = [
        {
            "id": i,
            "customer_id": random.choice(customer_ids),
            "warehouse_id": random.choice(warehouse_ids),
            "sale_date": created_at.isoformat(),
            "sale_type": random.choice(["retail", "wholesale"]),
            "total_amount": total_amount,
            "status": random.choice(["completed", "pending", "cancelled"]),
            "reference": fake.bothify(text="REF-#####"),
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat()
        } for i in range(1, nums+1)
    ]
    return sale

def purchases_data(nums:int = 20):
    created_at, updated_at = time_created_updated('6m', 'now', 0, 30)
    supplier_ids = [i for i in range(nums+1)]
    warehouse_ids = [1,2,3]
    total_amount = round(random.uniform(100.0 , 10000.0), 2)
    purchase= [
        {
            "id": i,
            "supplier_id": random.choice(supplier_ids),
            "warehouse_id": random.choice(warehouse_ids),
            "purchase_date": created_at.isoformat(),
            "total_amount": total_amount,
            "status": random.choice(["completed", "pending", "cancelled"]),
            "reference": fake.bothify(text="PUR-#####"),
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat()
        } for i in range(1, nums+1)
    ]
    return purchase



def write_to_file(directroy, data):
    with open(directroy, 'w') as f:
        json.dump(data, f, indent=4)

def create_file(filename:str, nums:int=10) -> None:
    data:dict = {
        'products': items_data(nums),
        'categories': category_data(nums),
        'suppliers': generate_suppliers_json(nums),
        'customers': customer_data(nums),
        'warehouse': warehouse_data(),
        'transactions': transaction_data(),
        'sales': sales_data(),
        'purchase': purchases_data(),
    }
    print("Creating file...")
    try:
        write_to_file(filename, data)
        print("File Created successfully")
    except Exception as e:
        print("Somthing went wrong, possible cause: ", e)
    

if __name__ == '__main__':
    create_file("./json/free_model.json")