import pandas as pd

orders_df = pd.read_csv("data/orders.csv")

def get_order(order_id):
    df = orders_df.copy()

    # Convert to string for safe comparison
    order_id = str(order_id)

    # Try exact match first
    order = df[df["order_id"] == order_id]

    if order.empty:
        # Try numeric fallback (e.g., 2 → O0002)
        if order_id.isdigit():
            formatted_id = f"O{int(order_id):04d}"
            order = df[df["order_id"] == formatted_id]

    if order.empty:
        return None

    return order.iloc[0].to_dict()