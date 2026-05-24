import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Configure the structural layout of our web viewport interface
st.set_page_config(page_title="PropInsight™ Analytics", page_icon="🏢", layout="wide")

# =====================================================================
# 🎨 BRANDING THEME SKIN INJECTION (#002244 & #FFFFFF)
# =====================================================================
st.markdown("""
    <style>
    /* FORCE THE MAIN BACKGROUND AND TEXT TO MATCH THE DARK THEME */
    .main, .block-container {
        background-color: #0b0f19 !important; /* Elegant slate dark background */
    }
    h1, h2, h3, h4, h5, h6, .main p, .main span, .main div {
        color: #ffffff !important; /* Forces all main screen layout headers to Pure White */
    }
    
    /* SIDEBAR MASTER COLOR ENGINE LAYOUT OVERRIDES */
    section[data-testid="stSidebar"] {
        background-color: #002244 !important; /* Premium Dark Blue Panel */
        border-right: 2px solid #ffffff !important; /* Pure White Divider Line */
    }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #ffffff !important; 
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] label p,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #ffffff !important; 
        font-weight: 800 !important;
        font-size: 1.05rem !important;
    }

    /* CONTAINER FRAMES FOR METRICS */
    div[data-testid="stMetric"], 
    div[data-testid="stMetricSimpleBox"] {
        background-color: #002244 !important; 
        border: 2px solid #ffffff !important; 
        padding: 15px 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* LABELS & VALUE TEXT FORCED TO PURE HIGH-CONTRAST WHITE */
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetricSimpleBox"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] label,
    div[data-testid="stMetricSimpleBox"] label {
        color: #ffffff !important; 
        opacity: 1 !important; 
        font-size: 1.05rem !important; 
        font-weight: 700 !important;
        -webkit-text-fill-color: #ffffff !important;
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
    
    /* CUSTOM BLOCK FOR EMI HIGHLIGHT RADIAL CALLOUTS */
    .emi-container {
        background-color: #002244 !important;
        border: 2px dashed #ffffff !important;
        padding: 20px;
        border-radius: 10px;
        margin-top: 15px;
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

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT locality FROM listings")
localities_list = [row[0] for row in cursor.fetchall()]
conn.close()

# =====================================================================
# INTERACTIVE SIDEBAR CONTROL PANEL
# =====================================================================
with st.sidebar:
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
    
    selected_locality = st.selectbox("Select Neighborhood Cluster", ["All Locations"] + localities_list)
    selected_bhk = st.slider("Minimum Layout Requirements (BHK)", min_value=1, max_value=4, value=1)
    max_budget = st.slider("Maximum Budget Allocation (INR)", min_value=3000000, max_value=20000000, value=20000000, step=500000)

# =====================================================================
# 📈 MAIN VIEWPORT PROCESSING LAYER
# =====================================================================
st.title("🏢 PropInsight™: Real Estate Valuation & Search Portal")
st.markdown("---")

query = "SELECT *, (price / square_feet) AS cost_per_sqft FROM listings WHERE price <= ? AND bedrooms >= ?"
params = [max_budget, selected_bhk]
if selected_locality != "All Locations":
    query += " AND locality = ?"
    params.append(selected_locality)
    
conn = get_db_connection()
df_properties = pd.read_sql_query(query, conn, params=params)
df_baselines = pd.read_sql_query("SELECT locality, AVG(price / square_feet) as baseline_avg FROM listings GROUP BY locality", conn)
conn.close()

st.markdown("### 📊 Dynamic Location Valuation Matrix")

if df_properties.empty:
    st.warning("⚠️ No properties found matching your criteria. Adjust your touchpad filters in the sidebar!")
else:
    avg_market_price = df_properties['price'].mean()
    avg_sqft_cost = df_properties['cost_per_sqft'].mean()
    total_options = len(df_properties)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Available Market Matches", f"{total_options} Properties")
    col2.metric("Average Neighborhood Valuation", f"₹{avg_market_price:,.0f}")
    col3.metric("Avg Rate Per Square Foot", f"₹{avg_sqft_cost:.0f}/sqft")
    
    # HTML5 Conversational Speech Core Link
    speech_text = f"Analysis complete. Found {total_options} property matches. The average valuation is {int(avg_market_price)} Rupees."
    tts_html = f"""
        <script>
        function speakSummary() {{
            var msg = new SpeechSynthesisUtterance("{speech_text}");
            window.speechSynthesis.speak(msg);
        }}
        </script>
        <button onclick="speakSummary()" style="background-color: #002244; color: white; border: 2px solid white; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 1rem; margin-top: 15px;">
            🔊 Listen to Analytics Audio Summary
        </button>
    """
    st.components.v1.html(tts_html, height=60)
    
    st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
    
    # Market Trends Chart Section
    st.markdown("### 📈 Market Trends & Valuation Distribution")
    fig = px.scatter(
        df_properties,
        x="square_feet",
        y="price",
        color="locality",
        size="cost_per_sqft",
        hover_name="title",
        labels={"square_feet": "Property Size (Sqft)", "price": "Market Price (INR)", "locality": "Neighborhood"},
        template="plotly_dark"
    )
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
    st.markdown("#### 🏢 Filtered Property Inventory Listings Catalog")
    
    df_merged = pd.merge(df_properties, df_baselines, on='locality', how='left')
    
    def calculate_deal_status(row):
        if row['cost_per_sqft'] < row['baseline_avg']:
            return "🔥 BARGAIN ASSET"
        return "Standard Market Value"
        
    df_merged['Market Status'] = df_merged.apply(calculate_deal_status, axis=1)
    display_cols = ['title', 'locality', 'bedrooms', 'price', 'square_feet', 'cost_per_sqft', 'Market Status']
    
    st.dataframe(
        df_merged[display_cols].style.format({'price': '₹{:,.0f}', 'cost_per_sqft': '₹{:.0f}/sqft'}), 
        use_container_width=True
    )
    
    st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
    
    # 🌟 BONUS FEATURE LAYER: ON-THE-FLY LOAN & EMI ESTIMATOR ENGINE
    st.markdown("### 🧮 On-the-Fly Mortgage Loan & EMI Estimator")
    
    # Dropdown selector containing your live dynamic listings records
    selected_property_title = st.selectbox("Isolate an Asset Row for Financial Estimation Analysis", df_merged['title'].unique())
    
    # Extract asset records based on selected dropdown title
    property_row = df_merged[df_merged['title'] == selected_property_title].iloc[0]
    property_price = property_row['price']
    
    calc_col1, calc_col2 = st.columns(2)
    with calc_col1:
        down_payment_pct = st.slider("Down Payment Allocation Percentage (%)", min_value=10, max_value=50, value=20, step=5)
        loan_tenure_years = st.slider("Loan Repayment Tenure Duration (Years)", min_value=5, max_value=30, value=20, step=5)
        interest_rate = st.slider("Annual Bank Interest Lending Rate (%)", min_value=5.0, max_value=15.0, value=8.5, step=0.1)
        
    with calc_col2:
        # Core mathematical transformations
        down_payment_amount = property_price * (down_payment_pct / 100)
        principal_loan_amount = property_price - down_payment_amount
        
        # Monthly interest formula primitives math modeling
        monthly_rate = (interest_rate / 12) / 100
        total_months = loan_tenure_years * 12
        
        # Guard clause handling standard mathematical evaluation
        if monthly_rate > 0:
            monthly_emi = principal_loan_amount * (monthly_rate * (1 + monthly_rate)**total_months) / ((1 + monthly_rate)**total_months - 1)
        else:
            monthly_emi = principal_loan_amount / total_months
            
        # Draw formatted data analytics calculations metrics callout box onto screen layout
        st.markdown(f"""
            <div class="emi-container">
                <h4 style="margin-top:0;">📋 Financial Assessment Summary:</h4>
                <p>💸 <b>Isolated Asset Price:</b> ₹{property_price:,.0f}</p>
                <p>🧱 <b>Upfront Down Payment Plan ({down_payment_pct}%):</b> ₹{down_payment_amount:,.0f}</p>
                <p>🛡️ <b>Principal Bank Financing Total:</b> ₹{principal_loan_amount:,.0f}</p>
                <hr style="border:0; height:1px; background-color:white; margin:10px 0;">
                <h3 style="color:#00f2fe !important; margin-bottom:0;">📉 Estimated Installment: ₹{monthly_emi:,.0f} / Month</h3>
            </div>
        """, unsafe_allow_html=True)
        