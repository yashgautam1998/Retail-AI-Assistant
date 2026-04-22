from datetime import datetime
from tools.order_tools import get_order
from tools.product_tools import get_product

from datetime import datetime

def evaluate_return(order_id: str):
    order = get_order(order_id)
    if not order:
        return {"error": "Order not found"}

    product = get_product(order["product_id"])
    if not product:
        return {"error": "Product not found"}

    order_date = datetime.strptime(order["order_date"], "%Y-%m-%d")
    days_since = (datetime.now() - order_date).days

    vendor = product["vendor"]

    result = {
        "eligible": False,
        "type": None,
        "reason": "",
        "days_since": days_since
    }

    # 🔴 Clearance (highest priority)
    if product["is_clearance"]:
        result["reason"] = "Clearance item → final sale (no return allowed)"
        return result

    # 🟣 Vendor: Aurelia Couture
    if vendor == "Aurelia Couture":
        result["eligible"] = True
        result["type"] = "exchange_only"
        result["reason"] = "Vendor policy: exchange only (no refunds)"
        return result

    # 🟣 Vendor: Nocturne
    if vendor == "Nocturne":
        if days_since <= 21:
            result["eligible"] = True
            result["type"] = "refund"
            result["reason"] = "Nocturne has extended 21-day return window"
        else:
            result["reason"] = "Return window expired (21-day limit)"
        return result

    # 🟡 Sale items
    if product["is_sale"]:
        if days_since <= 7:
            result["eligible"] = True
            result["type"] = "store_credit"
            result["reason"] = "Sale items returnable within 7 days for store credit"
        else:
            result["reason"] = "Sale return window expired (7 days)"
        return result

    # 🟢 Normal items
    if days_since <= 14:
        result["eligible"] = True
        result["type"] = "refund"
        result["reason"] = "Standard 14-day return policy"
    else:
        result["reason"] = "Return window expired (14 days)"

    return result