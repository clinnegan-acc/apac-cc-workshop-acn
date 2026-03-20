#!/usr/bin/env python3
"""
+============================================================+
|  FACTORY INVENTORY MANAGEMENT SYSTEM v2.1.3                |
|  (c) 1997 FactorySoft Solutions Inc.                       |
|  Licensed to: ACME Manufacturing Corp                      |
|  WARNING: Unauthorized access is prohibited!               |
+============================================================+

Terminal interface - connects directly to JSON data files.
"""
import json
import os
import sys
import time

# ---------------------------------------------------------------------------
# "Configuration" - hardcoded paths, naturally
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ANSI - but only the ugly ones
BOLD = "\033[1m"
DIM = "\033[2m"
BLINK = "\033[5m"
REVERSE = "\033[7m"
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BG_BLUE = "\033[44m"
BG_RED = "\033[41m"


def _load(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        return json.load(f)


def _save(filename, data):
    with open(os.path.join(DATA_DIR, filename), "w") as f:
        json.dump(data, f, indent=2)


# ---------------------------------------------------------------------------
# Fake slow output for that authentic legacy feel
# ---------------------------------------------------------------------------
def slow_print(text, delay=0.008):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def loading_bar(label="Loading", width=30, duration=1.0):
    sys.stdout.write(f"\n  {label} [")
    for i in range(width):
        sys.stdout.write("#")
        sys.stdout.flush()
        time.sleep(duration / width)
    sys.stdout.write("] DONE\n\n")


def beep():
    sys.stdout.write("\a")
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# Screen drawing helpers
# ---------------------------------------------------------------------------
def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")


def draw_box(lines, width=62, title=None):
    """Draw a single-line ASCII box around text."""
    print("+" + "-" * width + "+")
    if title:
        t = f"  {title}  "
        pad = width - len(t)
        print("|" + t + " " * pad + "|")
        print("+" + "-" * width + "+")
    for line in lines:
        text = line[:width]
        pad = width - len(text)
        print("|  " + text + " " * (pad - 2) + "|")
    print("+" + "-" * width + "+")


def draw_header():
    clear_screen()
    print(f"{BG_BLUE}{WHITE}{BOLD}")
    print("+==============================================================+")
    print("|     FACTORY INVENTORY MANAGEMENT SYSTEM  v2.1.3              |")
    print("|     (c) 1997 FactorySoft Solutions Inc.                      |")
    print("|     Serial: FSI-4829-ACME-MFG                               |")
    print("+==============================================================+")
    print(f"{RESET}")
    print(f"  {DIM}Terminal: {os.environ.get('TERM', 'vt100')}   "
          f"User: {os.environ.get('USER', 'OPERATOR')}   "
          f"Session: {os.getpid()}{RESET}")
    print()


def press_enter():
    input(f"\n  {DIM}<<< Press [ENTER] to continue >>>{RESET} ")


def draw_table(headers, rows, col_widths=None):
    """Draw a truly hideous ASCII table."""
    if not col_widths:
        col_widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=4)) + 2
                      for i, h in enumerate(headers)]
        # Cap widths
        col_widths = [min(w, 25) for w in col_widths]

    sep = "+" + "+".join("-" * w for w in col_widths) + "+"

    # Header
    print(sep)
    hdr = "|"
    for i, h in enumerate(headers):
        hdr += f"{BOLD}{str(h)[:col_widths[i]-1].center(col_widths[i])}{RESET}|"
    print(hdr)
    print(sep)

    # Rows
    for row in rows:
        line = "|"
        for i, cell in enumerate(row):
            text = str(cell)[:col_widths[i] - 1]
            line += f" {text}{' ' * (col_widths[i] - len(text) - 1)}|"
        print(line)

    print(sep)
    print(f"  {DIM}{len(rows)} record(s) returned{RESET}")


# ---------------------------------------------------------------------------
# Data views
# ---------------------------------------------------------------------------

