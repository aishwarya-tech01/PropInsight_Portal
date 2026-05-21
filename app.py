import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# Set up a wide page layout with a premium corporate title icon
st.set_page_config(page_title="PropInsight™ Analytics", page_icon="🏢", layout="wide")

# --- NATIVE UI ACCESSIBILITY ENGINE (SPEECH BROWSER TIER) ---
def speak_real_estate_action(text_message):
    """Uses native browser speech synthesis to announce property filter shifts instantly."""
    components.html(f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.webkitSpeechSynthesis?.cancel() || window.speechSynthesis.cancel(); 
                const textUtterance = new SpeechSynthesisUtterance("{text_message}");
                textUtterance.rate = 1.15; 
                window.speechSynthesis.speak(textUtterance);
            }}
        </script>
    """, height=0)

# --- PREMIUM CUSTOM CSS DESIGN STYLING INJECTION ---
st.markdown("""
    <style>
    /* Style the main title text */
    .main-title {
        color: #00f2fe;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        font-size: 2.3rem;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #718096;
        font-style: italic;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    
    /* 🎨 HIGH-CONTRAST SIDEBAR TEXT LABEL FIXES */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] label {
        color: #ffffff !important; /* Pure high-contrast solid white */
        font-weight: 700 !important; /* Bold font styling */
        font-size: 1.05rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }
    
    /* 🎨 HIGH-CONTRAST DASHBOARD CARD FIX */
    div[data-testid="stMetric"] {
        background-color: #0f172a !important; 
        border: 2px solid #334155 !important;
        padding: 20px 25px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
        transition: transform 0.2s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        border-color: #00f2fe !important;
    }
    
    /* 🏷️ Card Header Label Color Fix */
    div[data-testid="stMetric"] label [data-testid="stMetricLabel"] {
        color: #00f2fe !important; 
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }
    
    /* 🔢 Card Big Number Value Color Fix */
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important; 
        font-size: 2.2rem !important;
        font-weight: 700 !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    .custom-hr {
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, #00f2fe, #4facfe, transparent);
        margin: 20px 0;
    }
    .bargain-badge {
        background-color: #065f46;
        color: #34d399;
        font-weight: bold;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #059669;
        display: inline-block;
        font-size: 0.85rem;
    }
    .normal-badge {
        background-color: #1e293b;
        color: #94a3b8;
        font-weight: bold;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #334155;
        display: inline-block;
        font-size: 0.85rem;
    }
    .emi-box {
        background-color: #0f172a;
        border: 1px dashed #4facfe;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SECURE RELATIONAL DATABASE INITIALIZATION ---
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
        cursor.exec_numany = cursor.executemany("INSERT INTO listings (title, locality, bedrooms, price, square_feet) VALUES (?, ?, ?, ?, ?)", default_listings)
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 📊 SIDEBAR COMPONENT: INTERACTIVE CONTROL PANEL + LOGO
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 15px 0 10px 0;">
            <svg width="70" height="70" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 21H21" stroke="#00f2fe" stroke-width="2" stroke-linecap="round"/>
                <path d="M5 21V10L12 5L19 10V21" stroke="#4facfe" stroke-width="2" stroke-linejoin="round"/>
                <path d="M9 21V14H15V21" stroke="#00f2fe" stroke-width="2" stroke-linecap="round"/>
                <path d="M12 9V11" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"/>
                <line x1="12" y1="14" x2="12.01" y2="14" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <h2 style="color: #ffffff; font-family: 'Segoe UI'; font-weight: 700; font-size: 1.4rem; margin-top: 10px; margin-bottom: 0;">PropInsight™</h2>
            <p style="color: #00f2fe; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; margin: 0; font-weight: 600;">Analytics Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
    st.markdown("### 🔍 Touchpad Filters")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT locality FROM listings")
    localities = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if st.button("🔊 Initialize Voice Assist Mode", type="primary", use_container_width=True):
        speak_real_estate_action("Voice feedback engine successfully activated.")
    
    st.write("")
    
    selected_locality = st.selectbox("Select Neighborhood Cluster", ["All Locations"] + localities)
    if st.session_state.get("prev_loc", "All Locations") != selected_locality:
        st.session_state["prev_loc"] = selected_locality
        speak_real_estate_action(f"Filtering locations by {selected_locality}")
        st.rerun()
        
    selected_bhk = st.slider("Minimum Layout Requirements (BHK)", min_value=1, max_value=4, value=1)
    if st.session_state.get("prev_bhk", 1) != selected_bhk:
        st.session_state["prev_bhk"] = selected_bhk
        speak_real_estate_action(f"Minimum targets updated to {selected_bhk} bedrooms")
        st.rerun()
        
    max_budget = st.slider("Maximum Budget Allocation (INR)", min_value=3000000, max_value=20000000, value=20000000, step=500000)
    if st.session_state.get("prev_budget", 20000000) != max_budget:
        st.session_state["prev_budget"] = max_budget
        speak_real_estate_action("Budget threshold caps adjusted.")
        st.rerun()

# ==========================================
# 📈 MAIN SCREEN FRAMEWORK COMPONENT DISPLAY LAYER
# ==========================================
st.markdown('<div class="main-title">🏠 PropInsight™ Real Estate Search Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Enterprise Relational Search Portal Featuring Live Neighborhood Valuation Metrics & Analytical Vector Arrays</div>', unsafe_allow_html=True)

# Create interface views using Tabs
tab_search, tab_loan, tab_compare = st.tabs(["🔍 Live Property Catalog", "🏦 Dynamic Affordability Calculator", "📊 Municipal Sector Comparison"])

# FETCH DATA FOR PIPELINES
query = "SELECT *, (price / square_feet) AS cost_per_sqft FROM listings WHERE price <= ? AND bedrooms >= ?"
params = [max_budget, selected_bhk]
if selected_locality != "All Locations":
    query += " AND locality = ?"
    params.append(selected_locality)
    
conn = get_db_connection()
df_properties = pd.read_sql_query(query, conn, params=params)
df_all_market = pd.read_sql_query("SELECT locality, AVG(price / square_feet) as neighborhood_avg_sqft, AVG(price) as avg_price FROM listings GROUP BY locality", conn)
conn.close()

# ==========================================
# VIEW TAB 1: SEARCH & BARGAIN BADGES
# ==========================================
with tab_search:
    st.markdown("#### 📊 Dynamic Location Valuation Matrix")
    
    if df_properties.empty:
        st.warning("No listings match your targeted inputs.")
    else:
        avg_market_price = df_properties['price'].mean()
        avg_sqft_cost = df_properties['cost_per_sqft'].mean()
        total_options = len(df_properties)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Available Market Matches", f"{total_options} Properties")
        m2.metric("Average Neighborhood Valuation", f"₹{avg_market_price:,.0f}")
        m3.metric("Avg Rate Per Square Foot", f"₹{avg_sqft_cost:.0f}/sqft")
        
        st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
        st.markdown("#### 🏢 Smart Property Evaluation Catalog")
        
        df_evaluated = pd.merge(df_properties, df_all_market, on='locality', how='left')
        
        for index, row in df_evaluated.iterrows():
            col_desc, col_badge = st.columns([4, 1])
            with col_desc:
                st.markdown(f"**{row['title']}** — located in *{row['locality']}* ({row['bedrooms']} BHK)")
                st.write(f"📐 Size: {row['square_feet']} sqft | 💰 Evaluation: ₹{row['price']:,.0f} | Rate: ₹{row['cost_per_sqft']:.0f}/sqft")
            with col_badge:
                if row['cost_per_sqft'] < row['neighborhood_avg_sqft']:
                    savings_pct = ((row['neighborhood_avg_sqft'] - row['cost_per_sqft']) / row['neighborhood_avg_sqft']) * 100
                    st.markdown(f'<div class="bargain-badge">🔥 BARGAIN ({savings_pct:.0f}% Under Market)</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="normal-badge">⚖️ Standard Market Rate</div>', unsafe_allow_html=True)
            st.write("---")

# ==========================================
# VIEW TAB 2: THE BANKING LOAN MODULE
# ==========================================
with tab_loan:
    st.markdown("#### 🏦 Real Estate Mortgage Loan Simulation")
    
    if df_properties.empty:
        st.warning("No listings available to run financial simulations.")
    else:
        property_titles = df_properties['title'].tolist()
        selected_prop_title = st.selectbox("Select Target Property for Loan Analysis", property_titles)
        
        selected_row = df_properties[df_properties['title'] == selected_prop_title].iloc[0]
        property_base_price = selected_row['price']
        
        st.info(f" Selected Asset Valuation: **₹{property_base_price:,.0f} INR**")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            down_payment = st.slider("Down Payment Capital (INR)", min_value=0, max_value=int(property_base_price), value=int(property_base_price * 0.20), step=50000)
        with c2:
            interest_rate = st.slider("Bank Interest Rate (Annual %)", min_value=5.0, max_value=15.0, value=8.5, step=0.1)
        with c3:
            loan_tenure = st.slider("Loan Repayment Tenure (Years)", min_value=5, max_value=30, value=20, step=1)
            
        principal_loan_amount = property_base_price - down_payment
        
        if principal_loan_amount <= 0:
            st.success("🎉 Your down payment covers 100% of the asset cost! No banking loan or EMI schedules required.")
        else:
            monthly_interest = (interest_rate / 12) / 100
            total_months = loan_tenure * 12
            
            compounding_factor = (1 + monthly_interest) ** total_months
            calculated_monthly_emi = principal_loan_amount * (monthly_interest * compounding_factor) / (compounding_factor - 1)
            
            total_repayment = calculated_monthly_emi * total_months
            total_interest_paid = total_repayment - principal_loan_amount
            
            st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
            
            e1, e2, e3 = st.columns(3)
            e1.metric("Net Principal Loan Amount", f"₹{principal_loan_amount:,.0f}")
            e2.metric("Calculated Monthly EMI", f"₹{calculated_monthly_emi:,.0f} / month")
            e3.metric("Lifetime Bank Interest Cost", f"₹{total_interest_paid:,.0f}")

# ==========================================
# 📊 VIEW TAB 3: NEIGHBORHOOD COMPARISON DASHBOARD
# ==========================================
with tab_compare:
    st.markdown("#### ⚖️ Side-by-Side Municipal Sector Analytics")
    st.write("Compare localized data sets side-by-side to find the most value-optimized zones.")
    
    col_choice1, col_choice2 = st.columns(2)
    with col_choice1:
        loc1 = st.selectbox("Select First Neighborhood", localities, index=0)
    with col_choice2:
        loc2 = st.selectbox("Select Second Neighborhood", localities, index=1 if len(localities) > 1 else 0)
        
    # Filter dataset for only selected localities
    df_compare = df_all_market[df_all_market['locality'].isin([loc1, loc2])]
    
    if not df_compare.empty:
        # Render a side-by-side bar chart comparison using Plotly
        st.markdown("##### 📈 Rate Per Square Foot Comparison (INR)")
        fig_compare = px.bar(
            df_compare, 
            x="locality", 
            y="neighborhood_avg_sqft", 
            color="locality",
            text_auto='.0f',
            labels={"neighborhood_avg_sqft": "Avg Rate (₹/sqft)", "locality": "Zoning District"},
            template="plotly_dark"
        )
        fig_compare.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_compare, use_container_width=True)
        
        # Text analytics readout
        row1 = df_compare[df_compare['locality'] == loc1].iloc[0]
        row2 = df_compare[df_compare['locality'] == loc2].iloc[0]
        
        st.markdown(f"""
            <div class="emi-box">
                <p style="color: #00f2fe; margin: 0 0 10px 0; font-weight: bold; font-size: 1.05rem;">📋 Market Comparison Readout</p>
                <ul style="color: #ffffff; margin: 0; padding-left: 20px; font-size: 0.95rem; line-height: 1.6;">
                    <li><strong>{loc1}</strong> features an average rate of <span style="color: #00f2fe; font-weight: bold;">₹{row1['neighborhood_avg_sqft']:.0f}/sqft</span> with a baseline average cost of <span style="color: #00f2fe; font-weight: bold;">₹{row1['avg_price']:,.0f}</span>.</li>
                    <li><strong>{loc2}</strong> features an average rate of <span style="color: #00f2fe; font-weight: bold;">₹{row2['neighborhood_avg_sqft']:.0f}/sqft</span> with a baseline average cost of <span style="color: #00f2fe; font-weight: bold;">₹{row2['avg_price']:,.0f}</span>.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)