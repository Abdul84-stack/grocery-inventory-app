import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io
from barcode import Code128
from barcode.writer import ImageWriter
import base64
from io import BytesIO

# --- Configuration and Styling ---
st.set_page_config(layout="wide", page_title="Grocery Inventory Management")

st.markdown("""
<style>
    /* Google Fonts - Inter for a clean, modern look */
    @import url('https://https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* General body styling */
    body {
        font-family: 'Inter', sans-serif;
        background-color: #f0f2f6; /* Light gray background */
    }

    /* Streamlit container overrides */
    .st-emotion-cache-1gh2jqd { /* Main content container */
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 1.5rem;
        background-color: #ffffff; /* White background for main content area */
        border-radius: 12px; /* More rounded corners for the main area */
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05); /* Softer, larger shadow */
        margin: 1.5rem auto; /* Center with margin */
        max-width: 1200px; /* Max width for better readability on large screens */
    }
    .st-emotion-cache-1naxt9a { /* Sidebar container */
        background-color: #e0e0e0; /* Slightly darker gray for sidebar */
        border-right: 1px solid #c0c0c0;
        padding-top: 1rem;
        border-radius: 0 12px 12px 0; /* Rounded right corners */
    }
    .st-emotion-cache-1ldf025 { /* Wrapper for main content */
        padding-top: 0 !important; /* Remove default top padding to control it via .st-emotion-cache-1gh2jqd */
    }
    .st-emotion-cache-vk33p5 { /* Top-level block for padding in wide mode */
        padding-left: 0rem;
        padding-right: 0rem;
    }


    /* Headings */
    h1 {
        color: #2c3e50; /* Darker blue-gray for main titles */
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    h2 {
        color: #34495e;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    h3 {
        color: #555;
        font-weight: 500;
    }

    /* Section header styling */
    .section-header {
        font-size: 1.8em;
        font-weight: bold;
        color: #333;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #e9ecef; /* Thicker, lighter bottom border */
        padding-bottom: 0.8rem;
        text-align: center; /* Center align section headers */
        letter-spacing: 0.05em; /* Slightly more spaced letters */
    }

    /* Info boxes for dashboard */
    .info-box {
        background-color: #ffffff;
        border-radius: 10px; /* Slightly more rounded */
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08); /* Improved shadow */
        padding: 1.2rem;
        text-align: center;
        margin-bottom: 1.2rem;
        transition: transform 0.2s ease-in-out;
        border: 1px solid #e0e0e0; /* Subtle border */
        display: flex; /* Flexbox for icon and text */
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .info-box:hover {
        transform: translateY(-3px);
    }
    .info-box .icon {
        font-size: 3em; /* Icon size */
        margin-bottom: 0.5rem;
        color: #007bff; /* Icon color */
    }
    .info-box .value {
        font-size: 2.5em; /* Larger value font */
        font-weight: 700; /* Bolder value */
        color: #007bff; /* Primary blue */
        line-height: 1.2;
    }
    .info-box .label {
        font-size: 1em;
        color: #666;
        margin-top: 0.5rem;
        text-transform: uppercase; /* Uppercase label */
        letter-spacing: 0.03em;
    }

    /* Alert box for low stock */
    .low-stock-alert {
        background-color: #ffe0b2; /* Lighter orange-yellow */
        color: #e65100; /* Darker orange text */
        border: 1px solid #ffcc80;
        border-left: 6px solid #ff9800; /* More prominent orange border */
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    .low-stock-alert p {
        margin-bottom: 0.5rem;
    }

    /* Streamlit Button Styling */
    .stButton > button {
        background-color: #007bff; /* Primary blue */
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 123, 255, 0.3);
        cursor: pointer;
        font-size: 1em;
    }
    .stButton > button:hover {
        background-color: #0056b3; /* Darker blue on hover */
        box-shadow: 0 6px 15px rgba(0, 123, 255, 0.4);
        transform: translateY(-2px);
    }
    .stButton > button:active {
        background-color: #004085;
        transform: translateY(0);
        box_shadow: 0 2px 5px rgba(0, 123, 255, 0.5);
    }
    /* Specific styling for the icon buttons in Administrative Services, if they were used again */
    div[data-testid="stColumn"] .stButton > button {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100px; /* Fixed height for icon buttons */
        width: 100%; /* Make them fill column width */
        padding: 0.5rem;
        font-size: 0.9em;
        text-align: center;
        background-color: #f8f9fa; /* Lighter background for these cards */
        color: #333;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    div[data-testid="stColumn"] .stButton > button:hover {
        background-color: #e2e6ea;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px (0,0,0,0.1);
    }
    div[data-testid="stColumn"] .stButton > button .icon { /* Targeting the emoji/icon within the button */
        font-size: 2.5em; /* Adjust icon size */
        margin-bottom: 0.2rem;
        color: #007bff;
    }


    /* Streamlit Input Fields (text_input, number_input, selectbox) */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 8px;
        border: 1px solid #ced4da;
        padding: 0.5rem 1rem;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.075);
        transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus, .stSelectbox>div>div>div:focus-within {
        border-color: #80bdff;
        outline: 0;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    }

    /* Data Editor Styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden; /* Ensures rounded corners apply to the whole table */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    /* Messages (success, error, info) */
    .stAlert {
        border-radius: 8px;
        padding: 1rem 1.5rem;
    }
    .stAlert.success {
        background-color: #d4edda;
        color: #155724;
        border-color: #c3e6cb;
    }
    .stAlert.error {
        background-color: #f8d7da;
        color: #721c24;
        border-color: #f5c6cb;
    }
    .stAlert.info {
        background-color: #d1ecf1;
        color: #0c5460;
        border-color: #bee5eb;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] button {
        padding: 0.75rem 1.5rem;
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        border: 1px solid #e0e0e0;
        border-bottom: none;
        margin-right: 5px;
        font-weight: 600;
        color: #555;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #e9ecef;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #ffffff; /* Active tab background */
        border-top: 2px solid #007bff; /* Blue top border for active tab */
        border-left: 1px solid #e0e0e0;
        border-right: 1px solid #e0e0e0;
        color: #007bff; /* Active tab text color */
        box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
    }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1.5rem;
        margin-top: -1px; /* Overlap with tabs */
    }

    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #28a745; /* Green for healthy stock */
        border-radius: 5px;
    }
    .stProgress.low-stock-bar > div > div > div > div {
        background-color: #ffc107; /* Orange for low stock */
    }
    .stProgress.critical-stock-bar > div > div > div > div {
        background-color: #dc3545; /* Red for critical stock */
    }
    /* Receipt Styling - Custom for requested format */
    .receipt-container {
        font-family: 'monospace', 'Courier New', monospace;
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        max-width: 400px; /* Standard receipt width */
        margin-left: auto;
        margin-right: auto;
        font-size: 0.9em; /* Slightly smaller default font */
    }
    .receipt-header {
        text-align: center;
        margin-bottom: 15px;
        padding-bottom: 10px;
    }
    .receipt-header h3 {
        margin: 0;
        padding: 0;
        font-size: 1.5em; /* Larger store name */
        color: #333;
    }
    .receipt-header p {
        margin: 2px 0;
        font-size: 0.9em;
        color: #555;
    }
    .receipt-details {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        font-size: 0.9em;
    }
    .receipt-details span {
        white-space: nowrap; /* Prevent wrapping for date/time */
    }
    .receipt-line-dashed {
        border-bottom: 1px dashed #bbb;
        margin: 10px 0;
    }
    .receipt-items-header {
        display: flex;
        font-weight: bold;
        margin-bottom: 5px;
        font-size: 0.9em;
    }
    .receipt-items-header .qty-col { flex: 0 0 40px; text-align: left; }
    .receipt-items-header .desc-col { flex: 1; text-align: left; padding-left: 10px; }
    .receipt-items-header .price-col { flex: 0 0 80px; text-align: right; }
    .receipt-items-header .total-col { flex: 0 0 80px; text-align: right; }

    .receipt-item-row {
        display: flex;
        margin-bottom: 3px;
        font-size: 0.9em;
    }
    .receipt-item-row .qty-col { flex: 0 0 40px; text-align: left; }
    .receipt-item-row .desc-col { flex: 1; text-align: left; padding-left: 10px; }
    .receipt-item-row .price-col { flex: 0 0 80px; text-align: right; }
    .receipt-item-row .total-col { flex: 0 0 80px; text-align: right; }

    .receipt-summary-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 3px;
        font-size: 1em; /* Larger for summary */
    }
    .receipt-summary-row .label {
        flex: 1;
        text-align: left;
    }
    .receipt-summary-row .value {
        flex: 1;
        text-align: right;
        font-weight: bold;
    }
    .receipt-summary-row.total-row .value {
        font-size: 1.2em;
    }

    .receipt-footer {
        text-align: center;
        margin-top: 20px;
        font-size: 0.8em;
        color: #666;
    }

    /* Print-specific CSS */
    @media print {
        body > *:not(.receipt-container) {
            display: none !important; /* Hide everything except the receipt container */
        }
        .receipt-container {
            width: 100%;
            margin: 0;
            padding: 0;
            box-shadow: none;
            border: none;
            background-color: white;
            font-size: 10pt; /* Adjust font size for print */
        }
        .receipt-header, .receipt-line-dashed, .receipt-summary-row, .receipt-footer {
            border-color: #000; /* Darker borders for print */
        }
    }

    /* Analytics Report Cards */
    .report-card {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        border: 1px solid #e0e0e0;
        height: 100%; /* Ensure cards in a row have same height */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .report-card .value {
        font-size: 2.8em; /* Larger value */
        font-weight: 700;
        color: #007bff;
        margin-bottom: 0.5rem;
    }
    .report-card .label {
        font-size: 1.1em;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .report-card.red .value { color: #dc3545; }
    .report-card.green .value { color: #28a745; }
    .report-card.blue .value { color: #007bff; }


</style>
""", unsafe_allow_html=True)

