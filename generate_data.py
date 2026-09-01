import pandas as pd
import random

# 1. Generate FAQs
faqs = [
    (1, "How do I track my order?", "Use the Track Order page with your order ID."),
    (2, "Where is my parcel?", "Use the Track Order page with your order ID."),
    (3, "How do I return my order?", "Initiate a return within 7 days from My Orders."),
    (4, "Can I cancel my order?", "Orders can be cancelled before shipment."),
    (5, "How long is delivery?", "Delivery usually takes 3-7 business days."),
    (6, "Do you offer COD?", "Yes, Cash on Delivery is available for selected locations."),
    (7, "How can I contact support?", "Email support@example.com or use live chat."),
    (8, "Is there a warranty?", "Warranty depends on the product and brand."),
    (9, "Can I change my address?", "You can update the address before shipment."),
    (10, "How do I get a refund?", "Refunds are processed after successful return inspection."),
    (11, "Do you ship internationally?", "Currently domestic shipping only."),
    (12, "How do I reset my password?", "Use the Forgot Password option."),
    (13, "Can I exchange a product?", "Exchange is available for eligible products."),
    (14, "What payment methods are accepted?", "UPI, Cards, Net Banking and COD."),
    (15, "How do I download invoice?", "Invoices are available in My Orders."),
    (16, "Are products genuine?", "Yes, all products are sourced from authorized sellers."),
    (17, "How to apply coupon?", "Apply the coupon during checkout."),
    (18, "How to check stock?", "Product pages display stock availability."),
    (19, "Can I preorder?", "Preorder is available for selected products."),
    (20, "How do I delete my account?", "Contact customer support.")
]

df_faq = pd.DataFrame(faqs, columns=["FAQID", "Question", "Answer"])
df_faq.to_csv("data/faq.csv", index=False)

# 2. Generate Products
brands = {
    "Lenovo": "Laptop", "HP": "Laptop", "Dell": "Laptop", "ASUS": "Laptop", "Acer": "Laptop",
    "Samsung": "Mobile", "Apple": "Mobile", "OnePlus": "Mobile", "Xiaomi": "Mobile", "Realme": "Mobile",
    "Sony": "Headphones", "Boat": "Headphones", "JBL": "Headphones", "Noise": "Headphones", "boAt": "Headphones",
    "Samsung Smartwatch": "Smartwatch", "Noise Smartwatch": "Smartwatch", "Fire-Boltt": "Smartwatch", "Apple Smartwatch": "Smartwatch", "Amazfit": "Smartwatch"
}

products = []
pid = 1
for brand, category in brands.items():
    for i in range(1, 6):
        name = f"{brand} {i}"
        price = random.randint(10000, 90000) if category in ["Laptop", "Mobile"] else random.randint(1000, 10000)
        desc = f"{category} by {brand} suitable for everyday use and offers quality performance."
        rating = round(random.uniform(3.5, 4.9), 1)
        products.append((pid, name, category, brand, price, desc, rating))
        pid += 1

df_products = pd.DataFrame(products, columns=["ProductID", "ProductName", "Category", "Brand", "Price", "Description", "Rating"])
df_products.to_csv("data/products.csv", index=False)

# 3. Generate Reviews
reviews = []
review_id = 1
review_texts = [
    ("Excellent product", 5), ("Works perfectly", 5), ("Very good quality", 4), 
    ("Worth the money", 4), ("Average quality", 3), ("Disappointing purchase", 2),
    ("Not worth the price", 2), ("Poor battery", 1), ("Stopped working soon", 1),
    ("Highly recommended", 5)
]

for p in products:
    pid = p[0]
    pname = p[1]
    # Generate 10 reviews per product
    for _ in range(10):
        text, rating = random.choice(review_texts)
        reviews.append((review_id, pid, pname, text, rating))
        review_id += 1

df_reviews = pd.DataFrame(reviews, columns=["ReviewID", "ProductID", "ProductName", "Review", "Rating"])
df_reviews.to_csv("data/reviews.csv", index=False)

print("Datasets generated successfully!")