def view_dashboard():
    draw_header()
    loading_bar("Aggregating data from all modules", duration=1.5)

    inventory = _load("inventory.json")
    orders_data = _load("orders.json")
    backlog = _load("backlog_items.json")

    total_inv_value = sum(i["quantity_on_hand"] * i["unit_cost"] for i in inventory)
    low_stock = [i for i in inventory if i["quantity_on_hand"] <= i["reorder_point"]]
    pending = [o for o in orders_data if o["status"] in ("Processing", "Backordered")]

    print(f"  {REVERSE} DASHBOARD SUMMARY {RESET}")
    print()
    print(f"  +{'='*56}+")
    print(f"  |  {'METRIC':<35} {'VALUE':>17}  |")
    print(f"  +{'-'*56}+")
    print(f"  |  {'Total Inventory Value':<35} {'$'+format(total_inv_value, ',.2f'):>17}  |")
    print(f"  |  {'Total Items in Stock':<35} {sum(i['quantity_on_hand'] for i in inventory):>17,}  |")
    print(f"  |  {'Low Stock Alerts':<35} {YELLOW if low_stock else ''}{len(low_stock):>17}{RESET}  |")
    print(f"  |  {'Pending Orders':<35} {len(pending):>17}  |")
    print(f"  |  {'Backlog Items':<35} {RED}{len(backlog):>17}{RESET}  |")
    print(f"  |  {'Total Orders (all time)':<35} {len(orders_data):>17}  |")
    print(f"  +{'='*56}+")

    if low_stock:
        print(f"\n  {BLINK}{YELLOW}*** WARNING: {len(low_stock)} ITEM(S) BELOW REORDER POINT ***{RESET}")
        for item in low_stock:
            print(f"    {RED}! {item['sku']} - {item['name']}: "
                  f"{item['quantity_on_hand']} on hand (reorder at {item['reorder_point']}){RESET}")

    press_enter()


def view_inventory():
    draw_header()
    loading_bar("Querying inventory database", duration=1.2)

    inventory = _load("inventory.json")

    print(f"  {REVERSE} INVENTORY LISTING {RESET}")
    print(f"  {DIM}Showing all {len(inventory)} items across all warehouses{RESET}\n")

    headers = ["SKU", "Name", "Category", "Warehouse", "Qty", "Reorder", "Unit $", "Status"]
    rows = []
    for item in inventory:
        qty = item["quantity_on_hand"]
        reorder = item["reorder_point"]
        status = f"{RED}LOW{RESET}" if qty <= reorder else f"{GREEN}OK{RESET}"
        rows.append([
            item["sku"],
            item["name"][:22],
            item["category"][:14],
            item["warehouse"][:12],
            str(qty),
            str(reorder),
            f"${item['unit_cost']:.2f}",
            status,
        ])

    draw_table(headers, rows, col_widths=[10, 24, 16, 14, 7, 8, 10, 8])
    press_enter()


def view_orders():
    draw_header()
    loading_bar("Fetching order records", duration=1.0)

    orders_data = _load("orders.json")

    # Filter submenu
    print(f"  {REVERSE} ORDER FILTER OPTIONS {RESET}\n")
    print("  [1] All Orders")
    print("  [2] Delivered")
    print("  [3] Shipped")
    print("  [4] Processing")
    print("  [5] Backordered")
    print()
    choice = input("  Select filter [1-5]: ").strip()

    status_map = {"2": "Delivered", "3": "Shipped", "4": "Processing", "5": "Backordered"}
    if choice in status_map:
        orders_data = [o for o in orders_data if o["status"] == status_map[choice]]
        loading_bar(f"Filtering by status={status_map[choice]}", duration=0.5)

    print(f"\n  {REVERSE} ORDERS ({len(orders_data)} records) {RESET}\n")

    # Only show first 25 - pagination is "not implemented yet"
    display = orders_data[:25]
    headers = ["Order #", "Customer", "Status", "Date", "Value"]
    rows = []
    for o in display:
        rows.append([
            o["order_number"],
            o["customer"][:20],
            o["status"],
            o["order_date"][:10],
            f"${o['total_value']:,.2f}",
        ])

    draw_table(headers, rows, col_widths=[18, 22, 14, 12, 14])

    if len(orders_data) > 25:
        print(f"\n  {YELLOW}*** Showing 25 of {len(orders_data)} records. "
              f"Pagination not available in this version. ***{RESET}")
        print(f"  {DIM}Contact IT dept for full export (Form IT-2847){RESET}")

    press_enter()