# --- Initialize Inventory Data ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(
        [
            {"SKU": "PROD001", "Product Name": "Milo", "Unit": "45kg", "Category": "Beverages", "Quantity": 50, "Unit Price (₦)": 4500.00, "Cost Price (₦)": 4000.00, "Reorder Point": 13, "Expiry Date": datetime(2025, 11, 11).date(), "Last Updated": datetime.now(), "Store": "Main Store"},
            {"SKU": "PROD002", "Product Name": "Rice", "Unit": "25kg", "Category": "Pantry", "Quantity": 30, "Unit Price (₦)": 35000.00, "Cost Price (₦)": 32000.00, "Reorder Point": 8, "Expiry Date": datetime(2025, 11, 12).date(), "Last Updated": datetime.now(), "Store": "Main Store"},
            {"SKU": "PROD003", "Product Name": "Pepsi", "Unit": "Units", "Category": "Beverages", "Quantity": 144, "Unit Price (₦)": 500.00, "Cost Price (₦)": 350.00, "Reorder Point": 36, "Expiry Date": datetime(2025, 11, 13).date(), "Last Updated": datetime.now(), "Store": "Branch A"},
            {"SKU": "PROD004", "Product Name": "Biscuits", "Unit": "Units", "Category": "Snacks", "Quantity": 120, "Unit Price (₦)": 120.00, "Cost Price (₦)": 90.00, "Reorder Point": 30, "Expiry Date": datetime(2025, 11, 14).date(), "Last Updated": datetime.now(), "Store": "Main Store"},
            {"SKU": "PROD005", "Product Name": "Sugar", "Unit": "Kg", "Category": "Pantry", "Quantity": 10, "Unit Price (₦)": 6000.00, "Cost Price (₦)": 5500.00, "Reorder Point": 3, "Expiry Date": datetime(2025, 11, 15).date(), "Last Updated": datetime.now(), "Store": "Branch B"},
            {"SKU": "PROD006", "Product Name": "Fanta", "Unit": "Units", "Category": "Beverages", "Quantity": 38, "Unit Price (₦)": 500.00, "Cost Price (₦)": 350.00, "Reorder Point": 10, "Expiry Date": datetime(2025, 11, 16).date(), "Last Updated": datetime.now(), "Store": "Branch A"},
            {"SKU": "PROD007", "Product Name": "Semovita", "Unit": "1.5kg", "Category": "Pantry", "Quantity": 10, "Unit Price (₦)": 1800.00, "Cost Price (₦)": 1600.00, "Reorder Point": 3, "Expiry Date": datetime(2025, 11, 17).date(), "Last Updated": datetime.now(), "Store": "Main Store"},
            {"SKU": "PROD008", "Product Name": "Gala Sausage", "Unit": "Units", "Category": "Snacks", "Quantity": 24, "Unit Price (₦)": 250.00, "Cost Price (₦)": 180.00, "Reorder Point": 5, "Expiry Date": datetime(2025, 6, 29).date(), "Last Updated": datetime.now(), "Store": "Branch B"}, # This one is near expiry
        ]
    )
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=['Timestamp', 'SKU', 'Product Name', 'Quantity Change', 'Type', 'Selling Price (₦)', 'Cost Price (₦)', 'Revenue (₦)', 'Cost of Goods Sold (₦)', 'Profit/Loss (₦)', 'New Quantity', 'Store', 'Payment Method', 'Transaction ID']) # Added Payment Method and Transaction ID

# Initialize a new DataFrame for operating expenses
if 'operating_expenses' not in st.session_state:
    st.session_state.operating_expenses = pd.DataFrame(columns=['Date', 'Category', 'Description', 'Amount (₦)', 'Store'])


# Initialize the shopping cart and receipt history
if 'cart' not in st.session_state: # Corrected from 'current_cart'
    st.session_state.cart = [] # List of dictionaries: {'SKU', 'Product Name', 'Quantity', 'Unit Price', 'Subtotal'}
if 'receipt_history' not in st.session_state:
    st.session_state.receipt_history = [] # List of generated receipts (strings/markdown)
if 'last_receipt' not in st.session_state: # Initialize last_receipt for persistence
    st.session_state.last_receipt = ""

# Define thresholds for alerts
DEFAULT_EXPIRY_ALERT_DAYS = 10 # Default: Items expiring within the next 10 days
GALA_SAUSAGE_EXPIRY_ALERT_DAYS = 3 # Specific for Gala Sausage
LOW_STOCK_THRESHOLD = 10
CRITICAL_STOCK_THRESHOLD = 3

# --- Helper Functions ---
def add_product(sku, name, unit, category, quantity, selling_price, cost_price, reorder_point, expiry_date, store):
    # Check if SKU already exists for the given store (case-insensitive for robustness)
    if sku.upper() in st.session_state.inventory[st.session_state.inventory['Store'] == store]['SKU'].str.upper().values:
        st.error(f"Product with SKU '{sku}' already exists in {store}. Please use a unique SKU or update the existing product.")
        return False
    new_product = pd.DataFrame([{
        "SKU": sku.upper(), # Store SKU in uppercase for consistency
        "Product Name": name,
        "Unit": unit,
        "Category": category,
        "Quantity": quantity,
        "Unit Price (₦)": selling_price,
        "Cost Price (₦)": cost_price, # New: Store cost price
        "Reorder Point": reorder_point,
        "Expiry Date": expiry_date,
        "Last Updated": datetime.now(),
        "Store": store # Assign to the selected store
    }])
    st.session_state.inventory = pd.concat([st.session_state.inventory, new_product], ignore_index=True)
    st.success(f"Added '{name}' to inventory for {store}.")
    return True

