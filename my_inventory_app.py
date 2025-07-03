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
        box-shadow: 0 6px 15px rgba(0, 123, 255, 0.4);
        transform: translateY(-2px);
    }
    .stButton > button:active {
        background-color: #004085;
        transform: translateY(0);
        box-shadow: 0 2px 5px rgba(0, 123, 255, 0.5);
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
            unit = st.text_input("Unit (e.g., Kg, Liters, Pcs)").strip()
            selling_price = st.number_input("Unit Price (₦)", min_value=0.0, format="%.2f")
            cost_price = st.number_input("Cost Price (₦)", min_value=0.0, format="%.2f", help="The cost at which you purchase this product.")
            reorder_point = st.number_input("Reorder Point", min_value=0, step=1, help="Quantity at which to reorder this product.")
            expiry_date = st.date_input("Expiry Date", min_value=datetime.now().date())
        
        add_product_submitted = st.form_submit_button("Add Product")
        if add_product_submitted:
            if sku and product_name and unit and category and quantity >= 0 and selling_price >= 0 and cost_price >= 0 and reorder_point >= 0 and expiry_date:
                if add_product(sku, product_name, unit, category, quantity, selling_price, cost_price, reorder_point, expiry_date, st.session_state.current_store):
                    st.rerun() # Rerun to update the displayed inventory
            else:
                st.error("Please fill in all product details correctly.")

    st.subheader("Current Inventory")
    if not filtered_inventory.empty:
        # Create a copy for editing to avoid SettingWithCopyWarning
        edited_inventory_df = st.data_editor(
            filtered_inventory.copy(),
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "SKU": st.column_config.TextColumn("SKU", help="Unique identifier for the product.", required=True),
                "Product Name": st.column_config.TextColumn("Product Name", required=True),
                "Unit": st.column_config.TextColumn("Unit", required=True),
                "Category": st.column_config.TextColumn("Category", required=True),
                "Quantity": st.column_config.NumberColumn("Quantity", min_value=0, format="%d", required=True),
                "Unit Price (₦)": st.column_config.NumberColumn("Unit Price (₦)", min_value=0.0, format="%.2f", required=True),
                "Cost Price (₦)": st.column_config.NumberColumn("Cost Price (₦)", min_value=0.0, format="%.2f", required=True, help="Cost price of the product"), # Make cost price editable
                "Reorder Point": st.column_config.NumberColumn("Reorder Point", min_value=0, format="%d", required=True),
                "Expiry Date": st.column_config.DateColumn("Expiry Date", min_value=datetime.now().date()),
                "Last Updated": st.column_config.DatetimeColumn("Last Updated", format="YYYY-MM-DD HH:mm:ss", disabled=True),
                "Store": st.column_config.TextColumn("Store", disabled=True), # Store column should not be editable
            },
            key="inventory_data_editor"
        )

        if st.button("Save Inventory Changes", key="save_inventory_button"):
            # Validate edited data before saving
            valid_changes = True
            for index, row in edited_inventory_df.iterrows():
                # Check for empty strings in critical fields
                if not all([row['SKU'], row['Product Name'], row['Unit'], row['Category']]):
                    st.error(f"Row {index+1}: SKU, Product Name, Unit, and Category cannot be empty.")
                    valid_changes = False
                    break
                # Check for non-negative numbers
                if not all([row['Quantity'] >= 0, row['Unit Price (₦)'] >= 0, row['Cost Price (₦)'] >= 0, row['Reorder Point'] >= 0]):
                    st.error(f"Row {index+1}: Quantity, Unit Price, Cost Price, and Reorder Point must be non-negative.")
                    valid_changes = False
                    break
                # Check for valid date
                if not isinstance(row['Expiry Date'], (datetime, pd.Timestamp)) or pd.isna(row['Expiry Date']):
                    st.error(f"Row {index+1}: Expiry Date must be a valid date.")
                    valid_changes = False
                    break

            if valid_changes:
                # Update the original session state inventory, preserving other stores' data
                # Identify SKUs present in the current store's inventory before changes
                current_store_skus = st.session_state.inventory[st.session_state.inventory['Store'] == st.session_state.current_store]['SKU'].tolist()

                # Remove old data for the current store
                st.session_state.inventory = st.session_state.inventory[st.session_state.inventory['Store'] != st.session_state.current_store]
                
                # Add updated data, ensuring 'Last Updated' is current for modified rows
                # Only update 'Last Updated' for rows that were actually changed or are new
                # This simple approach updates all rows that pass through the data editor for the current store
                edited_inventory_df['Last Updated'] = datetime.now() # Update timestamp for all saved rows
                st.session_state.inventory = pd.concat([st.session_state.inventory, edited_inventory_df], ignore_index=True)
                
                st.success("Inventory updated successfully!")
                st.rerun()
            else:
                st.error("Please correct the errors in the inventory table before saving.")
    else:
        st.info("No products in inventory for this store. Add new products above.")