def view_demand():
    draw_header()
    loading_bar("Computing demand forecasts", duration=0.8)

    forecasts = _load("demand_forecasts.json")

    print(f"  {REVERSE} DEMAND FORECAST REPORT {RESET}\n")

    headers = ["SKU", "Item Name", "Current", "Forecast", "Trend", "Period"]
    rows = []
    for f in forecasts:
        trend = f["trend"]
        if trend == "increasing":
            trend_display = f"{RED}^ INCREASING{RESET}"
        elif trend == "decreasing":
            trend_display = f"{GREEN}v decreasing{RESET}"
        else:
            trend_display = f"{YELLOW}- stable{RESET}"
        rows.append([
            f["item_sku"],
            f["item_name"][:22],
            str(f["current_demand"]),
            str(f["forecasted_demand"]),
            trend_display,
            f["period"],
        ])

    draw_table(headers, rows, col_widths=[10, 24, 9, 10, 18, 14])
    press_enter()


def view_backlog():
    draw_header()
    loading_bar("Checking backlog status", duration=0.6)

    backlog = _load("backlog_items.json")

    print(f"  {BLINK}{RED}*** BACKLOG ALERT ***{RESET}\n")
    print(f"  {REVERSE} BACKLOG ITEMS ({len(backlog)} outstanding) {RESET}\n")

    headers = ["Order ID", "SKU", "Item", "Need", "Avail", "Short", "Days Late", "Priority"]
    rows = []
    for b in backlog:
        shortage = b["quantity_needed"] - b["quantity_available"]
        priority = b["priority"]
        if priority == "high":
            pri_display = f"{RED}HIGH{RESET}"
        else:
            pri_display = f"{YELLOW}MED{RESET}"
        rows.append([
            b["order_id"],
            b["item_sku"],
            b["item_name"][:18],
            str(b["quantity_needed"]),
            str(b["quantity_available"]),
            str(shortage),
            str(b["days_delayed"]),
            pri_display,
        ])

    draw_table(headers, rows, col_widths=[16, 10, 20, 7, 7, 7, 10, 10])
    press_enter()


def view_spending():
    draw_header()
    loading_bar("Generating financial reports", duration=1.8)

    spending = _load("spending.json")
    summary = spending["spending_summary"]
    monthly = spending["monthly_spending"]
    categories = spending["category_spending"]

    print(f"  {REVERSE} SPENDING OVERVIEW - FY2025 {RESET}\n")

    print(f"  +{'='*56}+")
    print(f"  |  {'COST CENTER':<30} {'TOTAL':>12} {'CHG%':>8}  |")
    print(f"  +{'-'*56}+")
    print(f"  |  {'Procurement':<30} {'$'+format(summary['total_procurement_cost'], ',.0f'):>12} {'+'+str(summary['procurement_change'])+'%':>8}  |")
    print(f"  |  {'Operational':<30} {'$'+format(summary['total_operational_cost'], ',.0f'):>12} {'+'+str(summary['operational_change'])+'%':>8}  |")
    print(f"  |  {'Labor':<30} {'$'+format(summary['total_labor_cost'], ',.0f'):>12} {'+'+str(summary['labor_change'])+'%':>8}  |")
    print(f"  |  {'Overhead':<30} {'$'+format(summary['total_overhead'], ',.0f'):>12} {'+'+str(summary['overhead_change'])+'%':>8}  |")
    print(f"  +{'='*56}+")

    total = (summary['total_procurement_cost'] + summary['total_operational_cost'] +
             summary['total_labor_cost'] + summary['total_overhead'])
    print(f"  |  {'GRAND TOTAL':<30} {BOLD}{'$'+format(total, ',.0f'):>12}{RESET}          |")
    print(f"  +{'='*56}+")

    # Monthly bar chart - ugly ASCII style
    print(f"\n  {REVERSE} MONTHLY PROCUREMENT TREND {RESET}\n")
    max_val = max(m["procurement"] for m in monthly)
    for m in monthly:
        bar_len = int((m["procurement"] / max_val) * 35)
        bar = "#" * bar_len
        print(f"  {m['month']:>4} |{CYAN}{bar}{RESET} ${m['procurement']:>10,}")

    # Category breakdown
    print(f"\n  {REVERSE} SPENDING BY CATEGORY {RESET}\n")
    headers = ["Category", "Amount", "% Total", "YoY Change"]
    rows = []
    for c in categories:
        rows.append([
            c["category"],
            f"${c['amount']:,.0f}",
            f"{c['percentage']}%",
            f"+{c['change']}%",
        ])
    draw_table(headers, rows, col_widths=[18, 14, 10, 12])

    press_enter()