def update_stock(sku, change_quantity, transaction_type, store, selling_price=0.0, purchase_cost_price=0.0, payment_method=None, transaction_id=None):
    # Find the product by SKU and Store (case-insensitive search for SKU)
    idx = st.session_state.inventory[(st.session_state.inventory['SKU'].str.upper() == sku.upper()) & (st.session_state.inventory['Store'] == store)].index
    if not idx.empty:
        current_qty = st.session_state.inventory.loc[idx[0], 'Quantity']
        product_name = st.session_state.inventory.loc[idx[0], 'Product Name']
        
        # Get current selling and cost prices from inventory for transaction recording
        current_selling_price = st.session_state.inventory.loc[idx[0], 'Unit Price (₦)']
        current_cost_price = st.session_state.inventory.loc[idx[0], 'Cost Price (₦)']

        new_qty = current_qty
        transaction_cost_price = 0.0 # Cost price relevant to this specific transaction
        transaction_revenue = 0.0
        transaction_cogs = 0.0
        transaction_profit = 0.0
        cost_of_goods_bought = 0.0

        if transaction_type == "Sale":
            if current_qty >= change_quantity:
                new_qty = current_qty - change_quantity
                st.session_state.inventory.loc[idx[0], 'Quantity'] = new_qty
                st.session_state.inventory.loc[idx[0], 'Last Updated'] = datetime.now()
                
                # For sales, selling_price is the price per unit sold
                transaction_revenue = change_quantity * selling_price
                # Cost of goods sold is quantity sold * current cost price from inventory
                transaction_cogs = change_quantity * current_cost_price
                transaction_profit = transaction_revenue - transaction_cogs
                
                # The cost price recorded for a sale transaction is the inventory's current cost price for that item
                transaction_cost_price = current_cost_price 

            else:
                st.error(f"Not enough stock for '{product_name}' in {store}. Available: {current_qty}, Attempted sale: {change_quantity}")
                return False
        
        elif transaction_type == "Purchase (Stock In)":
            new_qty = current_qty + change_quantity
            st.session_state.inventory.loc[idx[0], 'Quantity'] = new_qty
            st.session_state.inventory.loc[idx[0], 'Last Updated'] = datetime.now()
            
            # If a purchase_cost_price is provided, update the inventory's cost price for this product
            if purchase_cost_price > 0:
                st.session_state.inventory.loc[idx[0], 'Cost Price (₦)'] = purchase_cost_price
                transaction_cost_price = purchase_cost_price # Cost price for the purchase transaction
            else:
                transaction_cost_price = current_cost_price # Use existing cost price if none provided (shouldn't happen with proper input)
            
            # For purchases, revenue and profit are zero, cost is quantity * purchase_cost_price
            cost_of_goods_bought = change_quantity * transaction_cost_price # This is the "cost of goods bought"

            st.success(f"Recorded purchase: {change_quantity} units of '{product_name}' for {store}. New quantity: {new_qty}. Cost Price updated to ₦{transaction_cost_price:.2f}")

        # Record transaction for history
        new_transaction_data = {
            'Timestamp': datetime.now(),
            'SKU': sku.upper(),
            'Product Name': product_name,
            'Quantity Change': -change_quantity if transaction_type == "Sale" else change_quantity,
            'Type': transaction_type,
            'Selling Price (₦)': selling_price if transaction_type == "Sale" else 0.0, # Only relevant for sales
            'Cost Price (₦)': transaction_cost_price, # Cost price at the time of transaction
            'Revenue (₦)': transaction_revenue, # Only relevant for sales
            'Cost of Goods Sold (₦)': transaction_cogs if transaction_type == "Sale" else 0.0, # COGS only for sales
            'Cost of Goods Bought (₦)': cost_of_goods_bought if transaction_type == "Purchase (Stock In)" else 0.0, # COGB only for purchases
            'Profit/Loss (₦)': transaction_profit, # Only relevant for sales
            'New Quantity': new_qty,
            'Store': store, # Assign to the selected store
            'Payment Method': payment_method if payment_method else "N/A", # New: Payment Method
            'Transaction ID': transaction_id if transaction_id else "N/A" # New: Transaction ID
        }

        # Ensure all columns exist before concatenating
        for col in new_transaction_data.keys():
            if col not in st.session_state.transactions.columns:
                st.session_state.transactions[col] = pd.Series(dtype=type(new_transaction_data[col]))

        new_transaction_df = pd.DataFrame([new_transaction_data])
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_transaction_df], ignore_index=True)
        return True
    else:
        st.error(f"Product with SKU '{sku}' not found in {store}.")
        return False

def generate_barcode_base64(sku):
    try:
        # Code128 is flexible and supports alphanumeric SKUs
        barcode_obj = Code128(sku, writer=ImageWriter())
        
        # Save to a BytesIO object
        buffer = BytesIO()
        barcode_obj.write(buffer)
        
        # Encode to base64
        encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{encoded_image}"
    except Exception as e:
        st.warning(f"Could not generate barcode for SKU {sku}: {e}. Ensure SKU is valid for barcode type.")
        return None

def generate_receipt(cart_items, subtotal_amount, discount_amount, vat_rate, total_amount, payment_method, transaction_id, store_name, cashier_name=""):
    current_time_str = datetime.now().strftime('%H:%M')
    current_date_str = datetime.now().strftime('%d/%m/%Y')
    
    # Calculate VAT amount
    vat_amount = subtotal_amount * (vat_rate / 100)

    # Updated receipt header with the new business name and address
    receipt_str = f"""
    <div class="receipt-container">
        <div class="receipt-header">
            <h3>Habeni Diamond Kid Station</h3>
            <p>Retail Market, Abesan Estate, Ipaja, Lagos State</p>
            <p>Tel: 0802-000-0000</p>
            <p>TIN: 1034567890</p>
        </div>

        <div class="receipt-details">
            <span>Date: {current_date_str}  Time: {current_time_str}</span>
            <span>Cashier: {cashier_name if cashier_name else 'N/A'}</span>
        </div>
        <div class="receipt-line-dashed"></div>

        <div class="receipt-items-header">
            <span class="qty-col">Qty</span>
            <span class="desc-col">Description</span>
            <span class="price-col">Price</span>
            <span class="total-col">Total</span>
        </div>
        <div class="receipt-line-dashed"></div>
    """

    for item in cart_items:
        receipt_str += f"""
        <div class="receipt-item-row">
            <span class="qty-col">{item['Quantity']}</span>
            <span class="desc-col">{item['Product Name']}</span>
            <span class="price-col">{item['Unit Price']:.2f}</span>
            <span class="total-col">{item['Subtotal']:.2f}</span>
        </div>
        """

    receipt_str += f"""
        <div class="receipt-line-dashed"></div>

        <div class="receipt-summary-row">
            <span class="label">Sub-Total:</span>
            <span class="value">₦{subtotal_amount:,.2f}</span>
        </div>
    """
    if discount_amount > 0:
        receipt_str += f"""
        <div class="receipt-summary-row" style="color: red;">
            <span class="label">Discount:</span>
            <span class="value">-₦{discount_amount:,.2f}</span>
        </div>
        """

    receipt_str += f"""
        <div class="receipt-summary-row">
            <span class="label">VAT ({vat_rate:.1f}%):</span>
            <span class="value">₦{vat_amount:,.2f}</span>
        </div>
        <div class="receipt-summary-row total-row" style="font-weight: bold;">
            <span class="label">TOTAL:</span>
            <span class="value">₦{total_amount:,.2f}</span>
        </div>
        <div class="receipt-line-dashed"></div>

        <div class="receipt-summary-row">
            <span class="label">Payment Mode:</span>
            <span class="value">{payment_method}</span>
        </div>
        <div class="receipt-summary-row">
            <span class="label">Transaction ID:</span>
            <span class="value">{transaction_id if transaction_id else 'N/A'}</span>
        </div>

        <div class="receipt-footer">
            <p>Thank you for shopping with us!</p>
            <p>No refund after 7 days with receipt.</p>
        </div>
    </div>
    """
    return receipt_str

