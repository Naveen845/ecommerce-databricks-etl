import csv
import random
from datetime import date, timedelta
from pathlib import Path


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
SAMPLE_DIR = BASE_DIR / "data" / "sample"


# Create directories if they don't exist
RAW_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Configuration
# -----------------------------

NUM_CUSTOMERS = 100
NUM_PRODUCTS = 50
NUM_ORDERS = 1000

random.seed(42)


# -----------------------------
# Helper functions
# -----------------------------

def random_date(start_date, end_date):
    days = (end_date - start_date).days
    random_days = random.randint(0, days)

    return start_date + timedelta(days=random_days)


# -----------------------------
# Generate Customers
# -----------------------------

def generate_customers():
    customers = []

    cities = [
        "Hyderabad",
        "Bengaluru",
        "Chennai",
        "Mumbai",
        "Delhi",
        "Pune",
        "Kolkata",
        "Ahmedabad",
    ]

    states = {
        "Hyderabad": "Telangana",
        "Bengaluru": "Karnataka",
        "Chennai": "Tamil Nadu",
        "Mumbai": "Maharashtra",
        "Delhi": "Delhi",
        "Pune": "Maharashtra",
        "Kolkata": "West Bengal",
        "Ahmedabad": "Gujarat",
    }

    start_date = date(2023, 1, 1)
    end_date = date(2024, 12, 31)

    for i in range(1, NUM_CUSTOMERS + 1):
        city = random.choice(cities)

        customer = {
            "customer_id": f"CUST{i:04d}",
            "customer_name": f"Customer {i}",
            "email": f"customer{i}@example.com",
            "city": city,
            "state": states[city],
            "registration_date": random_date(start_date, end_date),
        }

        customers.append(customer)

    return customers


# -----------------------------
# Generate Products
# -----------------------------

def generate_products():
    products = []

    product_categories = {
        "Electronics": [
            "Laptop",
            "Smartphone",
            "Headphones",
            "Keyboard",
            "Mouse",
        ],
        "Fashion": [
            "T-Shirt",
            "Jeans",
            "Shoes",
            "Jacket",
            "Watch",
        ],
        "Home": [
            "Table",
            "Chair",
            "Lamp",
            "Mixer",
            "Bedsheet",
        ],
        "Books": [
            "Python Book",
            "Java Book",
            "SQL Book",
            "Data Engineering Book",
            "AI Book",
        ],
        "Grocery": [
            "Rice",
            "Oil",
            "Coffee",
            "Tea",
            "Snacks",
        ],
    }

    product_id = 1

    for category, names in product_categories.items():

        for name in names:

            for variant in range(1, 3):

                price = round(random.uniform(100, 50000), 2)

                product = {
                    "product_id": f"PROD{product_id:04d}",
                    "product_name": f"{name} {variant}",
                    "category": category,
                    "price": price,
                }

                products.append(product)

                product_id += 1

    return products


# -----------------------------
# Generate Orders
# -----------------------------

def generate_orders(customers, products):
    orders = []

    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)

    payment_methods = [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Net Banking",
        "Cash on Delivery",
    ]

    statuses = [
        "Completed",
        "Shipped",
        "Pending",
        "Cancelled",
    ]

    for i in range(1, NUM_ORDERS + 1):

        customer = random.choice(customers)
        product = random.choice(products)

        order = {
            "order_id": f"ORD{i:06d}",
            "customer_id": customer["customer_id"],
            "product_id": product["product_id"],
            "order_date": random_date(start_date, end_date),
            "quantity": random.randint(1, 5),
            "discount": round(random.uniform(0, 0.30), 2),
            "payment_method": random.choice(payment_methods),
            "status": random.choice(statuses),
        }

        orders.append(order)

    return orders


# -----------------------------
# Introduce bad records
# -----------------------------

def introduce_bad_records(orders):
    # Duplicate order
    orders.append(orders[0].copy())

    # Missing customer ID
    bad_order = orders[1].copy()
    bad_order["order_id"] = "ORD_BAD001"
    bad_order["customer_id"] = ""
    orders.append(bad_order)

    # Negative quantity
    bad_order = orders[2].copy()
    bad_order["order_id"] = "ORD_BAD002"
    bad_order["quantity"] = -5
    orders.append(bad_order)

    # Invalid status
    bad_order = orders[3].copy()
    bad_order["order_id"] = "ORD_BAD003"
    bad_order["status"] = "UNKNOWN"
    orders.append(bad_order)

    return orders


# -----------------------------
# Write CSV
# -----------------------------

def write_csv(file_path, data):
    if not data:
        return

    with open(file_path, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=data[0].keys()
        )

        writer.writeheader()
        writer.writerows(data)


# -----------------------------
# Main program
# -----------------------------

def main():

    print("Generating customers...")

    customers = generate_customers()

    print("Generating products...")

    products = generate_products()

    print("Generating orders...")

    orders = generate_orders(
        customers,
        products
    )

    print("Adding bad records...")

    orders = introduce_bad_records(orders)

    # Write raw datasets
    write_csv(
        RAW_DIR / "customers.csv",
        customers
    )

    write_csv(
        RAW_DIR / "products.csv",
        products
    )

    write_csv(
        RAW_DIR / "orders.csv",
        orders
    )

    # Create smaller sample dataset
    sample_orders = orders[:20]

    write_csv(
        SAMPLE_DIR / "orders_sample.csv",
        sample_orders
    )

    print()
    print("===================================")
    print("Data generation completed!")
    print("===================================")

    print(f"Customers : {len(customers)}")
    print(f"Products  : {len(products)}")
    print(f"Orders    : {len(orders)}")

    print()
    print("Files created:")
    print(RAW_DIR / "customers.csv")
    print(RAW_DIR / "products.csv")
    print(RAW_DIR / "orders.csv")
    print(SAMPLE_DIR / "orders_sample.csv")


if __name__ == "__main__":
    main()