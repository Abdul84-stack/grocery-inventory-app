import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# --- Configuration and Styling ---
st.set_page_config(layout="wide", page_title="Grocery Inventory Management")

st.markdown("""
<style>
    /* Google Fonts - Inter for a clean, modern look */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

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
        box_shadow: 0 6px 15px rgba(0, 123, 255, 0.4);
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
        box_shadow: 0 4px 8px (0,0,0,0.1);
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
    /* Receipt Styling */
    .receipt-container {
        font-family: 'monospace', 'Courier New', monospace;
        background-color: #f8f8f8;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
    }
    .receipt-header {
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 1px dashed #bbb;
        padding-bottom: 10px;
    }
    .receipt-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
    }
    /* New/Updated CSS for receipt item column alignment */
    .receipt-item-name {
        flex: 1; /* Allow name to take remaining space */
        text-align: left;
    }
    .receipt-item-qty {
        flex: 0 0 40px; /* Fixed width for quantity */
        text-align: right;
    }
    .receipt-item-price {
        flex: 0 0 80px; /* Fixed width for unit price */
        text-align: right;
    }
    .receipt-item-subtotal {
        flex: 0 0 80px; /* Fixed width for subtotal */
        text-align: right;
    }

    /* Header for receipt columns - matching item widths */
    .receipt-item-name-header {
        flex: 1;
        text-align: left;
    }
    .receipt-item-qty-header {
        flex: 0 0 40px;
        text-align: right;
    }
    .receipt-item-price-header {
        flex: 0 0 80px;
        text-align: right;
    }
    .receipt-item-subtotal-header {
        flex: 0 0 80px;
        text-align: right;
    }


    .receipt-total {
        margin-top: 15px;
        border-top: 1px dashed #bbb;
        padding-top: 10px;
        font-size: 1.2em;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
    }
    .receipt-footer {
        text-align: center;
        margin-top: 20px;
        font-size: 0.8em;
        color: #888;
    }
    .receipt-line {
        border-bottom: 1px dashed #bbb;
        margin: 5px 0;
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
            font-size: 12pt; /* Adjust font size for print */
        }
        .receipt-header, .receipt-item, .receipt-total, .receipt-footer {
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
    st.session_state.transactions = pd.DataFrame(columns=['Timestamp', 'SKU', 'Product Name', 'Quantity Change', 'Type', 'Selling Price (₦)', 'Cost Price (₦)', 'Revenue (₦)', 'Cost of Goods Sold (₦)', 'Profit/Loss (₦)', 'New Quantity', 'Store'])

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

def update_stock(sku, change_quantity, transaction_type, store, selling_price=0.0, purchase_cost_price=0.0):
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
            'Store': store # Assign to the selected store
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

def generate_receipt(cart_items, total_amount):
    receipt_str = f"""
    <div class="receipt-container">
        <div class="receipt-header">
            <h3>Habeni Diamond Kid Station</h3>
            <p>Abesan Estate, Lagos</p>
            <p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Store: {st.session_state.current_store}</p>
            <div class="receipt-line"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 10px;">
            <span class="receipt-item-name-header">Item</span>
            <span class="receipt-item-qty-header">Qty</span>
            <span class="receipt-item-price-header">Price</span>
            <span class="receipt-item-subtotal-header">Total</span>
        </div>
        <div class="receipt-line"></div>
    """
    for item in cart_items:
        # Cleaned up f-string formatting for less extraneous whitespace in generated HTML string
        receipt_str += f"""
        <div class="receipt-item">
            <span class="receipt-item-name">{item['Product Name']}</span><span class="receipt-item-qty">{item['Quantity']}</span><span class="receipt-item-price">₦{item['Unit Price']:.2f}</span><span class="receipt-item-subtotal">₦{item['Subtotal']:.2f}</span>
        </div>
        """
    receipt_str += f"""
        <div class="receipt-line"></div>
        <div class="receipt-total">
            <span>Total:</span>
            <span>₦{total_amount:.2f}</span>
        </div>
        <div class="receipt-footer">
            Thank you for your purchase!
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
        <p style="text-align: center; color: #666; font-size: 0.9em;">
            Green: Healthy Stock ({unique_healthy_items_count} products) |
            Orange: Low Stock ({low_stock_only_count} products) |
            Red: Critical Stock ({num_critical_stock} products)
        </p>
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

    tab1, tab2, tab3 = st.tabs(["View All Products", "Add New Product", "Bulk Upload Products"]) # Added new tab

    with tab1:
        st.subheader(f"All Products in Inventory for {st.session_state.current_store}")
        edited_df = st.data_editor(
            filtered_inventory,
            key="product_editor",
            use_container_width=True,
            column_config={
                "SKU": st.column_config.Column("SKU (Product No.)", help="Unique identifier for the product/back code", width="small", disabled=True),
                "Product Name": st.column_config.TextColumn("Product Name", help="Name of the product"),
                "Unit": st.column_config.TextColumn("Unit of Measure", help="e.g., kg, Units, Liters"),
                "Category": st.column_config.SelectboxColumn("Category", options=["Produce", "Dairy", "Bakery", "Meat", "Seafood", "Pantry", "Snacks", "Beverages", "Frozen", "Household", "Personal Care", "Other"]),
                "Quantity": st.column_config.NumberColumn("Quantity", help="Current stock quantity", min_value=0, format="%d"),
                "Unit Price (₦)": st.column_config.NumberColumn("Unit Price (₦)", help="Price per unit in Naira", min_value=0.01, format="%.2f"),
                "Cost Price (₦)": st.column_config.NumberColumn("Cost Price (₦)", help="Cost price per unit in Naira", min_value=0.00, format="%.2f"),
                "Reorder Point": st.column_config.NumberColumn("Reorder Point", help="Quantity at which to reorder", min_value=0, format="%d"),
                "Expiry Date": st.column_config.DateColumn("Expiry Date", help="Date the product expires", format="YYYY-MM-DD"),
                "Last Updated": st.column_config.DatetimeColumn("Last Updated", format="YYYY-MM-DD HH:mm:ss", disabled=True)
            },
            num_rows="dynamic"
        )
        if not edited_df.equals(filtered_inventory):
            # Update only the relevant rows in the main inventory DataFrame
            st.session_state.inventory = pd.concat([st.session_state.inventory[st.session_state.inventory['Store'] != st.session_state.current_store], edited_df], ignore_index=True)
            # Ensure 'Last Updated' is updated for any manual edits
            st.session_state.inventory.loc[st.session_state.inventory['Store'] == st.session_state.current_store, 'Last Updated'] = datetime.now()
            st.success("Inventory updated!")
            st.rerun()

    with tab2:
        st.subheader(f"Add New Product for {st.session_state.current_store}")
        with st.form("add_product_form"):
            new_sku = st.text_input("Product SKU (Back Code - Unique Identifier)", help="e.g., PROD001, Milo45kg").strip()
            new_name = st.text_input("Product Name", placeholder="e.g., Fuji Apples, Fresh Milk").strip()
            new_unit = st.text_input("Unit of Measure", placeholder="e.g., kg, Units, Liters").strip()
            new_category = st.selectbox("Category", ["Produce", "Dairy", "Bakery", "Meat", "Seafood", "Pantry", "Snacks", "Beverages", "Frozen", "Household", "Personal Care", "Other"])
            new_quantity = st.number_input("Initial Quantity", min_value=0, value=0)
            new_selling_price = st.number_input("Unit Selling Price (₦)", min_value=0.01, format="%.2f")
            new_cost_price = st.number_input("Initial Cost Price (₦)", min_value=0.00, format="%.2f", help="The cost at which you buy this product.")
            new_reorder_point = st.number_input("Reorder Point", min_value=0, value=0, help="Quantity at which to trigger a reorder alert.")
            new_expiry_date = st.date_input("Expiry Date", value=datetime.now().date() + timedelta(days=365))

            add_submitted = st.form_submit_button("Add Product")
            if add_submitted:
                if new_sku and new_name and new_unit and new_quantity >= 0 and new_selling_price > 0 and new_cost_price >= 0:
                    if add_product(new_sku, new_name, new_unit, new_category, new_quantity, new_selling_price, new_cost_price, new_reorder_point, new_expiry_date, st.session_state.current_store):
                        st.rerun()
                else:
                    st.error("Please fill in all required fields (SKU, Product Name, Unit, Quantity, Unit Selling Price, Initial Cost Price, Reorder Point, Expiry Date) and ensure valid values.")

    with tab3: # Bulk Upload Products Tab
        st.subheader(f"Bulk Upload Products (CSV/Excel) for {st.session_state.current_store}")
        st.info("""
        Upload a CSV or Excel file with your new purchased items.
        The file should contain the following columns (case-insensitive, exact spelling is recommended):
        - `SKU` (mandatory, unique identifier)
        - `Product Name` (mandatory)
        - `Quantity` (mandatory, integer)
        - `Unit Price (₦)` (mandatory, numeric - selling price)
        - `Cost Price (₦)` (mandatory, numeric - purchase cost)
        - `Unit` (optional, e.g., 'kg', 'Units')
        - `Category` (optional)
        - `Reorder Point` (optional, integer)
        - `Expiry Date` (optional,YYYY-MM-DD format)

        If an `SKU` already exists in the current store, its `Quantity` will be *added to* the current stock, and its `Cost Price (₦)` will be *updated* to the value in the uploaded file.
        """)

        uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    uploaded_df = pd.read_csv(uploaded_file)
                else: # .xlsx
                    uploaded_df = pd.read_excel(uploaded_file)

                st.write("Preview of Uploaded Data:")
                st.dataframe(uploaded_df, use_container_width=True)

                if st.button("Process Uploaded Products"):
                    required_columns = ['SKU', 'Product Name', 'Quantity', 'Unit Price (₦)', 'Cost Price (₦)']
                    # Check for required columns (case-insensitive)
                    uploaded_columns_lower = [col.lower() for col in uploaded_df.columns]
                    missing_columns = [col for col in required_columns if col.lower() not in uploaded_columns_lower]

                    if missing_columns:
                        st.error(f"Missing required columns in the uploaded file: {', '.join(missing_columns)}")
                    else:
                        success_count = 0
                        update_count = 0
                        add_count = 0
                        errors = []

                        # Normalize column names to match internal dataframe
                        uploaded_df.columns = [col.replace(' (₦)', ' (₦)') for col in uploaded_df.columns]
                        uploaded_df.columns = [col.replace(' (N)', ' (₦)') for col in uploaded_df.columns] # Handle N if user uses it

                        for index, row in uploaded_df.iterrows():
                            sku = str(row['SKU']).strip().upper()
                            product_name = str(row['Product Name']).strip()
                            quantity_to_add = int(row['Quantity'])
                            selling_price = float(row['Unit Price (₦)'])
                            cost_price = float(row['Cost Price (₦)'])
                            
                            unit = str(row.get('Unit', 'Units')).strip()
                            category = str(row.get('Category', 'Other')).strip()
                            reorder_point = int(row.get('Reorder Point', 0))
                            
                            expiry_date_val = row.get('Expiry Date')
                            if pd.isna(expiry_date_val):
                                expiry_date = datetime.now().date() + timedelta(days=365*5) # Default to 5 years if not provided
                            else:
                                try:
                                    if isinstance(expiry_date_val, datetime):
                                        expiry_date = expiry_date_val.date()
                                    else:
                                        expiry_date = pd.to_datetime(expiry_date_val).date()
                                except Exception:
                                    expiry_date = datetime.now().date() + timedelta(days=365*5) # Fallback on error


                            existing_product_idx = st.session_state.inventory[(st.session_state.inventory['SKU'] == sku) & (st.session_state.inventory['Store'] == st.session_state.current_store)].index

                            if not existing_product_idx.empty:
                                # Product exists, update quantity and cost price for the current store
                                current_inventory_qty = st.session_state.inventory.loc[existing_product_idx[0], 'Quantity']
                                st.session_state.inventory.loc[existing_product_idx[0], 'Quantity'] = current_inventory_qty + quantity_to_add
                                st.session_state.inventory.loc[existing_product_idx[0], 'Cost Price (₦)'] = cost_price # Update to new purchase cost
                                st.session_state.inventory.loc[existing_product_idx[0], 'Last Updated'] = datetime.now()
                                
                                # Record purchase transaction for the update
                                update_stock(sku, quantity_to_add, "Purchase (Stock In)", st.session_state.current_store, purchase_cost_price=cost_price)
                                update_count += 1
                            else:
                                # New product, add to inventory for the current store
                                # Use the add_product helper function
                                if add_product(sku, product_name, unit, category, quantity_to_add, selling_price, cost_price, reorder_point, expiry_date, st.session_state.current_store):
                                    # Manually record the initial purchase transaction for new products
                                    update_stock(sku, quantity_to_add, "Purchase (Stock In)", st.session_state.current_store, purchase_cost_price=cost_price)
                                    add_count += 1
                                else:
                                    errors.append(f"Failed to add new product {product_name} (SKU: {sku})")
                            success_count += 1
                        
                        st.success(f"Processed {success_count} rows: {add_count} new products added, {update_count} existing products updated for {st.session_state.current_store}.")
                        if errors:
                            st.error("Errors encountered during processing:\n" + "\n".join(errors))
                        st.rerun()

            except Exception as e:
                st.error(f"Error reading file or processing data: {e}. Please ensure the file format and column names are correct.")
        else:
            st.info(f"Upload a CSV or Excel file to begin bulk processing for {st.session_state.current_store}.")


elif selected_page == "Point of Sale": # New POS section
    st.markdown('<div class="section-header">💰 Point of Sale (POS)</div>', unsafe_allow_html=True)

    # Initialize cart in session state if not present
    if 'cart' not in st.session_state: # Corrected from 'current_cart'
        st.session_state.cart = [] # {'SKU', 'Product Name', 'Quantity', 'Unit Price', 'Subtotal'}
    
    col_input, col_cart = st.columns([1, 1.5]) # Two columns for input and cart display

    with col_input:
        st.subheader(f"Add Item to Cart ({st.session_state.current_store})")
        # Creating product options with SKU and Product Name for cleaner dropdown
        product_options = filtered_inventory.apply(lambda row: f"{row['SKU']} - {row['Product Name']}", axis=1).tolist()
        
        if not product_options:
            st.warning(f"No products in inventory for {st.session_state.current_store} to sell. Please add products first under 'Manage Products'.")
        else:
            selected_product_display_name = st.selectbox("Select Product:", product_options, key="pos_product_select")
            
            # Extract SKU from the selected option
            selected_sku_pos = selected_product_display_name.split(' - ')[0] if selected_product_display_name else None

            # Get details of the selected product
            product_details = filtered_inventory[filtered_inventory['SKU'].str.upper() == selected_sku_pos.upper()]
            
            if not product_details.empty:
                product_details = product_details.iloc[0]
                available_qty = int(product_details['Quantity'])
                unit_selling_price = product_details['Unit Price (₦)'] # Renamed for clarity
                
                st.info(f"Available Stock: {available_qty} {product_details['Unit']} | Unit Selling Price: ₦{unit_selling_price:.2f}")

                # Max value of quantity_to_add is the available stock
                quantity_to_add = st.number_input(f"Quantity for '{product_details['Product Name']}'", min_value=1, max_value=available_qty, value=1, key="qty_to_add_pos")
                
                if st.button("Add to Cart", key="add_to_cart_btn"):
                    if selected_sku_pos and quantity_to_add > 0:
                        # Check if item already in cart, update quantity
                        found_in_cart = False
                        for item in st.session_state.cart:
                            if item['SKU'] == selected_sku_pos:
                                # Ensure adding to cart doesn't exceed available stock
                                if (item['Quantity'] + quantity_to_add) > available_qty:
                                    st.error(f"Cannot add {quantity_to_add} more. Only {available_qty - item['Quantity']} remaining to reach available stock.")
                                else:
                                    item['Quantity'] += quantity_to_add
                                    item['Subtotal'] = item['Quantity'] * item['Unit Price']
                                    st.success(f"Added {quantity_to_add} more of '{product_details['Product Name']}' to cart. Current cart quantity: {item['Quantity']}")
                                found_in_cart = True
                                break
                        
                        if not found_in_cart:
                            if quantity_to_add > available_qty:
                                st.error(f"Cannot add {quantity_to_add}. Only {available_qty} available in stock.")
                            else:
                                item_subtotal = quantity_to_add * unit_selling_price
                                st.session_state.cart.append({
                                    "SKU": selected_sku_pos,
                                    "Product Name": product_details['Product Name'],
                                    "Quantity": quantity_to_add,
                                    "Unit Price": unit_selling_price, # This is the selling price
                                    "Subtotal": item_subtotal
                                })
                                st.success(f"Added {quantity_to_add} units of '{product_details['Product Name']}' to cart.")
                        st.rerun() # Rerun to update cart display and stock info

            else:
                st.info("Select a product to view details and add to cart.")

    with col_cart:
        st.subheader("Customer Cart")
        if st.session_state.cart:
            cart_df = pd.DataFrame(st.session_state.cart)
            st.dataframe(cart_df[['Product Name', 'Quantity', 'Unit Price', 'Subtotal']], use_container_width=True, hide_index=True)
            
            total_cart_amount = cart_df['Subtotal'].sum()
            st.markdown(f"### **Total Amount: ₦{total_cart_amount:.2f}**")

            col_finalize, col_clear, col_print_download = st.columns(3) # Adjusted column for print and download
            with col_finalize:
                if st.button("Finalize Sale & Generate Receipt", key="finalize_sale_btn"):
                    sale_successful = True
                    failed_item_name = None
                    
                    for item in st.session_state.cart:
                        sku = item['SKU']
                        qty_sold = item['Quantity']
                        selling_price = item['Unit Price']
                        
                        if not update_stock(sku, qty_sold, "Sale", st.session_state.current_store, selling_price=selling_price):
                            failed_item_name = item['Product Name']
                            sale_successful = False
                            break
                    
                    if sale_successful:
                        receipt_content = generate_receipt(st.session_state.cart, total_cart_amount)
                        st.session_state.receipt_history.append(receipt_content)
                        
                        st.success("Sale finalized! Receipt generated. Stock levels updated.")
                        st.session_state.cart = []
                        st.session_state.last_receipt = receipt_content
                        st.rerun()
                    else:
                        st.error(f"Sale could not be finalized due to insufficient stock for '{failed_item_name}'. Please adjust quantity or clear cart.")
            with col_clear:
                if st.button("Clear Cart", key="clear_cart_btn"):
                    st.session_state.cart = []
                    st.session_state.last_receipt = ""
                    st.info("Cart cleared.")
                    st.rerun()

        else:
            st.info("Cart is empty.")
    
    if st.session_state.last_receipt:
        st.subheader("Last Generated Receipt:")
        st.markdown(st.session_state.last_receipt, unsafe_allow_html=True)
        
        col_print, col_download = st.columns(2) # New columns for print and download buttons
        with col_print:
            if st.button("Print This Receipt", key="print_last_receipt_btn"):
                st.components.v1.html(
                    """
                    <script>
                        window.print();
                    </script>
                    """,
                    height=0,
                    width=0
                )
        with col_download:
            # Download as HTML, user can then print to PDF from browser
            st.download_button(
                label="Download Receipt as HTML",
                data=st.session_state.last_receipt,
                file_name=f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                key="download_receipt_html_btn"
            )


elif selected_page == "Record Transactions":
    st.markdown('<div class="section-header">✍️ Record Sales & Stock In</div>', unsafe_allow_html=True)

    transaction_tab, lookup_tab = st.tabs(["Record Individual Transaction", "Product Lookup by Back Code"])

    with transaction_tab:
        st.subheader(f"Record Single Inventory Movement for {st.session_state.current_store}")
        transaction_type = st.radio("Select Transaction Type:", ["Sale", "Purchase (Stock In)"])

        product_options_list = filtered_inventory.apply(lambda row: f"{row['SKU']} - {row['Product Name']}", axis=1).tolist()


        if not product_options_list:
            st.warning(f"No products in inventory for {st.session_state.current_store}. Please add products first under 'Manage Products'.")
        else:
            with st.form("transaction_form"):
                selected_product_option = st.selectbox("Select Product:", product_options_list, key="transaction_product_select")
                selected_sku_for_transaction = selected_product_option.split(' - ')[0] if selected_product_option else None

                quantity_change = st.number_input("Quantity:", min_value=1, value=1)
                
                purchase_cost_input = 0.0
                if transaction_type == "Purchase (Stock In)":
                    product_current_cost = filtered_inventory[filtered_inventory['SKU'].str.upper() == selected_sku_for_transaction.upper()]['Cost Price (₦)'].iloc[0] if selected_sku_for_transaction else 0.0
                    purchase_cost_input = st.number_input(f"Purchase Cost Price (₦) for '{selected_product_option.split(' - ')[1] if selected_product_option else ''}' (Current: ₦{product_current_cost:.2f})", min_value=0.00, format="%.2f", value=float(product_current_cost))


                submitted_transaction = st.form_submit_button(f"Record {transaction_type}")
                if submitted_transaction:
                    if selected_sku_for_transaction and quantity_change > 0:
                        if transaction_type == "Sale":
                            selling_price_for_manual_sale = filtered_inventory[filtered_inventory['SKU'].str.upper() == selected_sku_for_transaction.upper()]['Unit Price (₦)'].iloc[0]
                            if update_stock(selected_sku_for_transaction, quantity_change, transaction_type, st.session_state.current_store, selling_price=selling_price_for_manual_sale):
                                st.rerun()
                        elif transaction_type == "Purchase (Stock In)":
                            if update_stock(selected_sku_for_transaction, quantity_change, transaction_type, st.session_state.current_store, purchase_cost_price=purchase_cost_input):
                                st.rerun()
                    else:
                        st.error("Please select a product and enter a valid quantity.")

    with lookup_tab:
        st.subheader(f"Lookup Product by Back Code (SKU) for {st.session_state.current_store}")
        lookup_sku = st.text_input("Enter Product Back Code (SKU):", key="lookup_sku_input").strip()

        if lookup_sku:
            found_product = filtered_inventory[filtered_inventory['SKU'].str.upper() == lookup_sku.upper()]
            if not found_product.empty:
                product_data = found_product.iloc[0]
                st.success(f"Product Found: **{product_data['Product Name']}**")
                st.write(f"**SKU / Product Number:** {product_data['SKU']}")
                st.write(f"**Current Stock Level:** {product_data['Quantity']} {product_data['Unit']}")
                st.write(f"**Unit Selling Price:** ₦{product_data['Unit Price (₦)']:.2f}")
                st.write(f"**Current Cost Price:** ₦{product_data['Cost Price (₦)']:.2f}")
                st.write(f"**Category:** {product_data['Category']}")
                st.write(f"**Reorder Point:** {product_data['Reorder Point']}")
                st.write(f"**Expiry Date:** {product_data['Expiry Date'].strftime('%Y-%m-%d')}")
            else:
                st.warning(f"No product found with Back Code (SKU): '{lookup_sku}' in {st.session_state.current_store}.")
        else:
            st.info(f"Enter a product back code (SKU) to look up its details for {st.session_state.current_store}.")

elif selected_page == "Operating Expenses": # NEW SECTION FOR OPERATING EXPENSES
    st.markdown('<div class="section-header">💸 Operating Expenses</div>', unsafe_allow_html=True)

    st.subheader(f"Record New Operating Expense for {st.session_state.current_store}")
    with st.form("add_expense_form"):
        expense_date = st.date_input("Date of Expense", value=datetime.now().date())
        expense_category = st.selectbox("Expense Category", [
            "Salaries", "Rent", "Electricity Bills", "Internet Services",
            "Generator Fuel", "Generator Maintenance", "Transport",
            "Office Cleaning", "Office Maintenance", "Marketing", "Other"
        ])
        expense_description = st.text_area("Description", placeholder="e.g., Monthly rent payment, Diesel refill")
        expense_amount = st.number_input("Amount (₦)", min_value=0.00, format="%.2f")

        add_expense_submitted = st.form_submit_button("Add Expense")
        if add_expense_submitted:
            if expense_date and expense_category and expense_amount > 0:
                new_expense = pd.DataFrame([{
                    "Date": expense_date,
                    "Category": expense_category,
                    "Description": expense_description,
                    "Amount (₦)": expense_amount,
                    "Store": st.session_state.current_store # Assign to current store
                }])
                st.session_state.operating_expenses = pd.concat([st.session_state.operating_expenses, new_expense], ignore_index=True)
                st.success(f"Recorded expense: {expense_category} - ₦{expense_amount:.2f} for {st.session_state.current_store}")
                st.rerun()
            else:
                st.error("Please fill in all required fields and ensure the amount is valid.")

    st.markdown("---")
    st.subheader(f"Summary of Operating Expenses for {st.session_state.current_store}")
    if not filtered_expenses.empty:
        total_expenses = filtered_expenses['Amount (₦)'].sum()
        st.markdown(f"""
        <div class="report-card red">
            <div class="value">₦{total_expenses:,.2f}</div>
            <div class="label">Total Operating Expenses</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader(f"Detailed Operating Expenses for {st.session_state.current_store}")
        st.dataframe(filtered_expenses.sort_values(by='Date', ascending=False), use_container_width=True)

        csv_expenses = to_excel(filtered_expenses)
        st.download_button(
            label="Download Operating Expenses as Excel",
            data=csv_expenses,
            file_name=f"operating_expenses_report_{st.session_state.current_store.replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_expenses_excel"
        )
    else:
        st.info(f"No operating expenses recorded yet for {st.session_state.current_store}.")


elif selected_page == "Expiry Alerts":
    st.markdown('<div class="section-header">🗓️ Expiry Alerts</div>', unsafe_allow_html=True)

    today = datetime.now().date()
    
    expired_items = filtered_inventory[filtered_inventory['Expiry Date'] < today].sort_values(by="Expiry Date")
    
    expiring_soon_items_list = []
    for index, row in filtered_inventory.iterrows():
        product_expiry_date = row['Expiry Date']
        product_name = row['Product Name']
        
        # Ensure product_name is a string before calling .lower()
        if pd.notna(product_name) and str(product_name).strip().lower() == "gala sausage":
            alert_days = GALA_SAUSAGE_EXPIRY_ALERT_DAYS
        else:
            alert_days = DEFAULT_EXPIRY_ALERT_DAYS
        
        if today <= product_expiry_date <= today + timedelta(days=alert_days):
            expiring_soon_items_list.append(row)
            
    expiring_soon_items_df = pd.DataFrame(expiring_soon_items_list)
    if not expiring_soon_items_df.empty:
        expiring_soon_items_df = expiring_soon_items_df.sort_values(by="Expiry Date")


    st.subheader(f"Expired Products in {st.session_state.current_store}")
    if not expired_items.empty:
        st.error(f"⚠️ **{len(expired_items)} product(s) have already expired!** Please remove these from shelves.")
        st.dataframe(expired_items[['SKU', 'Product Name', 'Quantity', 'Expiry Date', 'Unit']], use_container_width=True)
    else:
        st.info(f"No products have expired in {st.session_state.current_store}.")

    st.subheader(f"Products Expiring Soon in {st.session_state.current_store}")
    if not expiring_soon_items_df.empty:
        st.warning(f"🗓️ The following **{len(expiring_soon_items_df)} product(s) are expiring soon!** Consider promotions or re-stocking.")
        expiring_soon_items_df['Days Until Expiry'] = (expiring_soon_items_df['Expiry Date'] - today).dt.days
        st.dataframe(expiring_soon_items_df[['SKU', 'Product Name', 'Quantity', 'Expiry Date', 'Days Until Expiry', 'Unit']], use_container_width=True)
    else:
        st.info(f"No products are expiring within their alert periods in {st.session_state.current_store}.")


elif selected_page == "Low Stock Alerts":
    st.markdown('<div class="section-header">🚨 Low Stock Alerts</div>', unsafe_allow_html=True)

    low_stock_items = filtered_inventory[filtered_inventory['Quantity'] <= filtered_inventory['Reorder Point']].sort_values(by="Quantity")
    critical_stock_items = filtered_inventory[filtered_inventory['Quantity'] <= CRITICAL_STOCK_THRESHOLD].sort_values(by="Quantity")

    st.markdown(f"### Critical Stock Products (Quantity $\\le$ {CRITICAL_STOCK_THRESHOLD}) in {st.session_state.current_store}", unsafe_allow_html=True)
    if not critical_stock_items.empty:
        st.markdown(f"""
        <div class="low-stock-alert">
            <p><strong>Critical Stock! Immediate Attention Required:</strong> These items are running extremely low.</p>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(critical_stock_items[['SKU', 'Product Name', 'Category', 'Quantity', 'Reorder Point', 'Last Updated']], use_container_width=True)
    else:
        st.info(f"No products are at critical stock levels in {st.session_state.current_store}.")

    st.subheader(f"Products Below Reorder Point in {st.session_state.current_store}")
    general_low_stock_only = low_stock_items[~low_stock_items['SKU'].isin(critical_stock_items['SKU'])]

    if not general_low_stock_only.empty:
        st.markdown(f"""
        <div class="low-stock-alert" style="background-color: #ffead6; color: #cc6600; border-left: 6px solid #ff9933;">
            <p><strong>Low Stock Warning!</strong> These items are below their reorder point and might need to be restocked soon.</p>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(general_low_stock_only[['SKU', 'Product Name', 'Category', 'Quantity', 'Reorder Point', 'Last Updated']], use_container_width=True)
    else:
        if critical_stock_items.empty:
            st.info(f"No products are currently low in stock in {st.session_state.current_store}. All good!")
        else:
            st.info(f"All products currently below reorder point are at critical stock levels in {st.session_state.current_store}.")

elif selected_page == "Analytics & Reports":
    st.markdown('<div class="section-header">📈 Analytics & Reports</div>', unsafe_allow_html=True)

    report_tabs = st.tabs(["Sales Report", "Cost of Goods Bought Report", "Cost of Sales Report", "Overall Profit/Loss Report (Current Store)", "Group Report (All Stores)"]) # Added overall profit/loss

    with report_tabs[0]: # Sales Report Tab
        st.subheader(f"Daily Sales Report for {st.session_state.current_store}")
        sales_transactions = filtered_transactions[filtered_transactions['Type'] == 'Sale'].copy()

        if not sales_transactions.empty:
            total_revenue = sales_transactions['Revenue (₦)'].sum()
            total_items_sold = sales_transactions['Quantity Change'].abs().sum()

            col_sales_rev, col_items_sold = st.columns(2)
            with col_sales_rev:
                st.markdown(f"""
                <div class="report-card blue">
                    <div class="value">₦{total_revenue:,.2f}</div>
                    <div class="label">Total Sales Revenue</div>
                </div>
                """, unsafe_allow_html=True)
            with col_items_sold:
                st.markdown(f"""
                <div class="report-card">
                    <div class="value">{total_items_sold:,.0f}</div>
                    <div class="label">Total Items Sold</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("Detailed Sales Transactions")
            sales_report_df = sales_transactions[['Timestamp', 'Product Name', 'Quantity Change', 'Selling Price (₦)', 'Revenue (₦)']].copy()
            sales_report_df.rename(columns={'Quantity Change': 'Quantity Sold'}, inplace=True)
            sales_report_df['Quantity Sold'] = sales_report_df['Quantity Sold'].abs()
            
            st.dataframe(sales_report_df.sort_values(by='Timestamp', ascending=False), use_container_width=True)

            csv = to_excel(sales_report_df)
            st.download_button(
                label="Download Sales Report as Excel",
                data=csv,
                file_name=f"sales_report_{st.session_state.current_store.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_sales_excel"
            )
        else:
            st.info(f"No sales transactions recorded yet for {st.session_state.current_store}.")

    with report_tabs[1]: # Cost of Goods Bought Report Tab
        st.subheader(f"Cost of Goods Bought Report for {st.session_state.current_store}")
        purchase_transactions = filtered_transactions[filtered_transactions['Type'] == 'Purchase (Stock In)'].copy()

        if not purchase_transactions.empty:
            total_cost_of_goods_bought = purchase_transactions['Cost of Goods Bought (₦)'].sum()
            total_items_bought = purchase_transactions['Quantity Change'].sum()

            col_purchase_cost, col_items_bought = st.columns(2)
            with col_purchase_cost:
                st.markdown(f"""
                <div class="report-card red">
                    <div class="value">₦{total_cost_of_goods_bought:,.2f}</div>
                    <div class="label">Total Procurement Cost</div>
                </div>
                """, unsafe_allow_html=True)
            with col_items_bought:
                st.markdown(f"""
                <div class="report-card">
                    <div class="value">{total_items_bought:,.0f}</div>
                    <div class="label">Total Items Procured</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("Detailed Purchase Transactions")
            purchase_report_df = purchase_transactions[['Timestamp', 'Product Name', 'Quantity Change', 'Cost Price (₦)', 'Cost of Goods Bought (₦)']].copy()
            purchase_report_df.rename(columns={'Quantity Change': 'Quantity Bought'}, inplace=True)
            
            st.dataframe(purchase_report_df.sort_values(by='Timestamp', ascending=False), use_container_width=True)

            csv = to_excel(purchase_report_df)
            st.download_button(
                label="Download Cost of Goods Bought Report as Excel",
                data=csv,
                file_name=f"cost_of_goods_bought_report_{st.session_state.current_store.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_cogs_bought_excel"
            )
        else:
            st.info(f"No purchase transactions recorded yet for {st.session_state.current_store}.")

    with report_tabs[2]: # Cost of Sales / COGS Report Tab
        st.subheader(f"Cost of Sales (COGS) Report for {st.session_state.current_store}")
        cogs_transactions = filtered_transactions[filtered_transactions['Type'] == 'Sale'].copy() # COGS is tied to sales

        if not cogs_transactions.empty:
            total_cogs = cogs_transactions['Cost of Goods Sold (₦)'].sum()

            st.markdown(f"""
            <div class="report-card red">
                <div class="value">₦{total_cogs:,.2f}</div>
                <div class="label">Total Cost of Sales (COGS)</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("Detailed Cost of Sales Transactions")
            cogs_report_df = cogs_transactions[['Timestamp', 'Product Name', 'Quantity Change', 'Cost Price (₦)', 'Cost of Goods Sold (₦)']].copy()
            cogs_report_df.rename(columns={'Quantity Change': 'Quantity Sold'}, inplace=True)
            cogs_report_df['Quantity Sold'] = cogs_report_df['Quantity Sold'].abs() # Display as positive quantity
            
            st.dataframe(cogs_report_df.sort_values(by='Timestamp', ascending=False), use_container_width=True)

            csv = to_excel(cogs_report_df)
            st.download_button(
                label="Download Cost of Sales Report as Excel",
                data=csv,
                file_name=f"cost_of_sales_report_{st.session_state.current_store.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_cogs_excel"
            )
        else:
            st.info(f"No sales (and thus no Cost of Sales) transactions recorded yet for {st.session_state.current_store}.")
            
    with report_tabs[3]: # Overall Profit/Loss Report (Current Store)
        st.subheader(f"Overall Profit/Loss Report for {st.session_state.current_store}")

        sales_for_profit = filtered_transactions[filtered_transactions['Type'] == 'Sale'].copy()
        
        if not sales_for_profit.empty or not filtered_expenses.empty:
            gross_profit = sales_for_profit['Profit/Loss (₦)'].sum() # This is the "Gross Profit" from sales
            total_operating_expenses = filtered_expenses['Amount (₦)'].sum()
            net_profit_loss = gross_profit - total_operating_expenses

            col_gross_profit, col_net_profit = st.columns(2)
            with col_gross_profit:
                st.markdown(f"""
                <div class="report-card {'green' if gross_profit >= 0 else 'red'}">
                    <div class="value">₦{gross_profit:,.2f}</div>
                    <div class="label">Gross Profit (Sales)</div>
                </div>
                """, unsafe_allow_html=True)
            with col_net_profit:
                st.markdown(f"""
                <div class="report-card {'green' if net_profit_loss >= 0 else 'red'}">
                    <div class="value">₦{net_profit_loss:,.2f}</div>
                    <div class="label">Net Profit/Loss (After Expenses)</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("Summary Breakdown")
            st.write(f"**Total Sales Revenue:** ₦{sales_for_profit['Revenue (₦)'].sum():,.2f}")
            st.write(f"**Total Cost of Goods Sold (COGS):** ₦{sales_for_profit['Cost of Goods Sold (₦)'].sum():,.2f}")
            st.write(f"**Total Operating Expenses:** ₦{total_operating_expenses:,.2f}")

            profit_loss_data = {
                'Metric': ['Total Sales Revenue', 'Total Cost of Goods Sold (COGS)', 'Gross Profit', 'Total Operating Expenses', 'Net Profit/Loss'],
                'Amount (₦)': [
                    sales_for_profit['Revenue (₦)'].sum(),
                    sales_for_profit['Cost of Goods Sold (₦)'].sum(),
                    gross_profit,
                    total_operating_expenses,
                    net_profit_loss
                ]
            }
            profit_loss_df = pd.DataFrame(profit_loss_data)
            st.dataframe(profit_loss_df, hide_index=True, use_container_width=True)

            csv = to_excel(profit_loss_df)
            st.download_button(
                label="Download Profit/Loss Report (Current Store) as Excel",
                data=csv,
                file_name=f"profit_loss_report_{st.session_state.current_store.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_profit_loss_current_store_excel"
            )

        else:
            st.info(f"No sales or operating expenses recorded yet for {st.session_state.current_store} to generate a Profit/Loss Report.")


    with report_tabs[4]: # Group Report (All Stores)
        st.subheader("Group Report: Consolidated Sales, Cost, and Profit Across All Stores")

        all_sales_transactions = st.session_state.transactions[st.session_state.transactions['Type'] == 'Sale'].copy()
        all_operating_expenses = st.session_state.operating_expenses.copy()

        if not all_sales_transactions.empty or not all_operating_expenses.empty:
            # Aggregate by store for sales
            sales_by_store = all_sales_transactions.groupby('Store').agg(
                Total_Revenue=('Revenue (₦)', 'sum'),
                Total_COGS=('Cost of Goods Sold (₦)', 'sum'),
                Gross_Profit=('Profit/Loss (₦)', 'sum')
            ).reset_index()

            # Aggregate by store for expenses
            expenses_by_store = all_operating_expenses.groupby('Store').agg(
                Total_Expenses=('Amount (₦)', 'sum')
            ).reset_index()

            # Merge sales and expenses data
            group_report_df = pd.merge(sales_by_store, expenses_by_store, on='Store', how='outer').fillna(0)

            # Calculate Net Profit/Loss for each store
            group_report_df['Net Profit/Loss'] = group_report_df['Gross_Profit'] - group_report_df['Total_Expenses']
            
            st.dataframe(group_report_df, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.subheader("Overall Group Totals:")

            overall_total_revenue = group_report_df['Total_Revenue'].sum()
            overall_total_cogs = group_report_df['Total_COGS'].sum()
            overall_gross_profit = group_report_df['Gross_Profit'].sum()
            overall_total_expenses = group_report_df['Total_Expenses'].sum()
            overall_net_profit_loss = overall_gross_profit - overall_total_expenses

            col_group_revenue, col_group_gross_profit, col_group_net_profit = st.columns(3)
            with col_group_revenue:
                st.markdown(f"""
                <div class="report-card blue">
                    <div class="value">₦{overall_total_revenue:,.2f}</div>
                    <div class="label">Group Total Revenue</div>
                </div>
                """, unsafe_allow_html=True)
            with col_group_gross_profit:
                st.markdown(f"""
                <div class="report-card {'green' if overall_gross_profit >= 0 else 'red'}">
                    <div class="value">₦{overall_gross_profit:,.2f}</div>
                    <div class="label">Group Gross Profit</div>
                </div>
                """, unsafe_allow_html=True)
            with col_group_net_profit:
                st.markdown(f"""
                <div class="report-card {'green' if overall_net_profit_loss >= 0 else 'red'}">
                    <div class="value">₦{overall_net_profit_loss:,.2f}</div>
                    <div class="label">Group Net Profit/Loss</div>
                </div>
                """, unsafe_allow_html=True)
            
            group_summary_data = {
                'Metric': ['Overall Total Sales Revenue', 'Overall Total Cost of Goods Sold (COGS)', 'Overall Gross Profit', 'Overall Total Operating Expenses', 'Overall Net Profit/Loss'],
                'Amount (₦)': [
                    overall_total_revenue,
                    overall_total_cogs,
                    overall_gross_profit,
                    overall_total_expenses,
                    overall_net_profit_loss
                ]
            }
            group_summary_df = pd.DataFrame(group_summary_data)
            st.dataframe(group_summary_df, hide_index=True, use_container_width=True)

            csv = to_excel(group_report_df)
            st.download_button(
                label="Download Group Report as Excel",
                data=csv,
                file_name=f"group_profit_loss_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_group_report_excel"
            )

        else:
            st.info("No sales or operating expenses recorded across all stores to generate a Group Report.")


elif selected_page == "About":
    st.markdown('<div class="section-header">ℹ️ About This Application</div>', unsafe_allow_html=True)
    st.write("""
    This is a **Grocery Inventory Management System** designed to help small businesses,
    especially grocery stores and supermarkets, efficiently manage their stock, track sales,
    monitor expenses, and generate insightful reports.

    **Key Features:**

    * **Multi-Store Support:** Manage inventory, sales, and expenses across multiple store locations.
    * **Product Management:** Add, view, and update product details including SKU, name, quantity,
        prices (cost and selling), reorder points, and expiry dates.
    * **Bulk Product Upload:** Easily add or update multiple products using CSV or Excel files,
        which intelligently adds to existing stock and updates cost prices for purchases.
    * **Point of Sale (POS):** A streamlined interface to process sales, add products to a cart,
        and generate receipts.
    * **Transaction Logging:** Automatically records all sales and stock deliveries (purchases),
        including updating cost prices for purchases, specific to the selected store.
    * **Operating Expenses:** A new section to track and report daily operational expenses like
        rent, salaries, utilities, etc., specific to the selected store.
    * **Expiry Alerts:** Identifies products that have expired or are nearing their expiry date,
        with customizable alert periods per product, specific to the selected store.
    * **Low Stock Alerts:** Identifies products needing reordering, categorized by urgency (Low and Critical Stock),
        specific to the selected store.
    * **Analytics & Reports:** Generate comprehensive reports on sales, cost of goods bought, and profit/loss, including:
        * Individual store reports (Sales, Cost of Goods Bought, Cost of Sales/Profit for current store).
        * An **Overall Profit/Loss Report** for the currently selected store.
        * A **Group Report** consolidating Sales, Cost of Sales, Gross Profit, and Net Profit across **all** stores.
    * With the ability to download data in Excel format for all reports.

    **Note:** This application uses Streamlit's `st.session_state` for data persistence, meaning data
    will reset if the browser tab is closed or the Streamlit server restarts. For real-world
    use, a robust database integration (e.g., Firestore, PostgreSQL) would be required to ensure
    data is permanently saved.
    """)
    st.write("Developed with ❤️ using Streamlit.")