# Helper function to convert DataFrame to Excel for download
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

# --- Sidebar Navigation ---
st.sidebar.title("Fresh Groceries Inventory")
st.sidebar.markdown("---")

# Store management
if 'stores' not in st.session_state:
    st.session_state.stores = ["Main Store", "Branch A", "Branch B"] # Initial stores
if 'current_store' not in st.session_state:
    st.session_state.current_store = st.session_state.stores[0]

st.sidebar.subheader("Select Store")
selected_store = st.sidebar.selectbox("Choose a Store:", st.session_state.stores, key="store_selector")
if selected_store != st.session_state.current_store:
    st.session_state.current_store = selected_store
    st.rerun()

st.sidebar.markdown("---")
menu_options = [
    "Dashboard",
    "Manage Products",
    "Point of Sale",
    "Record Transactions",
    "Operating Expenses", # New menu item
    "Expiry Alerts",
    "Low Stock Alerts",
    "Analytics & Reports",
    "About"
]
selected_page = st.sidebar.radio("Navigation", menu_options, key="main_nav")

# Filter dataframes by selected store
filtered_inventory = st.session_state.inventory[st.session_state.inventory['Store'] == st.session_state.current_store]
filtered_transactions = st.session_state.transactions[st.session_state.transactions['Store'] == st.session_state.current_store]
filtered_expenses = st.session_state.operating_expenses[st.session_state.operating_expenses['Store'] == st.session_state.current_store]

# --- Main Content Area ---
st.title("Grocery Inventory Management System")
st.markdown(f"For: **Habeni Diamond Kid Station - {st.session_state.current_store}**") # Updated store name here!


if selected_page == "Dashboard":
    st.markdown('<div class="section-header">📊 Dashboard</div>', unsafe_allow_html=True)
    
    total_products = len(filtered_inventory)
    total_quantity = filtered_inventory['Quantity'].sum()

    # Calculate low, critical, and expiring items
    low_stock_items = filtered_inventory[filtered_inventory['Quantity'] <= filtered_inventory['Reorder Point']]
    critical_stock_items = filtered_inventory[filtered_inventory['Quantity'] <= CRITICAL_STOCK_THRESHOLD] # Use fixed critical threshold
    
    today = datetime.now().date()
    
    # Logic for expiring_soon_items with special handling for "Gala Sausage"
    expiring_soon_items_list = []
    for index, row in filtered_inventory.iterrows():
        product_expiry_date = row['Expiry Date']
        product_name = row['Product Name']
        
        # Check if product_name is a valid string before calling .lower()
        if pd.notna(product_name) and str(product_name).strip().lower() == "gala sausage":
            alert_days = GALA_SAUSAGE_EXPIRY_ALERT_DAYS
        else:
            alert_days = DEFAULT_EXPIRY_ALERT_DAYS

        if today <= product_expiry_date <= today + timedelta(days=alert_days):
            expiring_soon_items_list.append(row)

    expiring_soon_items = pd.DataFrame(expiring_soon_items_list)
    
    if not expiring_soon_items.empty:
        expiring_soon_items = expiring_soon_items.sort_values(by="Expiry Date")

    expired_items = filtered_inventory[filtered_inventory['Expiry Date'] < today].sort_values(by="Expiry Date")

    num_low_stock = len(low_stock_items)
    num_critical_stock = len(critical_stock_items)
    num_expiring_soon = len(expiring_soon_items)
    num_expired = len(expired_items)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="info-box">
            <span class="icon">📦</span>
            <div class="value">{total_products}</div>
            <div class="label">Total Unique Products</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="info-box">
            <span class="icon">🛒</span>
            <div class="value">{total_quantity}</div>
            <div class="label">Total Items in Stock</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="info-box">
            <span class="icon">⚠️</span>
            <div class="value">{num_low_stock}</div>
            <div class="label">Low Stock Items</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="info-box">
            <span class="icon">🗓️</span>
            <div class="value">{num_expiring_soon + num_expired}</div>
            <div class="label">Expiring Items</div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Stock Health Overview")
    if total_products > 0:
        # For simplicity, calculate percentages based on count of items, not total quantity
        # Filter out duplicates for the progress bar calculation
        unique_healthy_items_count = total_products - len(low_stock_items.merge(critical_stock_items, on='SKU', how='outer'))
        healthy_stock_percent = (unique_healthy_items_count / total_products) * 100
        low_stock_only_count = num_low_stock - num_critical_stock
        low_stock_percent = (low_stock_only_count / total_products) * 100
        critical_stock_percent = (num_critical_stock / total_products) * 100
        
        progress_html = f"""
        <div style="width: 100%; background-color: #e0e0e0; border-radius: 5px; overflow: hidden; height: 25px; margin-bottom: 1rem;">
            <div style="width: {healthy_stock_percent:.2f}%; background-color: #28a745; height: 100%; float: left; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                {f'{healthy_stock_percent:.0f}% Healthy' if healthy_stock_percent > 10 else ''}
            </div>
            <div style="width: {low_stock_percent:.2f}%; background-color: #ffc107; height: 100%; float: left; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                {f'{low_stock_percent:.0f}% Low' if low_stock_percent > 10 else ''}
            </div>
            <div style="width: {critical_stock_percent:.2f}%; background-color: #dc3545; height: 100%; float: left; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                {f'{critical_stock_percent:.0f}% Critical' if critical_stock_percent > 10 else ''}
            </div>
        </div>
        """
        st.markdown(progress_html, unsafe_allow_html=True)
        st.markdown(f"""
        <p style="text-align: center; color: #666; font-size: 0.9em;"> Green: Healthy Stock ({unique_healthy_items_count} products) | Orange: Low Stock ({low_stock_only_count} products) | Red: Critical Stock ({num_critical_stock} products) </p>
        """, unsafe_allow_html=True)
    else:
        st.info("No products in inventory yet. Add some to see stock health!")

    st.subheader("Category Distribution")
    if not filtered_inventory.empty:
        category_counts = filtered_inventory['Category'].value_counts()
        if not category_counts.empty:
            st.bar_chart(category_counts)
        else:
            st.info("No categories defined yet.")
    else:
        st.info("No products to display category distribution.")

    st.subheader("Recent Inventory Activity")
    if not filtered_transactions.empty:
        st.dataframe(filtered_transactions.sort_values(by='Timestamp', ascending=False).head(5), use_container_width=True)
    else:
        st.info("No recent inventory transactions recorded.")


