import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Configure the structural layout of our web viewport interface
st.set_page_config(page_title="PropInsight™ Analytics", page_icon="🏢", layout="wide")

# =====================================================================
# 🎨 STEP-BY-STEP CUSTOM BRANDING THEME SKIN INJECTION (#002244 & #FFFFFF)
# =====================================================================
st.markdown("""
    <style>
    /* 1. FORCE THE MAIN BACKGROUND AND TEXT TO MATCH THE DARK THEME */
    .main, .block-container {
        background-color: #0b0f19 !important; /* Elegant slate dark background */
    }
    h1, h2, h3, h4, h5, h6, .main p, .main span, .main div {
        color: #ffffff !important; /* Forces all main screen layout headers to Pure White */
    }
    
    /* 2. FIXED: ADDED MISSING HASH SYMBOL (#) AND STRIPPED LIGHT-MODE BLUR */
    section[data-testid="stSidebar"] {
        background-color: #002244 !important; /* Locks left panel to Premium Dark Blue */
        border-right: 2px solid #ffffff !important; /* Pure White Divider Line */
    }
    
    /* 3. FORCES ALL SIDEBAR BRANDING & DESCRIPTION TEXT TO PURE WHITE */
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #ffffff !important; 
        font-weight: 700 !important;
    }

    /* 4. SHARP HIGH-CONTRAST SLIDER & DROPDOWN WHITE LABELS FOR VISIBILITY */
    section[data-testid="stSidebar"] label p,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #ffffff !important; 
        font-weight: 800 !important;
        font-size: 1.05rem !important;
    }

    /* 5. FORCE MAIN PAGE METRIC SUMMARIES TO SECTOR DARK BLUE BOXES */
    div[data-testid="stMetric"], 
    div[data-testid="stMetricSimpleBox"] {
        background-color: #002244 !important; 
        border: 2px solid #ffffff !important; 
        padding: 15px 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
  /* FIXED: TARGEETS RAW INTERNAL LABEL CLASSES AND FORCES MAXIMUM OPACITY */
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetricSimpleBox"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] label,
    div[data-testid="stMetricSimpleBox"] label {
        color: #ffffff !important; /* Pure high-contrast solid white */
        opacity: 1 !important; /* Disables any light-theme dimming overrides */
        font-size: 1.05rem !important; 
        font-weight: 700 !important;
        -webkit-text-fill-color: #ffffff !important; /* Extra browser insurance */
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetricSimpleBox"] [data-testid="stMetricValue"] {
        color: #ffffff !important; 
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }
    
    .custom-hr {
        border: 0;
        height: 2px;
        background-image: linear-gradient(to right, #ffffff, #002244, transparent);
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# RELATIONAL DATABASE ARCHITECTURE SEED 
# =====================================================================
def get_db_connection():
    return sqlite3.connect('property_directory.db')

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            property_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, locality TEXT, bedrooms INTEGER, price REAL, square_feet INTEGER
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM listings")
    if cursor.fetchone()[0] == 0:
        default_listings = [
            ('Premium 2BHK Apartment', 'Koregaon Park', 2, 7500000, 1100),
            ('Luxury 3BHK Residency', 'Koregaon Park', 3, 12000000, 1600),
            ('Cozy 1BHK Flat', 'Kothrud', 1, 4500000, 600),
            ('Spacious 3BHK Apartment', 'Kothrud', 3, 9500000, 1450),
            ('Modern 2BHK Smart Home', 'Baner', 2, 6800000, 1050),
            ('Elite Penthouse Suite', 'Baner', 4, 18000000, 2400),
            ('Budget Studio Apartment', 'Wagholi', 1, 3200000, 450),
            ('Urban 2BHK Residency', 'Wagholi', 2, 5100000, 950),
            ('Investor Liquidation 2BHK', 'Baner', 2, 5200000, 1100)
        ]
        cursor.executemany("INSERT INTO listings (title, locality, bedrooms, price, square_feet) VALUES (?, ?, ?, ?, ?)", default_listings)
    conn.commit()
    conn.close()

init_db()

# Fetch dynamic localities list from database for our filter component
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT locality FROM listings")
localities_list = [row[0] for row in cursor.fetchall()]
conn.close()

# =====================================================================
# 📊 INTEGRATED SIDEBAR COMPONENT: LOGO + THE 3 RESTORED FEATURES
# =====================================================================
with st.sidebar:
    # RESTORED FEATURE: Premium Branding SVG Logo Vector Container
    st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <svg width="75" height="75" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 21H21" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
                <path d="M5 21V10L12 5L19 10V21" stroke="#ffffff" stroke-width="2" stroke-linejoin="round"/>
                <path d="M9 21V14H15V21" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
                <path d="M12 9V11" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"/>
                <line x1="12" y1="14" x2="12.01" y2="14" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <h2 style="margin-top: 10px; margin-bottom: 0; font-size: 1.5rem;">PropInsight™</h2>
            <p style="font-size: 0.8rem; letter-spacing: 1px; text-transform: uppercase; margin-top: 2px; opacity: 0.8;">Analytics Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
    st.markdown("### 🔍 Touchpad Filters")
    
    # 1. RESTORED FEATURE: Select Neighborhood Dropdown Menu Selector
    selected_locality = st.selectbox("Select Neighborhood Cluster", ["All Locations"] + localities_list)
        
    # 2. RESTORED FEATURE: Minimum Bedrooms Requirement Slider Layout
    selected_bhk = st.slider("Minimum Layout Requirements (BHK)", min_value=1, max_value=4, value=1)
        
    # 3. RESTORED FEATURE: Maximum Budget Allocation Threshold Slider
    max_budget = st.slider("Maximum Budget Allocation (INR)", min_value=3000000, max_value=20000000, value=20000000, step=500000)

# =====================================================================
# 📈 MAIN SCREEN SEARCH ENGINE APPLICATION PIPELINE LAYER
# =====================================================================
st.title("🏢 PropInsight™: Real Estate Valuation & Search Portal")
st.markdown("---")

# Build dynamic parameters relational query pipeline matching our 3 features
query = "SELECT *, (price / square_feet) AS cost_per_sqft FROM listings WHERE price <= ? AND bedrooms >= ?"
params = [max_budget, selected_bhk]
if selected_locality != "All Locations":
    query += " AND locality = ?"
    params.append(selected_locality)
    
conn = get_db_connection()
df_properties = pd.read_sql_query(query, conn, params=params)
conn.close()

st.markdown("### 📊 Dynamic Location Valuation Matrix")

if df_properties.empty:
    st.warning("No properties found matching your criteria. Adjust your touchpad filters in the sidebar!")
else:
    # Mathematical data transformations
    avg_market_price = df_properties['price'].mean()
    avg_sqft_cost = df_properties['cost_per_sqft'].mean()
    total_options = len(df_properties)
    
    # Render our 3 Custom Dark Blue Cards with White Text
    col1, col2, col3 = st.columns(3)
    col1.metric("Available Market Matches", f"{total_options} Properties")
    col2.metric("Average Neighborhood Valuation", f"₹{avg_market_price:,.0f}")
    col3.metric("Avg Rate Per Square Foot", f"₹{avg_sqft_cost:.0f}/sqft")
    
    st.markdown("---")
    st.markdown("#### 🏢 Filtered Property Inventory Listings Catalog")
    # Clean data frame display table
    st.dataframe(df_properties[['title', 'locality', 'bedrooms', 'price', 'square_feet', 'cost_per_sqft']], use_container_width=True)