def add_inventory_item():
    draw_header()
    print(f"  {REVERSE} ADD NEW INVENTORY ITEM {RESET}\n")
    print(f"  {DIM}Fill in all fields. Press Ctrl+C to cancel.{RESET}\n")

    try:
        inventory = _load("inventory.json")
        new_id = str(max(int(i["id"]) for i in inventory) + 1)

        sku = input("  SKU code     : ").strip()
        name = input("  Item name    : ").strip()
        category = input("  Category     : ").strip()
        warehouse = input("  Warehouse    : ").strip()
        qty = input("  Qty on hand  : ").strip()
        reorder = input("  Reorder point: ").strip()
        unit_cost = input("  Unit cost $  : ").strip()
        location = input("  Location     : ").strip()

        if not all([sku, name, category, warehouse, qty, reorder, unit_cost]):
            print(f"\n  {RED}ERROR: All fields are required!{RESET}")
            beep()
            press_enter()
            return

        new_item = {
            "id": new_id,
            "sku": sku,
            "name": name,
            "category": category,
            "warehouse": warehouse,
            "quantity_on_hand": int(qty),
            "reorder_point": int(reorder),
            "unit_cost": float(unit_cost),
            "location": location,
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }

        inventory.append(new_item)
        loading_bar("Writing to data file", duration=1.5)
        _save("inventory.json", inventory)

        print(f"  {GREEN}SUCCESS: Item {sku} added to inventory (ID: {new_id}){RESET}")
        beep()

    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Operation cancelled by user.{RESET}")
    except (ValueError, TypeError) as e:
        print(f"\n  {RED}INPUT ERROR: {e}{RESET}")
        beep()

    press_enter()


def search_orders():
    draw_header()
    print(f"  {REVERSE} ORDER SEARCH {RESET}\n")

    query = input("  Enter order # or customer name: ").strip().lower()
    if not query:
        return

    loading_bar(f"Searching {len(_load('orders.json'))} records", duration=1.0)

    orders_data = _load("orders.json")
    results = [o for o in orders_data
               if query in o.get("order_number", "").lower()
               or query in o.get("customer", "").lower()]

    if not results:
        print(f"  {YELLOW}No records found matching '{query}'{RESET}")
        beep()
    else:
        print(f"  Found {len(results)} matching record(s):\n")
        for o in results[:10]:
            print(f"  +{'-'*56}+")
            print(f"  | Order:    {o['order_number']:<44} |")
            print(f"  | Customer: {o['customer']:<44} |")
            print(f"  | Status:   {o['status']:<44} |")
            print(f"  | Date:     {o['order_date'][:10]:<44} |")
            print(f"  | Value:    ${o['total_value']:>12,.2f}{' '*31} |")
            print(f"  | Items:    {len(o.get('items', []))} line item(s){' '*32} |")
        print(f"  +{'-'*56}+")
        if len(results) > 10:
            print(f"  {YELLOW}... and {len(results) - 10} more (display limit reached){RESET}")

    press_enter()