elif selected_page == "Manage Products":
    st.markdown('<div class="section-header">📦 Manage Products</div>', unsafe_allow_html=True)
    
    st.subheader("Add New Product")
    with st.form("add_product_form"):
        col1, col2 = st.columns(2)
        with col1:
            sku = st.text_input("SKU (Unique Identifier)", max_chars=20).strip()
            product_name = st.text_input("Product Name").strip()
            category = st.selectbox("Category", filtered_inventory['Category'].unique().tolist() + ["New Category"] if not filtered_inventory.empty else ["New Category"])
            if category == "New Category":
                new_category = st.text_input("Enter New Category Name").strip()
                if new_category:
                    category = new_category
                else:
                    st.warning("Please enter a new category name or select an existing one.")
                    st.stop()
            quantity = st.number_input("Quantity", min_value=0, step=1)
        with col2:
            unit = st.text_input("Unit (e.g., kg, L, units)", "units").strip()
            selling_price = st.number_input("Unit Price (₦)", min_value=0.00, format="%.2f")
            cost_price = st.number_input("Cost Price (₦)", min_value=0.00, format="%.2f", help="This is the price you buy the product for.")
            reorder_point = st.number_input("Reorder Point", min_value=0, step=1)
            expiry_date = st.date_input("Expiry Date", value=datetime.now() + timedelta(days=365))
            store = st.selectbox("Assign to Store", st.session_state.stores, index=st.session_state.stores.index(st.session_state.current_store))

        add_submit = st.form_submit_button("Add Product")
        if add_submit:
            if sku and product_name and category and quantity is not None and selling_price is not None and cost_price is not None and reorder_point is not None and expiry_date:
                add_product(sku, product_name, unit, category, quantity, selling_price, cost_price, reorder_point, expiry_date, store)
            else:
                st.error("Please fill in all the required fields.")


    st.subheader("Current Inventory")
    if not filtered_inventory.empty:
        # Display the filtered inventory and allow editing
        st.dataframe(filtered_inventory, use_container_width=True)

        st.subheader("Generate Barcode for a Product")
        barcode_sku_to_print = st.selectbox("Select a product SKU to generate a barcode", filtered_inventory['SKU'].tolist())
        if barcode_sku_to_print:
            st.info("The generated barcode is a Code 128 type, suitable for alphanumeric SKUs.")
            barcode_data = generate_barcode_base64(barcode_sku_to_print)
            if barcode_data:
                st.markdown(f"<p style='text-align:center; font-size: 1.2em;'>{barcode_sku_to_print}</p>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:center;'><img src='{barcode_data}' alt='Barcode' style='max-width: 300px; height: auto;'></div>", unsafe_allow_html=True)
            
            # Button to trigger the print dialog for the barcode
            if st.button("Print Barcode"):
                # A simple way to trigger the browser's print dialog
                st.markdown(f"""
                <script>
                var content = "<div style='text-align:center; padding: 20px;'><h3>{barcode_sku_to_print}</h3><img src='{barcode_data}' style='max-width: 100%;'></div>";
                var printWindow = window.open('', '', 'height=400,width=600');
                printWindow.document.write('<html><head><title>Print Barcode</title>');
                printWindow.document.write('</head><body >');
                printWindow.document.write(content);
                printWindow.document.write('</body></html>');
                printWindow.document.close();
                printWindow.focus();
                printWindow.print();
                printWindow.close();
                </script>
                """, unsafe_allow_html=True)
            
        st.subheader("Remove a Product")
        with st.form("remove_form"):
            products_to_remove = st.multiselect(
                "Select one or more products to remove (SKU)",
                filtered_inventory['SKU'].tolist(),
                key="remove_multiselect"
            )
            removal_reason = st.text_area("Reason for Removal", height=68)
            
            submitted = st.form_submit_button("Remove Item")

            if submitted:
                if products_to_remove and removal_reason:
                    for sku in products_to_remove:
                        try:
                            # Use index to remove
                            index_to_remove = st.session_state.inventory[(st.session_state.inventory['SKU'] == sku) & (st.session_state.inventory['Store'] == st.session_state.current_store)].index
                            if not index_to_remove.empty:
                                product_name_removed = st.session_state.inventory.loc[index_to_remove[0], 'Product Name']
                                st.session_state.inventory = st.session_state.inventory.drop(index_to_remove).reset_index(drop=True)
                                st.success(f"Removed '{product_name_removed}' with SKU '{sku}' from inventory. Reason: {removal_reason}")
                                # No need to record in transactions since it's a full removal, not a transaction.
                            else:
                                st.warning(f"Product with SKU '{sku}' not found in the selected store.")
                        except Exception as e:
                            st.error(f"An error occurred while trying to remove SKU '{sku}': {e}")
                    # Rerun the app to update the display
                    st.rerun()
                else:
                    st.warning("Please select at least one product and provide a reason for removal.")
    else:
        st.info("No products in inventory for this store.")


elif selected_page == "Point of Sale":
    st.markdown('<div class="section-header">💰 Point of Sale (POS)</div>', unsafe_allow_html=True)
    st.warning("This POS system is for demonstration purposes. It does not handle concurrent transactions or real-time payment processing.")

    tab1, tab2 = st.tabs(["🛒 Sales Terminal", "📄 Receipt History"])

    with tab1:
        st.subheader("Current Cart")
        
        # Display cart in a DataFrame for a clean look
        if st.session_state.cart:
            cart_df = pd.DataFrame(st.session_state.cart)
            cart_df['Subtotal (₦)'] = cart_df['Subtotal'].apply(lambda x: f"₦{x:,.2f}")
            st.dataframe(cart_df[['Product Name', 'SKU', 'Quantity', 'Unit Price', 'Subtotal (₦)']], use_container_width=True)
        else:
            st.info("Cart is empty.")

        col1, col2, col3 = st.columns(3)
        with col1:
            subtotal = sum(item['Subtotal'] for item in st.session_state.cart)
            st.metric("Sub-Total", f"₦{subtotal:,.2f}")
        
        with col2:
            discount_amount = st.number_input("Discount (₦)", min_value=0.0, format="%.2f")

        with col3:
            vat_rate = st.number_input("VAT (%)", min_value=0.0, max_value=100.0, value=7.5, step=0.1)
        
        final_subtotal = subtotal - discount_amount
        vat_amount = final_subtotal * (vat_rate / 100)
        total_amount = final_subtotal + vat_amount

        st.metric("Total Amount Due", f"₦{total_amount:,.2f}")

        # --- Add to Cart Form ---
        st.subheader("Add Item to Cart")
        with st.form("add_to_cart_form"):
            product_options = filtered_inventory['Product Name'].unique().tolist()
            selected_product_name = st.selectbox("Select Product", product_options)
            
            if selected_product_name:
                # Find the SKU and Unit Price for the selected product
                product_info = filtered_inventory[filtered_inventory['Product Name'] == selected_product_name].iloc[0]
                sku = product_info['SKU']
                unit_price = product_info['Unit Price (₦)']
                max_qty = product_info['Quantity']
                
                quantity_to_add = st.number_input(f"Quantity to Sell (Max: {max_qty})", min_value=1, max_value=int(max_qty) if max_qty > 0 else 1, step=1, key=f"qty_add_{sku}")
            else:
                quantity_to_add = 0
            
            add_to_cart_button = st.form_submit_button("Add to Cart")
            
            if add_to_cart_button:
                if selected_product_name and quantity_to_add > 0:
                    # Check if the item is already in the cart
                    item_in_cart = next((item for item in st.session_state.cart if item['SKU'] == sku), None)
                    if item_in_cart:
                        new_qty = item_in_cart['Quantity'] + quantity_to_add
                        if new_qty > max_qty:
                            st.warning(f"Cannot add more '{selected_product_name}'. Total in cart would exceed available stock.")
                        else:
                            item_in_cart['Quantity'] = new_qty
                            item_in_cart['Subtotal'] = new_qty * unit_price
                            st.success(f"Added {quantity_to_add} more units of '{selected_product_name}'. New cart quantity: {new_qty}")
                            st.rerun()
                    else:
                        st.session_state.cart.append({
                            'SKU': sku,
                            'Product Name': selected_product_name,
                            'Quantity': quantity_to_add,
                            'Unit Price': unit_price,
                            'Subtotal': quantity_to_add * unit_price
                        })
                        st.success(f"Added {quantity_to_add} units of '{selected_product_name}' to cart.")
                        st.rerun()

        # --- Checkout Form ---
        st.subheader("Checkout")
        if st.session_state.cart:
            with st.form("checkout_form"):
                payment_method = st.selectbox("Payment Method", ["Cash", "POS/Card", "Transfer"])
                transaction_id = st.text_input("Transaction ID (Optional)", help="Enter a unique ID for the transaction, e.g., from POS receipt.")
                
                checkout_button = st.form_submit_button("Process Payment & Print Receipt")

                if checkout_button:
                    transaction_successful = True
                    for item in st.session_state.cart:
                        if not update_stock(item['SKU'], item['Quantity'], "Sale", st.session_state.current_store, selling_price=item['Unit Price'], payment_method=payment_method, transaction_id=transaction_id):
                            st.error(f"Checkout failed due to stock issues for {item['Product Name']}. Please re-check inventory.")
                            transaction_successful = False
                            break
                    
                    if transaction_successful:
                        st.success(f"Payment of ₦{total_amount:,.2f} processed successfully!")
                        
                        # Generate and store receipt
                        receipt = generate_receipt(st.session_state.cart, subtotal, discount_amount, vat_rate, total_amount, payment_method, transaction_id, st.session_state.current_store)
                        st.session_state.receipt_history.append(receipt)
                        st.session_state.last_receipt = receipt # Store the most recent receipt
                        
                        st.session_state.cart = [] # Clear the cart after successful checkout
                        
                        st.rerun() # Rerun to clear the form and display the receipt

    with tab2:
        st.subheader("Last Transaction Receipt")
        if st.session_state.last_receipt:
            st.markdown(st.session_state.last_receipt, unsafe_allow_html=True)
            if st.button("Print Receipt", key="print_receipt_btn"):
                # Use a small javascript snippet to trigger the print dialog
                st.markdown('<script>window.print();</script>', unsafe_allow_html=True)

            st.download_button(
                label="Download Last Receipt (HTML)",
                data=st.session_state.last_receipt,
                file_name=f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html"
            )
        else:
            st.info("No recent receipts to display.")
        
        st.subheader("All Receipt History")
        if st.session_state.receipt_history:
            for i, receipt in enumerate(reversed(st.session_state.receipt_history)):
                with st.expander(f"Receipt #{len(st.session_state.receipt_history) - i} ({datetime.now().strftime('%Y-%m-%d %H:%M')})"):
                    st.markdown(receipt, unsafe_allow_html=True)
        else:
            st.info("No receipts recorded yet.")

