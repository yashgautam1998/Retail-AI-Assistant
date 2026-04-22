import pandas as pd

products_df = pd.read_csv("data/product_inventory.csv")


def search_products(filters: dict):
    df = products_df.copy()

    def apply_filters(df, filters):
        temp = df.copy()

        if "max_price" in filters:
            temp = temp[temp["price"] <= filters["max_price"]]

        if "size" in filters:
            size = str(filters["size"])
            temp = temp[temp["sizes_available"].str.contains(size, na=False)]

            def has_stock(stock_str):
                stock = eval(stock_str)
                return stock.get(size, 0) > 0

            temp = temp[temp["stock_per_size"].apply(has_stock)]

        if filters.get("is_sale"):
            temp = temp[temp["is_sale"] == True]

        if "tags" in filters:
            tag_matches = pd.Series(False, index=temp.index)
            for tag in filters["tags"]:
                tag_matches |= temp["tags"].str.contains(tag, case=False, na=False)
            temp = temp[tag_matches]

        return temp

    # 🔍 Step 1: strict
    result = apply_filters(df, filters)

    # 🔥 Step 2: fallback (remove sale)
    if result.empty and filters.get("is_sale"):
        relaxed = filters.copy()
        relaxed.pop("is_sale")
        result = apply_filters(df, relaxed)

    # 🔥 Step 3: fallback (remove tags)
    if result.empty and "tags" in filters:
        relaxed = filters.copy()
        relaxed.pop("tags")
        result = apply_filters(df, relaxed)

    result = result.sort_values(by="bestseller_score", ascending=False)

    return result.head(5).to_dict(orient="records")

def get_product(product_id: int):
    product = products_df[products_df["product_id"] == product_id]
    if product.empty:
        return None
    return product.iloc[0].to_dict()