def system_info():
    draw_header()
    print(f"  {REVERSE} SYSTEM INFORMATION {RESET}\n")

    inventory = _load("inventory.json")
    orders_data = _load("orders.json")

    lines = [
        f"Application:     FactorySoft IMS v2.1.3",
        f"Build Date:      1997-11-14",
        f"Python Version:  {sys.version.split()[0]}",
        f"Platform:        {sys.platform}",
        f"Data Directory:  {DATA_DIR}",
        f"",
        f"DATA FILE SIZES:",
        f"  inventory.json       {len(inventory):>6} records",
        f"  orders.json          {len(orders_data):>6} records",
        f"  demand_forecasts     {len(_load('demand_forecasts.json')):>6} records",
        f"  backlog_items        {len(_load('backlog_items.json')):>6} records",
        f"  transactions         {len(_load('transactions.json')):>6} records",
        f"",
        f"DISK USAGE:",
    ]

    total_size = 0
    for fname in os.listdir(DATA_DIR):
        fpath = os.path.join(DATA_DIR, fname)
        size = os.path.getsize(fpath)
        total_size += size
        lines.append(f"  {fname:<25} {size:>8} bytes")
    lines.append(f"  {'TOTAL':<25} {total_size:>8} bytes")
    lines.append("")
    lines.append(f"WARNING: No database engine detected.")
    lines.append(f"Running in flat-file JSON mode.")
    lines.append(f"Max recommended records: 10,000")

    draw_box(lines, width=60, title="SYSTEM DIAGNOSTICS")
    press_enter()


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------
def main_menu():
    while True:
        draw_header()

        print(f"  {BOLD}MAIN MENU{RESET}")
        print(f"  {'='*40}")
        print()
        print(f"  {CYAN}[1]{RESET}  Dashboard Summary")
        print(f"  {CYAN}[2]{RESET}  View Inventory")
        print(f"  {CYAN}[3]{RESET}  View Orders")
        print(f"  {CYAN}[4]{RESET}  Search Orders")
        print(f"  {CYAN}[5]{RESET}  Demand Forecasts")
        print(f"  {CYAN}[6]{RESET}  Backlog Report")
        print(f"  {CYAN}[7]{RESET}  Spending Report")
        print(f"  {CYAN}[8]{RESET}  Add Inventory Item")
        print(f"  {CYAN}[9]{RESET}  System Info")
        print(f"  {CYAN}[0]{RESET}  Exit")
        print()
        print(f"  {DIM}Tip: For web API access, run app.py instead{RESET}")
        print()

        choice = input(f"  Enter selection [0-9]: ").strip()

        if choice == "1":
            view_dashboard()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            view_orders()
        elif choice == "4":
            search_orders()
        elif choice == "5":
            view_demand()
        elif choice == "6":
            view_backlog()
        elif choice == "7":
            view_spending()
        elif choice == "8":
            add_inventory_item()
        elif choice == "9":
            system_info()
        elif choice == "0":
            clear_screen()
            slow_print(f"\n  {DIM}Closing connections...{RESET}", delay=0.02)
            slow_print(f"  {DIM}Flushing buffers...{RESET}", delay=0.02)
            slow_print(f"  {DIM}Saving session log...{RESET}", delay=0.02)
            print(f"\n  {GREEN}Goodbye. Have a productive day.{RESET}")
            print(f"  {DIM}(c) 1997 FactorySoft Solutions Inc.{RESET}\n")
            sys.exit(0)
        else:
            beep()
            print(f"\n  {RED}INVALID SELECTION. Please enter a number 0-9.{RESET}")
            time.sleep(1)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        # Startup sequence - painfully slow
        clear_screen()
        print(f"\n{DIM}")
        slow_print("  Initializing FactorySoft IMS v2.1.3 ...", delay=0.03)
        slow_print("  Checking license key ... OK", delay=0.02)
        slow_print("  Loading data modules ...", delay=0.02)
        loading_bar("Reading inventory database", duration=1.0)
        slow_print("  Verifying data integrity ...", delay=0.02)
        loading_bar("Checksumming records", duration=0.8)
        slow_print("  Establishing terminal session ...", delay=0.02)
        slow_print(f"  Welcome, {os.environ.get('USER', 'OPERATOR').upper()}", delay=0.03)
        print(f"{RESET}")
        time.sleep(0.5)

        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Session terminated by user (SIGINT){RESET}")
        print(f"  {DIM}(c) 1997 FactorySoft Solutions Inc.{RESET}\n")
        sys.exit(1)