elif selected_page == "Record Transactions":
    st.markdown('<div class="section-header">🧾 Record Transactions</div>', unsafe_allow_html=True)
    
    st.subheader(f"Transaction History for {st.session_state.current_store}")
    if not filtered_transactions.empty:
        # Allow editing and adding new rows for manual transactions
        edited_transactions = st.data_editor(
            filtered_transactions.sort_values(by='Timestamp', ascending=False),
            column_config={
                "Timestamp": st.column_config.DatetimeColumn(
                    "Timestamp",
                    format="YYYY-MM-DD HH:mm:ss",
                    disabled=True
                ),
                "Store": st.column_config.TextColumn(disabled=True),
                "SKU": st.column_config.TextColumn(disabled=True),
                "Product Name": st.column_config.TextColumn(disabled=True),
                "Type": st.column_config.SelectboxColumn("Type", options=["Sale", "Purchase (Stock In)", "Adjustment"], required=True),
                "Quantity Change": st.column_config.NumberColumn("Quantity Change", format="%d", help="Use a positive number for stock in, negative for stock out."),
            },
            num_rows="dynamic",
            use_container_width=True
        )

        st.subheader("Adjust Existing Inventory")
        with st.form("adjust_form"):
            product_options = filtered_inventory['SKU'].tolist()
            sku_to_adjust = st.selectbox("Select Product to Adjust", product_options)
            
            if sku_to_adjust:
                current_qty = filtered_inventory[filtered_inventory['SKU'] == sku_to_adjust]['Quantity'].iloc[0]
                st.info(f"Current Quantity for '{sku_to_adjust}': {current_qty}")
            
            adjustment_quantity = st.number_input("Adjustment Quantity", step=1, help="Positive for adding stock, negative for removing.")
            adjustment_type = st.selectbox("Adjustment Type", ["Stock In", "Stock Out", "Correction"])
            reason = st.text_input("Reason for Adjustment", "Correction for inventory count")
            
            adjust_button = st.form_submit_button("Apply Adjustment")
            
            if adjust_button:
                if sku_to_adjust and adjustment_quantity != 0:
                    product_info = filtered_inventory[filtered_inventory['SKU'] == sku_to_adjust].iloc[0]
                    product_name = product_info['Product Name']
                    
                    new_qty = current_qty + adjustment_quantity
                    
                    if new_qty < 0:
                        st.error("Adjustment would result in negative stock. Please correct the quantity.")
                    else:
                        st.session_state.inventory.loc[st.session_state.inventory['SKU'] == sku_to_adjust, 'Quantity'] = new_qty
                        st.session_state.inventory.loc[st.session_state.inventory['SKU'] == sku_to_adjust, 'Last Updated'] = datetime.now()
                        
                        new_transaction_data = {
                            'Timestamp': datetime.now(),
                            'SKU': sku_to_adjust,
                            'Product Name': product_name,
                            'Quantity Change': adjustment_quantity,
                            'Type': f"Adjustment - {adjustment_type}",
                            'Selling Price (₦)': 0.0,
                            'Cost Price (₦)': 0.0,
                            'Revenue (₦)': 0.0,
                            'Cost of Goods Sold (₦)': 0.0,
                            'Profit/Loss (₦)': 0.0,
                            'New Quantity': new_qty,
                            'Store': st.session_state.current_store,
                            'Payment Method': "N/A",
                            'Transaction ID': f"ADJ-{datetime.now().timestamp()}"
                        }
                        
                        # Ensure all columns exist before concatenating
                        for col in new_transaction_data.keys():
                            if col not in st.session_state.transactions.columns:
                                st.session_state.transactions[col] = pd.Series(dtype=type(new_transaction_data[col]))
                        
                        new_transaction_df = pd.DataFrame([new_transaction_data])
                        st.session_state.transactions = pd.concat([st.session_state.transactions, new_transaction_df], ignore_index=True)
                        st.success(f"Adjusted '{product_name}' by {adjustment_quantity}. New quantity: {new_qty}")
                        st.rerun()
                else:
                    st.warning("Please select a product and enter a non-zero adjustment quantity.")
    else:
        st.info("No transaction history for this store yet.")

