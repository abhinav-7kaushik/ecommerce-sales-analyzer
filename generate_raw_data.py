import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

N = 2500

categories = ["Electronics", "Furniture", "Clothing", "Groceries", "Beauty", "Sports", "Toys", "Books"]
products_by_cat = {
    "Electronics": ["Phone", "Laptop", "Headphones", "Smartwatch", "Tablet"],
    "Furniture": ["Chair", "Table", "Sofa", "Bookshelf", "Bed"],
    "Clothing": ["T-shirt", "Jeans", "Jacket", "Shoes", "Cap"],
    "Groceries": ["Rice", "Oil", "Spices", "Snacks", "Beverages"],
    "Beauty": ["Lipstick", "Shampoo", "Perfume", "Face Cream", "Sunscreen"],
    "Sports": ["Football", "Cricket Bat", "Yoga Mat", "Dumbbells", "Tennis Racket"],
    "Toys": ["Lego Set", "Puzzle", "Action Figure", "Board Game", "RC Car"],
    "Books": ["Novel", "Comic", "Textbook", "Cookbook", "Biography"],
}
customers = [f"Customer_{i}" for i in range(1, 401)]

rows = []
for i in range(1, N + 1):
    cat = random.choice(categories)
    product = random.choice(products_by_cat[cat])
    customer = random.choice(customers)
    qty = random.randint(1, 5)
    base_price = random.randint(20, 1500)
    sales = base_price * qty
    date = pd.Timestamp("2023-01-01") + pd.Timedelta(days=random.randint(0, 730))

    # introduce inconsistent date formats
    fmt_choice = random.random()
    if fmt_choice < 0.6:
        date_str = date.strftime("%Y-%m-%d")
    elif fmt_choice < 0.85:
        date_str = date.strftime("%d/%m/%Y")
    else:
        date_str = date.strftime("%b %d, %Y")

    # introduce inconsistent sales formatting (currency symbols/commas as strings)
    sales_choice = random.random()
    if sales_choice < 0.15:
        sales_val = f"₹{sales:,}"
    elif sales_choice < 0.25:
        sales_val = f"{sales:,}"
    else:
        sales_val = sales

    rows.append({
        "OrderID": 1000 + i,
        "Date": date_str,
        "Customer": customer,
        "Category": cat,
        "Product": product,
        "Sales": sales_val,
        "Quantity": qty,
    })

df = pd.DataFrame(rows)

# introduce missing values (~6% of cells across key columns)
for col in ["Customer", "Product", "Sales", "Quantity", "Date"]:
    mask = np.random.rand(len(df)) < 0.03
    df.loc[mask, col] = np.nan

# introduce duplicate rows (~3%)
dupes = df.sample(frac=0.03, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

# shuffle
df = df.sample(frac=1, random_state=7).reset_index(drop=True)

df.to_csv("sales_data_raw.csv", index=False)
print("Raw rows generated:", len(df))
print(df.isnull().sum())
print("Exact duplicate rows:", df.duplicated().sum())