elif selected_page == "Point of Sale":
    st.markdown('<div class="section-header">🛒 Point of Sale</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"Products Available in {st.session_state.current_store}")
        if not filtered_inventory.empty:
            # Display products with current stock for selection
            products_for_sale = filtered_inventory[['SKU', 'Product Name', 'Quantity', 'Unit Price (₦)']].copy()
            products_for_sale.rename(columns={'Unit Price (₦)': 'Price (₦)'}, inplace=True)
            st.dataframe(products_for_sale, use_container_width=True, hide_index=True)

            st.write("---")
            st.subheader("Add Item to Cart")
            
            # Use unique keys for selectbox and number_input
            selected_product_name = st.selectbox(
                "Select Product",
                products_for_sale['Product Name'].tolist(),
                key="pos_product_select"
            )
            
            if selected_product_name:
                selected_product_data = filtered_inventory[filtered_inventory['Product Name'] == selected_product_name].iloc[0]
                available_quantity = selected_product_data['Quantity']
                unit_price = selected_product_data['Unit Price (₦)']

                st.info(f"Selected: **{selected_product_name}** | Available: **{available_quantity}** units | Unit Price: **₦{unit_price:.2f}**")
                
                quantity_to_add = st.number_input(
                    "Quantity to Add",
                    min_value=1,
                    max_value=int(available_quantity) if available_quantity > 0 else 0,
                    step=1,
                    key="pos_quantity_input"
                )

                if st.button("Add to Cart", key="add_to_cart_button"):
                    if quantity_to_add > 0:
                        # Check if product is already in cart to update quantity
                        found_in_cart = False
                        for item in st.session_state.cart:
                            if item['SKU'] == selected_product_data['SKU']:
                                if (item['Quantity'] + quantity_to_add) <= available_quantity:
                                    item['Quantity'] += quantity_to_add
                                    item['Subtotal'] = item['Quantity'] * item['Unit Price']
                                    st.success(f"Added {quantity_to_add} more of '{selected_product_name}' to cart.")
                                else:
                                    st.error(f"Cannot add {quantity_to_add} more. Only {available_quantity - item['Quantity']} available.")
                                found_in_cart = True
                                break
                        
                        if not found_in_cart:
                            if quantity_to_add <= available_quantity:
                                st.session_state.cart.append({
                                    'SKU': selected_product_data['SKU'],
                                    'Product Name': selected_product_name,
                                    'Quantity': quantity_to_add,
                                    'Unit': selected_product_data['Unit'], # Added unit to cart item
                                    'Unit Price': unit_price,
                                    'Cost Price': selected_product_data['Cost Price (₦)'], # Added cost price to cart item
                                    'Subtotal': quantity_to_add * unit_price
                                })
                                st.success(f"Added {quantity_to_add} of '{selected_product_name}' to cart.")
                            else:
                                st.error(f"Requested quantity ({quantity_to_add}) exceeds available stock ({available_quantity}).")
                    else:
                        st.warning("Please enter a quantity greater than 0.")
        else:
            st.info("No products in inventory for sale in this store.")

    with col2:
        st.subheader("Shopping Cart")
        if st.session_state.cart:
            cart_df = pd.DataFrame(st.session_state.cart)
            cart_display_df = cart_df[['Product Name', 'Quantity', 'Unit Price', 'Subtotal']].copy()
            cart_display_df.rename(columns={'Unit Price': 'Price (₦)', 'Subtotal': 'Subtotal (₦)'}, inplace=True)
            st.dataframe(cart_display_df, hide_index=True, use_container_width=True)

            cart_total = cart_df['Subtotal'].sum()
            st.markdown(f"### Cart Total: ₦{cart_total:.2f}")

            st.write("---")
            if st.button("Complete Sale", key="complete_sale_button"):
                if st.session_state.cart:
                    transaction_successful = True
                    total_revenue_from_sale = 0
                    total_cogs_from_sale = 0
                    
                    # Process each item in the cart
                    for item in st.session_state.cart:
                        sku = item['SKU']
                        qty = item['Quantity']
                        unit_price_sold = item['Unit Price']
                        cost_price_of_item = item['Cost Price'] # Use the cost price recorded at time of adding to cart

                        if not update_stock(sku, qty, "Sale", st.session_state.current_store, unit_price_sold, cost_price_of_item):
                            transaction_successful = False
                            st.error(f"Failed to process sale for {item['Product Name']}. Sale aborted.")
                            break # Stop processing if any item fails
                        else:
                            total_revenue_from_sale += (qty * unit_price_sold)
                            total_cogs_from_sale += (qty * cost_price_of_item)

                    if transaction_successful:
                        # Generate and display receipt
                        receipt = generate_receipt(st.session_state.cart, total_revenue_from_sale)
                        st.session_state.last_receipt = receipt # Store for potential printing
                        st.session_state.receipt_history.append(receipt) # Add to history
                        
                        st.success("Sale completed and recorded!")
                        st.markdown("### Customer Receipt:")
                        st.markdown(receipt, unsafe_allow_html=True)
                        
                        # Clear cart after successful sale
                        st.session_state.cart = []
                        st.rerun() # Rerun to clear cart display
                else:
                    st.warning("Cart is empty. Add products before completing a sale.")

            # Clear Cart Button
            if st.button("Clear Cart", key="clear_cart_button"):
                st.session_state.cart = []
                st.success("Shopping cart cleared.")
                st.rerun() # Rerun to update the displayed cart

            # Print Receipt Button
            if st.session_state.last_receipt and st.button("Print Last Receipt", key="print_receipt_button"):
                # Inject JavaScript to trigger print dialog for the receipt div
                st.components.v1.html(
                    """
                    <script>
                        function printReceipt() {
                            var printContents = document.querySelector('.receipt-container').outerHTML;
                            var originalContents = document.body.innerHTML;
                            document.body.innerHTML = printContents;
                            window.print();
                            document.body.innerHTML = originalContents;
                            window.location.reload(); // Reload to restore Streamlit app
                        }
                        printReceipt();
                    </script>
                    """,
                    height=0,
                    width=0
                )
                st.info("Please use your browser's print dialog to print the receipt.")
                
        else:
            st.info("Shopping cart is empty.")
            st.session_state.last_receipt = "" # Ensure no old receipt is displayed if cart is empty


elif selected_page == "Record Transactions":
    st.markdown('<div class="section-header">📊 Record Transactions</div>', unsafe_allow_html=True)
    st.subheader("Manual Stock Update / Transaction Record")

    with st.form("transaction_form"):
        product_options = filtered_inventory['Product Name'].tolist()
        selected_product = st.selectbox("Select Product", product_options, key="manual_transaction_product")
        
        if selected_product:
            product_sku = filtered_inventory[filtered_inventory['Product Name'] == selected_product]['SKU'].iloc[0]
            current_qty = filtered_inventory[filtered_inventory['Product Name'] == selected_product]['Quantity'].iloc[0]
            current_selling_price = filtered_inventory[filtered_inventory['Product Name'] == selected_product]['Unit Price (₦)'].iloc[0]
            current_cost_price = filtered_inventory[filtered_inventory['Product Name'] == selected_product]['Cost Price (₦)'].iloc[0]

            st.info(f"Current Stock: {current_qty} for '{selected_product}'")

            transaction_type = st.radio("Transaction Type", ["Sale", "Purchase (Stock In)", "Adjustment (Out)", "Adjustment (In)"], key="transaction_type_radio")
            
            quantity_change = st.number_input("Quantity Change", min_value=0, step=1, key="quantity_change_input")
            
            selling_price_input = 0.0
            purchase_cost_price_input = 0.0

            if transaction_type == "Sale":
                selling_price_input = st.number_input(f"Selling Price per Unit (₦) (Current: ₦{current_selling_price:.2f})", min_value=0.0, value=current_selling_price, format="%.2f", key="sale_price_input")
            elif transaction_type == "Purchase (Stock In)":
                purchase_cost_price_input = st.number_input(f"New Cost Price per Unit (₦) (Current: ₦{current_cost_price:.2f})", min_value=0.0, value=current_cost_price, format="%.2f", help="Enter the new cost price for this purchase. This will update the inventory's cost price for this product.", key="purchase_cost_input")
            
            notes = st.text_area("Notes (Optional)", key="transaction_notes")

            submit_transaction = st.form_submit_button("Record Transaction")

            if submit_transaction:
                if quantity_change > 0:
                    if transaction_type == "Sale" or transaction_type == "Adjustment (Out)":
                        if update_stock(product_sku, quantity_change, transaction_type, st.session_state.current_store, selling_price=selling_price_input):
                            st.success(f"Recorded {transaction_type} of {quantity_change} units for '{selected_product}'.")
                            st.rerun()
                    elif transaction_type == "Purchase (Stock In)" or transaction_type == "Adjustment (In)":
                        if update_stock(product_sku, quantity_change, transaction_type, st.session_state.current_store, purchase_cost_price=purchase_cost_price_input):
                            st.success(f"Recorded {transaction_type} of {quantity_change} units for '{selected_product}'.")
                            st.rerun()
                else:
                    st.error("Quantity change must be greater than zero.")
        else:
            st.info("Please add products to the inventory first to record transactions.")

    st.subheader("Transaction History for Current Store")
    if not filtered_transactions.empty:
        # Display relevant columns for transaction history
        st.dataframe(filtered_transactions[[
            'Timestamp', 'Product Name', 'Quantity Change', 'Type', 'Selling Price (₦)', 
            'Cost Price (₦)', 'Revenue (₦)', 'Cost of Goods Sold (₦)', 'Profit/Loss (₦)', 
            'Cost of Goods Bought (₦)', 'New Quantity'
        ]].sort_values(by='Timestamp', ascending=False), use_container_width=True)
        
        # Download transaction history
        st.download_button(
            label="Download Transaction History (Excel)",
            data=to_excel(filtered_transactions),
            file_name=f"transactions_{st.session_state.current_store}_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No transactions recorded for this store yet.")


elif selected_page == "Operating Expenses":
    st.markdown('<div class="section-header">💸 Operating Expenses</div>', unsafe_allow_html=True)
    st.subheader("Add New Operating Expense")

    with st.form("add_expense_form"):
        expense_date = st.date_input("Date", datetime.now().date())
        expense_category = st.selectbox("Category", ["Rent", "Salaries", "Utilities", "Marketing", "Maintenance", "Others"])
        expense_description = st.text_area("Description", max_chars=200)
        expense_amount = st.number_input("Amount (₦)", min_value=0.0, format="%.2f")

        add_expense_submitted = st.form_submit_button("Add Expense")

        if add_expense_submitted:
            if expense_amount > 0 and expense_description:
                new_expense = pd.DataFrame([{
                    "Date": expense_date,
                    "Category": expense_category,
                    "Description": expense_description,
                    "Amount (₦)": expense_amount,
                    "Store": st.session_state.current_store
                }])
                st.session_state.operating_expenses = pd.concat([st.session_state.operating_expenses, new_expense], ignore_index=True)
                st.success(f"Added expense '{expense_description}' of ₦{expense_amount:.2f}.")
                st.rerun()
            else:
                st.error("Please provide a description and a valid amount for the expense.")
    
    st.subheader("Operating Expenses for Current Store")
    if not filtered_expenses.empty:
        st.dataframe(filtered_expenses.sort_values(by='Date', ascending=False), use_container_width=True)

        total_expenses = filtered_expenses['Amount (₦)'].sum()
        st.markdown(f"**Total Operating Expenses for {st.session_state.current_store}: ₦{total_expenses:,.2f}**")

        st.download_button(
            label="Download Operating Expenses (Excel)",
            data=to_excel(filtered_expenses),
            file_name=f"operating_expenses_{st.session_state.current_store}_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No operating expenses recorded for this store yet.")


elif selected_page == "Expiry Alerts":
    st.markdown('<div class="section-header">🗓️ Expiry Alerts</div>', unsafe_allow_html=True)

    today = datetime.now().date()
    
    # Existing expiring_soon_items and expired_items logic is reused from dashboard section
    # Re-calculate to ensure it's fresh for this page if needed, or assume filtered_inventory is up-to-date.
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
        expiring_soon_items = expiring_soon_items.sort_values(by="Expiry Date")

    expired_items = filtered_inventory[filtered_inventory['Expiry Date'] < today].sort_values(by="Expiry Date")


    st.subheader("Expired Products")
    if not expired_items.empty:
        st.error("The following products have **EXPIRED**:")
        st.dataframe(expired_items[['Product Name', 'SKU', 'Quantity', 'Expiry Date', 'Store']], use_container_width=True)
    else:
        st.info("No products have expired.")

    st.subheader(f"Products Expiring Soon (within {DEFAULT_EXPIRY_ALERT_DAYS} days)")
    if not expiring_soon_items.empty:
        st.warning("The following products are **Nearing Expiry Date**:")
        st.dataframe(expiring_soon_items[['Product Name', 'SKU', 'Quantity', 'Expiry Date', 'Store']], use_container_width=True)
    else:
        st.info("No products are expiring soon.")


elif selected_page == "Low Stock Alerts":
    st.markdown('<div class="section-header">⚠️ Low Stock Alerts</div>', unsafe_allow_html=True)
    
    # Existing low_stock_items and critical_stock_items logic is reused from dashboard section
    low_stock_items = filtered_inventory[filtered_inventory['Quantity'] <= filtered_inventory['Reorder Point']]
    critical_stock_items = filtered_inventory[filtered_inventory['Quantity'] <= CRITICAL_STOCK_THRESHOLD]

    st.subheader("Critical Stock Items")
    if not critical_stock_items.empty:
        st.markdown('<div class="low-stock-alert">', unsafe_allow_html=True)
        st.markdown(f"**CRITICAL STOCK ALERT!** The following products have **{CRITICAL_STOCK_THRESHOLD}** or fewer units left:", unsafe_allow_html=True)
        st.dataframe(critical_stock_items[['Product Name', 'SKU', 'Quantity', 'Reorder Point', 'Store']], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No products are at critical stock levels.")

    st.subheader("Low Stock Items (Below Reorder Point)")
    # Filter out items already identified as critical stock to avoid duplication
    low_stock_only_items = low_stock_items[~low_stock_items['SKU'].isin(critical_stock_items['SKU'])]
    if not low_stock_only_items.empty:
        st.warning("The following products are at **Low Stock** and need reordering:")
        st.dataframe(low_stock_only_items[['Product Name', 'SKU', 'Quantity', 'Reorder Point', 'Store']], use_container_width=True)
    else:
        st.info("No products are currently at low stock levels (excluding critical stock).")

elif selected_page == "Analytics & Reports":
    st.markdown('<div class="section-header">📈 Analytics & Reports</div>', unsafe_allow_html=True)

    st.subheader(f"Reports for {st.session_state.current_store}")

    # Calculate metrics for the current store
    total_revenue = filtered_transactions[filtered_transactions['Type'] == 'Sale']['Revenue (₦)'].sum()
    total_cogs = filtered_transactions[filtered_transactions['Type'] == 'Sale']['Cost of Goods Sold (₦)'].sum()
    gross_profit = total_revenue - total_cogs
    total_expenses = filtered_expenses['Amount (₦)'].sum()
    net_profit = gross_profit - total_expenses

    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.markdown(f"""
        <div class="report-card blue">
            <div class="value">₦{total_revenue:,.2f}</div>
            <div class="label">Total Sales Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    with col_r2:
        st.markdown(f"""
        <div class="report-card red">
            <div class="value">₦{total_cogs:,.2f}</div>
            <div class="label">Total Cost of Sales</div>
        </div>
        """, unsafe_allow_html=True)
    with col_r3:
        st.markdown(f"""
        <div class="report-card {'green' if gross_profit >= 0 else 'red'}">
            <div class="value">₦{gross_profit:,.2f}</div>
            <div class="label">Gross Profit</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.subheader(f"Overall Profit/Loss for {st.session_state.current_store}")
    col_nl1, col_nl2 = st.columns(2)
    with col_nl1:
        st.markdown(f"""
        <div class="report-card red">
            <div class="value">₦{total_expenses:,.2f}</div>
            <div class="label">Total Operating Expenses</div>
        </div>
        """, unsafe_allow_html=True)
    with col_nl2:
        st.markdown(f"""
        <div class="report-card {'green' if net_profit >= 0 else 'red'}">
            <div class="value">₦{net_profit:,.2f}</div>
            <div class="label">Net Profit/Loss</div>
        </div>
        """, unsafe_allow_html=True)


    st.markdown("---")
    st.subheader("Group Report (All Stores Consolidated)")
    
    # Calculate consolidated metrics
    all_sales_transactions = st.session_state.transactions[st.session_state.transactions['Type'] == 'Sale']
    group_total_revenue = all_sales_transactions['Revenue (₦)'].sum()
    group_total_cogs = all_sales_transactions['Cost of Goods Sold (₦)'].sum()
    group_gross_profit = group_total_revenue - group_total_cogs
    group_total_expenses = st.session_state.operating_expenses['Amount (₦)'].sum()
    group_net_profit = group_gross_profit - group_total_expenses

    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    with col_g1:
        st.markdown(f"""
        <div class="report-card blue">
            <div class="value">₦{group_total_revenue:,.2f}</div>
            <div class="label">Group Sales Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    with col_g2:
        st.markdown(f"""
        <div class="report-card red">
            <div class="value">₦{group_total_cogs:,.2f}</div>
            <div class="label">Group Cost of Sales</div>
        </div>
        """, unsafe_allow_html=True)
    with col_g3:
        st.markdown(f"""
        <div class="report-card {'green' if group_gross_profit >= 0 else 'red'}">
            <div class="value">₦{group_gross_profit:,.2f}</div>
            <div class="label">Group Gross Profit</div>
        </div>
        """, unsafe_allow_html=True)
    with col_g4:
        st.markdown(f"""
        <div class="report-card {'green' if group_net_profit >= 0 else 'red'}">
            <div class="value">₦{group_net_profit:,.2f}</div>
            <div class="label">Group Net Profit/Loss</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Export Reports")

    col_export1, col_export2, col_export3 = st.columns(3)

    with col_export1:
        st.download_button(
            label="Download Inventory (Excel)",
            data=to_excel(st.session_state.inventory),
            file_name=f"full_inventory_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_inventory"
        )
    with col_export2:
        st.download_button(
            label="Download All Transactions (Excel)",
            data=to_excel(st.session_state.transactions),
            file_name=f"all_transactions_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_all_transactions"
        )
    with col_export3:
        st.download_button(
            label="Download All Expenses (Excel)",
            data=to_excel(st.session_state.operating_expenses),
            file_name=f"all_expenses_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_all_expenses"
        )

    st.subheader("Receipt History")
    if st.session_state.receipt_history:
        # Display the last few receipts or provide a way to select
        selected_receipt_index = st.selectbox("Select Receipt to View:", 
                                            options=range(len(st.session_state.receipt_history)),
                                            format_func=lambda x: f"Receipt {x+1} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", # Placeholder for dynamic date
                                            index=len(st.session_state.receipt_history) - 1, # Default to latest
                                            key="receipt_history_selector")
        st.markdown(st.session_state.receipt_history[selected_receipt_index], unsafe_allow_html=True)
    else:
        st.info("No receipts have been generated yet.")


elif selected_page == "About":
    st.markdown('<div class="section-header">ℹ️ About</div>', unsafe_allow_html=True)
    st.write("""
    This **Grocery Inventory Management** application is designed to help businesses
    efficiently manage their product stock, track sales and purchases, monitor operating
    expenses, and generate insightful reports.

    **Key Features:**
    * **Multi-Store Support:** Manage inventory and transactions for multiple store locations.
    * **Product Management:** Add, view, edit, and delete product details including SKU,
        name, category, quantity, unit, selling price, cost price, reorder point, and expiry date.
    * **Transaction Logging:** Record all sales and stock deliveries (purchases),
        including updating cost prices for purchases, specific to the selected store.
    * **Operating Expenses:** A new section to track and report daily operational expenses
        like rent, salaries, utilities, etc., specific to the selected store.
    * **Expiry Alerts:** Identifies products that have expired or are nearing their
        expiry date, with customizable alert periods per product, specific to the selected store.
    * **Low Stock Alerts:** Identifies products needing reordering, categorized by urgency
        (Low and Critical Stock), specific to the selected store.
    * **Analytics & Reports:** Generate comprehensive reports on sales, cost of goods bought,
        and profit/loss, including:
        * Individual store reports (Sales, Cost of Goods Bought, Cost of Sales/Profit for current store).
        * An **Overall Profit/Loss Report** for the currently selected store.
        * A **Group Report** consolidating Sales, Cost of Sales, Gross Profit, and Net Profit
            across **all** stores.
    * With the ability to download data in Excel format for all reports.

    **Note:** This application uses Streamlit's `st.session_state` for data persistence, meaning data
    will reset if the browser tab is closed or the Streamlit server restarts. For real-world
    use, a robust database integration (e.g., Firestore, PostgreSQL) would be required to ensure
    data is permanently saved.
    """)
    st.write("Developed with ❤️ using Streamlit.")