elif selected_page == "Operating Expenses":
    st.markdown('<div class="section-header">💸 Operating Expenses</div>', unsafe_allow_html=True)
    
    st.subheader("Record a New Expense")
    with st.form("add_expense_form"):
        col1, col2 = st.columns(2)
        with col1:
            expense_date = st.date_input("Date", datetime.now().date())
            expense_category = st.selectbox("Category", ["Rent", "Salaries", "Utilities", "Supplies", "Maintenance", "Others"])
        with col2:
            expense_amount = st.number_input("Amount (₦)", min_value=0.0, format="%.2f")
            expense_store = st.selectbox("Store", st.session_state.stores, index=st.session_state.stores.index(st.session_state.current_store))
        
        expense_description = st.text_area("Description")
        
        add_expense_button = st.form_submit_button("Add Expense")
        
        if add_expense_button:
            if expense_amount > 0 and expense_description:
                new_expense = pd.DataFrame([{
                    "Date": expense_date,
                    "Category": expense_category,
                    "Description": expense_description,
                    "Amount (₦)": expense_amount,
                    "Store": expense_store
                }])
                st.session_state.operating_expenses = pd.concat([st.session_state.operating_expenses, new_expense], ignore_index=True)
                st.success(f"Recorded expense of ₦{expense_amount:,.2f} for {expense_category}.")
                st.rerun()
            else:
                st.error("Please enter a valid amount and description.")

    st.subheader("Monthly Expenses Report")
    if not filtered_expenses.empty:
        # Group by month and category
        filtered_expenses['Month'] = filtered_expenses['Date'].apply(lambda x: x.strftime('%Y-%m'))
        monthly_expenses = filtered_expenses.groupby('Month')['Amount (₦)'].sum().reset_index()
        monthly_expenses_by_category = filtered_expenses.groupby(['Month', 'Category'])['Amount (₦)'].sum().unstack(fill_value=0)
        
        st.write("Total Monthly Expenses")
        st.bar_chart(monthly_expenses.set_index('Month'))
        
        st.write("Monthly Expenses by Category")
        st.bar_chart(monthly_expenses_by_category)
        
        st.subheader("All Expenses")
        st.dataframe(filtered_expenses.sort_values(by="Date", ascending=False), use_container_width=True)
        st.download_button(
            label="Download Expenses Data as Excel",
            data=to_excel(filtered_expenses),
            file_name=f"operating_expenses_{st.session_state.current_store}_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No operating expenses recorded for this store yet.")

elif selected_page == "Expiry Alerts":
    st.markdown('<div class="section-header">⚠️ Expiry Alerts</div>', unsafe_allow_html=True)
    
    today = datetime.now().date()
    
    # Logic for expiring_soon_items with special handling for "Gala Sausage"
    expiring_soon_items_list = []
    for index, row in filtered_inventory.iterrows():
        product_expiry_date = row['Expiry Date']
        product_name = row['Product Name']
        
        if pd.notna(product_name) and str(product_name).strip().lower() == "gala sausage":
            alert_days = GALA_SAUSAGE_EXPIRY_ALERT_DAYS
        else:
            alert_days = DEFAULT_EXPIRY_ALERT_DAYS

        if today <= product_expiry_date <= today + timedelta(days=alert_days):
            expiring_soon_items_list.append(row)

    expiring_soon_items = pd.DataFrame(expiring_soon_items_list)

    if not expiring_soon_items.empty:
        expiring_soon_items['Days Left'] = (expiring_soon_items['Expiry Date'] - today).dt.days
        st.subheader(f"Items Expiring Soon (within {DEFAULT_EXPIRY_ALERT_DAYS} days)")
        st.warning(f"The following {len(expiring_soon_items)} items are expiring soon and need attention.", icon="🚨")
        
        # Display as a table with sorted dates
        st.dataframe(
            expiring_soon_items.sort_values(by="Expiry Date")[['SKU', 'Product Name', 'Quantity', 'Expiry Date', 'Days Left']],
            use_container_width=True
        )
    else:
        st.info("No items are expiring soon.")

    # Expired Items
    expired_items = filtered_inventory[filtered_inventory['Expiry Date'] < today]
    if not expired_items.empty:
        expired_items['Days Expired'] = (today - expired_items['Expiry Date']).dt.days
        st.subheader("Expired Items")
        st.error(f"The following {len(expired_items)} items have expired and should be removed from stock.", icon="❌")
        st.dataframe(
            expired_items.sort_values(by="Expiry Date")[['SKU', 'Product Name', 'Quantity', 'Expiry Date', 'Days Expired']],
            use_container_width=True
        )
    else:
        st.info("No items have expired.")

elif selected_page == "Low Stock Alerts":
    st.markdown('<div class="section-header">📦 Low Stock Alerts</div>', unsafe_allow_html=True)
    
    # Calculate low stock items based on reorder point
    low_stock_items = filtered_inventory[
        (filtered_inventory['Quantity'] <= filtered_inventory['Reorder Point']) & 
        (filtered_inventory['Quantity'] > CRITICAL_STOCK_THRESHOLD)
    ].sort_values(by="Quantity")

    # Calculate critical stock items based on a fixed threshold
    critical_stock_items = filtered_inventory[
        filtered_inventory['Quantity'] <= CRITICAL_STOCK_THRESHOLD
    ].sort_values(by="Quantity")

    # Display Critical Stock first
    if not critical_stock_items.empty:
        st.subheader("🚨 Critical Stock Items (Need Immediate Restock)")
        st.error(f"The following {len(critical_stock_items)} items are below the critical stock threshold of {CRITICAL_STOCK_THRESHOLD} and need to be reordered immediately.", icon="🚨")
        st.dataframe(
            critical_stock_items[['SKU', 'Product Name', 'Quantity', 'Reorder Point']],
            use_container_width=True
        )
    else:
        st.success(f"No critical stock items found for {st.session_state.current_store}!")

    # Display Low Stock
    if not low_stock_items.empty:
        st.subheader("⚠️ Low Stock Items (Reorder Point Reached)")
        st.warning(f"The following {len(low_stock_items)} items have reached their reorder point and need to be restocked soon.", icon="⚠️")
        st.dataframe(
            low_stock_items[['SKU', 'Product Name', 'Quantity', 'Reorder Point']],
            use_container_width=True
        )
    else:
        st.info(f"No low stock items found for {st.session_state.current_store}.")

