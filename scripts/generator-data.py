import os
import csv
import json
import random
from datetime import datetime, timedelta


def generate_sample_ecommerce_data(
    num_users,
    num_products,
    num_orders,
    num_sessions,
    output_dir="/home/alino/Desktop/bootcamp/smaple-project/data",
):
    random.seed(42)

    users_dir = output_dir
    behavioral_dir = os.path.join(output_dir, "behavioral")

    os.makedirs(users_dir, exist_ok=True)
    os.makedirs(behavioral_dir, exist_ok=True)

    users_path = os.path.join(users_dir, "users.csv")
    products_path = os.path.join(users_dir, "products.csv")
    orders_path = os.path.join(users_dir, "orders.csv")

    first_names = [
        "Albert", "Todd", "Lindsey", "Dawn", "Anthony", "Joseph", "Sarah",
        "Lindsay", "Caleb", "Olivia", "Noah", "Emma", "Mason", "Sophia"
    ]
    last_names = [
        "Todd", "Davidson", "Hansen", "Rodriguez", "Bryant", "Donaldson",
        "Miranda", "Roth", "Washington", "Smith", "Johnson", "Brown"
    ]
    domains = ["example.com", "example.net", "example.org"]
    devices = ["mobile", "desktop", "tablet"]
    loyalty_tiers = ["Bronze", "Silver", "Gold"]
    categories = ["Electronics", "Home", "Clothing", "Beauty", "Gaming"]
    payment_methods = ["credit_card", "paypal", "apple_pay"]
    order_statuses = ["completed"]
    shipping_methods = ["standard", "express", "next_day"]
    url_paths = [
        "/", "/home", "/cart", "/help", "/faq", "/deals", "/black-friday",
        "/best-sellers", "/category/clothing", "/category/beauty",
        "/category/gaming", "/category/electronics/laptops",
        "/search?q=headphones"
    ]
    search_queries = [
        "back to school deals", "best laptop under 1000", "black hoodie",
        "nintendo switch accessories", "summer dress", "cargo pants",
        "desk lamp", "oversized t shirt", "wireless earbuds", "gaming mouse"
    ]
    city_prefixes = ["New", "Lake", "East", "West", "North", "South"]
    city_names = [
        "Andrewfort", "Kimberlymouth", "Melissa", "James", "Christopher",
        "Tabithaside", "Geoffreyview", "Riverdale", "Oakville"
    ]
    states = ["MD", "SG", "ND", "DE", "MA", "FR", "TX"]

    def rand_date(start, end):
        delta = end - start
        seconds = random.randint(0, int(delta.total_seconds()))
        return start + timedelta(seconds=seconds)

    def make_email(first, last):
        return f"{first.lower()}{last.lower()}{random.randint(1,99)}@{random.choice(domains)}"

    def make_location():
        return f"{random.choice(city_prefixes)} {random.choice(city_names)}, {random.choice(states)}"

    def make_product_name():
        adjectives1 = ["Assimilated", "Polarized", "Synergized", "Organic", "Focused", "Pre-emptive", "Object-based", "Exclusive", "Streamlined"]
        adjectives2 = ["static", "zero-defect", "intermediate", "attitude-oriented", "tangible", "disintermediate", "bottom-line", "human-resource"]
        nouns = ["Internet solution", "core", "function", "forecast", "capability", "success", "archive", "groupware", "task-force"]
        return f"{random.choice(adjectives1)} {random.choice(adjectives2)} {random.choice(nouns)}"

    # -------------------
    # Generate users
    # -------------------
    users = []
    user_ids = []

    signup_start = datetime(2024, 1, 1)
    signup_end = datetime(2026, 5, 1)

    for i in range(1, num_users + 1):
        user_id = f"U{1000 + i}"
        first = random.choice(first_names)
        last = random.choice(last_names)
        name = f"{first} {last}"
        email = make_email(first, last)
        signup_date = rand_date(signup_start, signup_end).date().isoformat()
        device = random.choice(devices)
        loyalty_tier = random.choices(loyalty_tiers, weights=[0.6, 0.3, 0.1])[0]
        location = make_location()

        users.append({
            "user_id": user_id,
            "name": name,
            "email": email,
            "signup_date": signup_date,
            "device": device,
            "loyalty_tier": loyalty_tier,
            "location": location,
        })
        user_ids.append(user_id)

    with open(users_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "user_id", "name", "email", "signup_date", "device", "loyalty_tier", "location"
        ])
        writer.writeheader()
        writer.writerows(users)

    # -------------------
    # Generate products
    # -------------------
    products = []
    product_ids = []

    for i in range(1, num_products + 1):
        product_id = f"P{1000 + i}"
        products.append({
            "product_id": product_id,
            "name": make_product_name(),
            "price": round(random.uniform(10, 2000), 2),
            "category": random.choice(categories),
            "inventory": random.randint(0, 500),
            "popularity_score": round(random.uniform(0.01, 0.99), 2),
        })
        product_ids.append(product_id)

    with open(products_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "product_id", "name", "price", "category", "inventory", "popularity_score"
        ])
        writer.writeheader()
        writer.writerows(products)

    product_lookup = {p["product_id"]: p for p in products}

    # -------------------
    # Generate orders
    # -------------------
    orders = []
    order_ids = []

    order_start = datetime(2026, 5, 20, 0, 0, 0)
    order_end = datetime(2026, 5, 21, 23, 59, 59)

    for i in range(1, num_orders + 1):
        order_id = f"O{1000 + i}"
        user_id = random.choice(user_ids)
        timestamp = rand_date(order_start, order_end).isoformat(timespec="seconds")
        total = round(random.uniform(15, 1800), 2)
        status = random.choice(order_statuses)
        payment_method = random.choice(payment_methods)

        orders.append({
            "order_id": order_id,
            "user_id": user_id,
            "timestamp": timestamp,
            "total": total,
            "status": status,
            "payment_method": payment_method,
        })
        order_ids.append(order_id)

    with open(orders_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "order_id", "user_id", "timestamp", "total", "status", "payment_method"
        ])
        writer.writeheader()
        writer.writerows(orders)

    # -------------------
    # Generate behavioral session JSONL files
    # -------------------
    session_start = datetime(2026, 4, 21, 0, 0, 0)
    session_end = datetime(2026, 5, 21, 23, 59, 59)

    def make_page_view(ts, user_id, device, session_id):
        return {
            "timestamp": ts.isoformat(timespec="seconds"),
            "user_id": user_id,
            "event_type": "page_view",
            "device": device,
            "session_id": session_id,
            "url_path": random.choice(url_paths),
            "duration_sec": random.randint(1, 180),
            "http_status": 200,
        }

    def make_search(ts, user_id, device, session_id):
        return {
            "timestamp": ts.isoformat(timespec="seconds"),
            "user_id": user_id,
            "event_type": "product_search",
            "device": device,
            "session_id": session_id,
            "query": random.choice(search_queries),
            "results_count": random.randint(5, 80),
            "clicked_position": random.randint(1, 15),
        }

    def make_wishlist(ts, user_id, device, session_id):
        return {
            "timestamp": ts.isoformat(timespec="seconds"),
            "user_id": user_id,
            "event_type": "wishlist_add",
            "device": device,
            "session_id": session_id,
            "product_id": random.choice(product_ids),
            "wishlist_name": "default",
        }

    def make_add_to_cart(ts, user_id, device, session_id, product_id, cart_count):
        return {
            "timestamp": ts.isoformat(timespec="seconds"),
            "user_id": user_id,
            "event_type": "add_to_cart",
            "device": device,
            "session_id": session_id,
            "product_id": product_id,
            "quantity": 1,
            "cart_total_items": cart_count,
        }

    def make_remove_from_cart(ts, user_id, device, session_id, product_id, cart_count):
        return {
            "timestamp": ts.isoformat(timespec="seconds"),
            "user_id": user_id,
            "event_type": "remove_from_cart",
            "device": device,
            "session_id": session_id,
            "product_id": product_id,
            "quantity": 1,
            "cart_total_items": cart_count,
        }

    def make_cart_view(ts, user_id, device, session_id, cart):
        cart_items = []
        total = 0.0
        for pid in cart:
            price = product_lookup[pid]["price"]
            cart_items.append({
                "product_id": pid,
                "price": price,
                "quantity": 1
            })
            total += price

        return {
            "timestamp": ts.isoformat(timespec="seconds"),
            "user_id": user_id,
            "event_type": "cart_view",
            "device": device,
            "session_id": session_id,
            "cart_items": cart_items,
            "cart_value": round(total, 2) if random.random() > 0.2 else 0,
        }

    def make_checkout_start(ts, user_id, device, session_id, cart):
        total = round(sum(product_lookup[pid]["price"] for pid in cart), 2)
        return {
            "timestamp": ts.isoformat(timespec="seconds"),
            "user_id": user_id,
            "event_type": "checkout_start",
            "device": device,
            "session_id": session_id,
            "shipping_method": random.choice(shipping_methods),
            "cart_value": total,
        }

    def make_payment_attempt(ts, user_id, device, session_id):
        success = random.random() > 0.1
        return {
            "timestamp": ts.isoformat(timespec="seconds"),
            "user_id": user_id,
            "event_type": "payment_attempt",
            "device": device,
            "session_id": session_id,
            "payment_type": random.choice(payment_methods),
            "success": success,
            "error_code": None if success else random.choice(["DECLINED", "TIMEOUT", "CVV_FAILED"]),
        }

    def make_order_complete(ts, user_id, device, session_id, order_id):
        return {
            "timestamp": ts.isoformat(timespec="seconds"),
            "user_id": user_id,
            "event_type": "order_complete",
            "device": device,
            "session_id": session_id,
            "order_id": order_id,
            "fulfillment_speed": random.choice(shipping_methods),
        }

    for i in range(num_sessions):
        user_id = random.choice(user_ids)
        user_device = next(u["device"] for u in users if u["user_id"] == user_id)
        start_ts = rand_date(session_start, session_end)
        session_id = f"session_{start_ts.strftime('%Y%m%d_%H%M%S')}_{user_id}"
        file_name = f"{user_id}_{session_id}.json"
        file_path = os.path.join(behavioral_dir, file_name)

        events = []
        cart = []

        ts = start_ts
        event_count = random.randint(15, 45)

        for _ in range(event_count):
            ts += timedelta(seconds=random.randint(1, 60))

            possible_events = ["page_view", "product_search", "wishlist_add", "cart_view", "add_to_cart"]
            if cart:
                possible_events += ["remove_from_cart", "checkout_start"]

            event_type = random.choice(possible_events)

            if event_type == "page_view":
                events.append(make_page_view(ts, user_id, user_device, session_id))

            elif event_type == "product_search":
                events.append(make_search(ts, user_id, user_device, session_id))

            elif event_type == "wishlist_add":
                events.append(make_wishlist(ts, user_id, user_device, session_id))

            elif event_type == "add_to_cart":
                pid = random.choice(product_ids)
                cart.append(pid)
                events.append(make_add_to_cart(ts, user_id, user_device, session_id, pid, len(cart)))

            elif event_type == "remove_from_cart" and cart:
                pid = random.choice(cart)
                cart.remove(pid)
                events.append(make_remove_from_cart(ts, user_id, user_device, session_id, pid, len(cart)))

            elif event_type == "cart_view":
                events.append(make_cart_view(ts, user_id, user_device, session_id, cart))

            elif event_type == "checkout_start" and cart:
                events.append(make_checkout_start(ts, user_id, user_device, session_id, cart))

                ts += timedelta(seconds=random.randint(5, 20))
                payment_event = make_payment_attempt(ts, user_id, user_device, session_id)
                events.append(payment_event)

                if payment_event["success"]:
                    ts += timedelta(seconds=random.randint(5, 20))
                    order_id = f"O{random.randint(1500, 9999)}"
                    events.append(make_order_complete(ts, user_id, user_device, session_id, order_id))
                    cart.clear()

        with open(file_path, "w", encoding="utf-8") as f:
            for event in events:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"Generated users: {users_path}")
    print(f"Generated products: {products_path}")
    print(f"Generated orders: {orders_path}")
    print(f"Generated session files in: {behavioral_dir}")


if __name__ == "__main__":
    generate_sample_ecommerce_data(
        output_dir="../data",
        num_users=90,
        num_products=200,
        num_orders=450,
        num_sessions=800,
    )
