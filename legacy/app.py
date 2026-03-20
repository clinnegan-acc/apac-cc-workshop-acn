"""
Factory Inventory Management System - Legacy Flask Application
Single-file monolith serving JSON API endpoints.
"""
import json
import os
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Data loading — JSON files in data/ directory, held in memory
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def _load(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        return json.load(f)


def _save(filename, data):
    with open(os.path.join(DATA_DIR, filename), "w") as f:
        json.dump(data, f, indent=2)


inventory_items = _load("inventory.json")
orders = _load("orders.json")
demand_forecasts = _load("demand_forecasts.json")
backlog_items = _load("backlog_items.json")
spending_data = _load("spending.json")
spending_summary = spending_data["spending_summary"]
monthly_spending = spending_data["monthly_spending"]
category_spending = spending_data["category_spending"]
recent_transactions = _load("transactions.json")
purchase_orders = _load("purchase_orders.json")

# ---------------------------------------------------------------------------
# Quarter mapping
# ---------------------------------------------------------------------------
QUARTER_MAP = {
    "Q1-2025": ["2025-01", "2025-02", "2025-03"],
    "Q2-2025": ["2025-04", "2025-05", "2025-06"],
    "Q3-2025": ["2025-07", "2025-08", "2025-09"],
    "Q4-2025": ["2025-10", "2025-11", "2025-12"],
}


def filter_by_month(items, month):
    if not month or month == "all":
        return items
    if month.startswith("Q") and month in QUARTER_MAP:
        months = QUARTER_MAP[month]
        return [i for i in items if any(m in i.get("order_date", "") for m in months)]
    return [i for i in items if month in i.get("order_date", "")]


def apply_filters(items, warehouse=None, category=None, status=None):
    filtered = items
    if warehouse and warehouse != "all":
        filtered = [i for i in filtered if i.get("warehouse") == warehouse]
    if category and category != "all":
        filtered = [i for i in filtered if i.get("category", "").lower() == category.lower()]
    if status and status != "all":
        filtered = [i for i in filtered if i.get("status", "").lower() == status.lower()]
    return filtered


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def root():
    return jsonify({"message": "Factory Inventory Management System API", "version": "1.0.0"})


@app.route("/api/inventory")
def get_inventory():
    warehouse = request.args.get("warehouse")
    category = request.args.get("category")
    return jsonify(apply_filters(inventory_items, warehouse, category))


@app.route("/api/inventory/<item_id>")
def get_inventory_item(item_id):
    item = next((i for i in inventory_items if i["id"] == item_id), None)
    if not item:
        abort(404)
    return jsonify(item)


@app.route("/api/orders")
def get_orders():
    warehouse = request.args.get("warehouse")
    category = request.args.get("category")
    status = request.args.get("status")
    month = request.args.get("month")
    result = apply_filters(orders, warehouse, category, status)
    result = filter_by_month(result, month)
    return jsonify(result)


@app.route("/api/orders/<order_id>")
def get_order(order_id):
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        abort(404)
    return jsonify(order)


@app.route("/api/demand")
def get_demand():
    return jsonify(demand_forecasts)


@app.route("/api/backlog")
def get_backlog():
    result = []
    for item in backlog_items:
        d = dict(item)
        d["has_purchase_order"] = any(po["backlog_item_id"] == item["id"] for po in purchase_orders)
        result.append(d)
    return jsonify(result)


@app.route("/api/dashboard/summary")
def get_dashboard_summary():
    warehouse = request.args.get("warehouse")
    category = request.args.get("category")
    status = request.args.get("status")
    month = request.args.get("month")

    fi = apply_filters(inventory_items, warehouse, category)
    fo = filter_by_month(apply_filters(orders, warehouse, category, status), month)

    return jsonify({
        "total_inventory_value": round(sum(i["quantity_on_hand"] * i["unit_cost"] for i in fi), 2),
        "low_stock_items": len([i for i in fi if i["quantity_on_hand"] <= i["reorder_point"]]),
        "pending_orders": len([o for o in fo if o["status"] in ("Processing", "Backordered")]),
        "total_backlog_items": len(backlog_items),
        "total_orders_value": sum(o["total_value"] for o in fo),
    })


@app.route("/api/spending/summary")
def get_spending_summary():
    return jsonify(spending_summary)


@app.route("/api/spending/monthly")
def get_monthly_spending():
    return jsonify(monthly_spending)


@app.route("/api/spending/categories")
def get_category_spending():
    return jsonify(category_spending)


@app.route("/api/spending/transactions")
def get_recent_transactions():
    return jsonify(recent_transactions)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