elif selected_page == "Analytics & Reports":
    st.markdown('<div class="section-header">📈 Analytics & Reports</div>', unsafe_allow_html=True)

    # Calculate metrics for the current store
    
    st.subheader(f"Financial Summary for {st.session_state.current_store}")
    col1, col2, col3, col4 = st.columns(4)
    
    # Ensure transactions DataFrame is not empty before calculations
    if not filtered_transactions.empty:
        
        # Calculate revenue, COGS, and profit from "Sale" transactions
        sales_data = filtered_transactions[filtered_transactions['Type'] == 'Sale']
        total_revenue = sales_data['Revenue (₦)'].sum()
        total_cogs = sales_data['Cost of Goods Sold (₦)'].sum()
        gross_profit = total_revenue - total_cogs
        
        # Calculate Cost of Goods Bought from "Purchase (Stock In)" transactions
        purchase_data = filtered_transactions[filtered_transactions['Type'] == 'Purchase (Stock In)']
        total_cog_bought = purchase_data['Cost of Goods Bought (₦)'].sum()
        
        # Calculate total expenses for the current store
        total_expenses = filtered_expenses['Amount (₦)'].sum()
        net_profit = gross_profit - total_expenses

        with col1:
            st.markdown(f"""
            <div class="report-card blue">
                <div class="value">₦{total_revenue:,.2f}</div>
                <div class="label">Total Revenue</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="report-card green">
                <div class="value">₦{gross_profit:,.2f}</div>
                <div class="label">Gross Profit</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="report-card red">
                <div class="value">₦{total_expenses:,.2f}</div>
                <div class="label">Total Expenses</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="report-card blue">
                <div class="value">₦{net_profit:,.2f}</div>
                <div class="label">Net Profit</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No transaction data available for this store to generate a financial summary.")

    st.subheader("Reports")
    report_type = st.selectbox("Select Report Type", ["Sales Report", "Cost of Goods Report", "Profit & Loss Statement", "Group Summary Report"])

    if report_type == "Sales Report":
        st.markdown("### Sales Report")
        if not filtered_transactions.empty:
            sales_data = filtered_transactions[filtered_transactions['Type'] == 'Sale'].copy()
            sales_data['Date'] = sales_data['Timestamp'].dt.date
            sales_summary = sales_data.groupby('Date').agg(
                Total_Sales=('Quantity Change', 'sum'),
                Total_Revenue=('Revenue (₦)', 'sum')
            ).reset_index()
            st.line_chart(sales_summary.set_index('Date')['Total_Revenue'])
            st.dataframe(sales_data[['Timestamp', 'Product Name', 'Quantity Change', 'Selling Price (₦)', 'Revenue (₦)', 'Payment Method', 'Transaction ID']], use_container_width=True)
            st.download_button(
                label="Download Sales Report as Excel",
                data=to_excel(sales_data),
                file_name=f"sales_report_{st.session_state.current_store}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("No sales data available.")

    elif report_type == "Cost of Goods Report":
        st.markdown("### Cost of Goods Report")
        if not filtered_transactions.empty:
            purchase_data = filtered_transactions[filtered_transactions['Type'] == 'Purchase (Stock In)'].copy()
            purchase_data['Date'] = purchase_data['Timestamp'].dt.date
            purchase_summary = purchase_data.groupby('Date').agg(
                Items_Bought=('Quantity Change', 'sum'),
                Total_Cost=('Cost of Goods Bought (₦)', 'sum')
            ).reset_index()
            st.line_chart(purchase_summary.set_index('Date')['Total_Cost'])
            st.dataframe(purchase_data[['Timestamp', 'Product Name', 'Quantity Change', 'Cost Price (₦)', 'Cost of Goods Bought (₦)']], use_container_width=True)
            st.download_button(
                label="Download Cost of Goods Report as Excel",
                data=to_excel(purchase_data),
                file_name=f"cost_of_goods_report_{st.session_state.current_store}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("No cost of goods data available.")

    elif report_type == "Profit & Loss Statement":
        st.markdown("### Profit & Loss Statement")
        # Ensure all necessary data is available
        if not filtered_transactions.empty or not filtered_expenses.empty:
            # Aggregate sales data (revenue, cogs)
            sales_data = filtered_transactions[filtered_transactions['Type'] == 'Sale']
            total_revenue = sales_data['Revenue (₦)'].sum()
            total_cogs = sales_data['Cost of Goods Sold (₦)'].sum()
            gross_profit = total_revenue - total_cogs
            
            # Aggregate expenses
            total_expenses = filtered_expenses['Amount (₦)'].sum()
            net_profit = gross_profit - total_expenses
            
            # Display P&L statement
            st.write(f"**Period:** All Time to Date")
            st.markdown(f"**Store:** {st.session_state.current_store}")
            st.markdown("---")
            st.metric("Total Revenue", f"₦{total_revenue:,.2f}")
            st.metric("Cost of Goods Sold (COGS)", f"₦{total_cogs:,.2f}")
            st.markdown("### **Gross Profit**", unsafe_allow_html=True)
            st.metric("Gross Profit", f"₦{gross_profit:,.2f}")
            st.markdown("---")
            st.markdown("### Operating Expenses", unsafe_allow_html=True)
            if not filtered_expenses.empty:
                st.dataframe(filtered_expenses[['Date', 'Category', 'Description', 'Amount (₦)']], use_container_width=True)
            st.metric("Total Operating Expenses", f"₦{total_expenses:,.2f}")
            st.markdown("---")
            st.markdown("### **Net Profit/Loss**", unsafe_allow_html=True)
            st.metric("Net Profit", f"₦{net_profit:,.2f}")

        else:
            st.info("No transaction or expense data to generate a Profit & Loss statement.")

    elif report_type == "Group Summary Report":
        st.markdown("### Group Summary Report (All Stores)")
        
        # Aggregate data across all stores
        all_sales = st.session_state.transactions[st.session_state.transactions['Type'] == 'Sale']
        all_expenses = st.session_state.operating_expenses
        
        if not all_sales.empty or not all_expenses.empty:
            
            # Group sales data by store
            sales_by_store = all_sales.groupby('Store').agg(
                Total_Revenue=('Revenue (₦)', 'sum'),
                Total_COGS=('Cost of Goods Sold (₦)', 'sum')
            ).reset_index()
            sales_by_store['Gross Profit'] = sales_by_store['Total_Revenue'] - sales_by_store['Total_COGS']
            
            # Group expenses data by store
            expenses_by_store = all_expenses.groupby('Store').agg(
                Total_Expenses=('Amount (₦)', 'sum')
            ).reset_index()
            
            # Merge the two dataframes
            group_summary = pd.merge(sales_by_store, expenses_by_store, on='Store', how='outer').fillna(0)
            group_summary['Net Profit'] = group_summary['Gross Profit'] - group_summary['Total_Expenses']
            
            st.dataframe(group_summary, use_container_width=True)
            
            # Add a row for totals
            totals_row = pd.DataFrame([{
                "Store": "Total (All Stores)",
                "Total_Revenue": group_summary['Total_Revenue'].sum(),
                "Total_COGS": group_summary['Total_COGS'].sum(),
                "Gross Profit": group_summary['Gross Profit'].sum(),
                "Total_Expenses": group_summary['Total_Expenses'].sum(),
                "Net Profit": group_summary['Net Profit'].sum()
            }])
            
            st.markdown("---")
            st.subheader("Consolidated Totals")
            st.dataframe(totals_row, use_container_width=True)
            
            # Download button for the group report
            st.download_button(
                label="Download Group Summary Report as Excel",
                data=to_excel(group_summary),
                file_name=f"group_summary_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("No data available across all stores to generate a group summary report.")

elif selected_page == "About":
    st.markdown('<div class="section-header">ℹ️ About This Application</div>', unsafe_allow_html=True)
    st.markdown("""
    ### Fresh Groceries Inventory Management System

    This application is a simple, browser-based inventory and sales management tool built using the **Streamlit** framework. It is designed to demonstrate key features for a small-scale retail business.

    **Key Features:**

    * **Multi-Store Management:** Easily switch between different store locations (`Main Store`, `Branch A`, `Branch B`) to manage inventory and view reports specific to each location.
    * **Inventory CRUD:** Add new products, view a list of all items, and remove products with a reason.
    * **Point of Sale (POS):** A basic POS interface to add items to a cart, apply discounts and VAT, and process sales.
    * **Transaction History:** All sales and inventory adjustments are logged in a searchable transaction history. Now includes **Payment Method** and **Transaction ID** for sales.
    * **Operating Expenses:** A new section to track and report daily operational expenses like rent, salaries, utilities, etc., specific to the selected store.
    * **Expiry Alerts:** Identifies products that have expired or are nearing their expiry date, with customizable alert periods per product, specific to the selected store.
    * **Low Stock Alerts:** Identifies products needing reordering, categorized by urgency (Low and Critical Stock), specific to the selected store.
    * **Analytics & Reports:** Generate comprehensive reports on sales, cost of goods bought, and profit/loss, including:
        * Individual store reports (Sales, Cost of Goods Bought, Cost of Sales/Profit for current store).
        * An **Overall Profit/Loss Report** for the currently selected store.
        * A **Group Report** consolidating Sales, Cost of Sales, Gross Profit, and Net Profit across **all** stores.
    * With the ability to download data in Excel format for all reports.

    **Note:** This application uses Streamlit's `st.session_state` for data persistence, meaning data will reset if the browser tab is closed or the Streamlit server restarts. For real-world use, a robust database integration (e.g., Firestore, PostgreSQL) would be required to ensure data is permanently saved.
    """)
    st.write("Developed with ❤️ using Streamlit.")
