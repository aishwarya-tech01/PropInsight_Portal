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
        color: #a0aec0;
        font-style: italic;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    /* Design corporate metric display dashboard cards */
    div[data-testid="stMetric"] {
        background-color: #1e293b;
        border: 2px solid #334155;
        padding: 20px 25px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #00f2fe;
    }
    /* Style the sidebar panel view block */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    /* Custom divider design line */
    .custom-hr {
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, #00f2fe, #4facfe, transparent);
        margin: 20px 0;
    }
    /* 🟢 CUSTOM BARGAIN BADGE STYLING */
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
        # Seeding our Pune marketplace dataset
        default_listings = [
            ('Premium 2BHK Apartment', 'Koregaon Park', 2, 7500000, 1100),
            ('Luxury 3BHK Residency', 'Koregaon Park', 3, 12000000, 1600),
            ('Cozy 1BHK Flat', 'Kothrud', 1, 4500000, 600),
            ('Spacious 3BHK Apartment', 'Kothrud', 3, 9500000, 1450),
            ('Modern 2BHK Smart Home', 'Baner', 2, 6800000, 1050),
            ('Elite Penthouse Suite', 'Baner', 4, 18000000, 2400),
            ('Budget Studio Apartment', 'Wagholi', 1, 3200000, 450),
            ('Urban 2BHK Residency', 'Wagholi', 2, 5100000, 950),
            # Adding an underpriced bargain property to test our logic loops!
            ('Investor Liquidation 2BHK', 'Baner', 2, 5200000, 1100)
        ]
        cursor.executemany("INSERT INTO listings (title, locality, bedrooms, price, square_feet) VALUES (?, ?, ?, ?, ?)", default_listings)
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

# Build dynamic SQL query strings from filter slider data points
query = "SELECT *, (price / square_feet) AS cost_per_sqft FROM listings WHERE price <= ? AND bedrooms >= ?"
params = [max_budget, selected_bhk]

if selected_locality != "All Locations":
    query += " AND locality = ?"
    params.append(selected_locality)
    
conn = get_db_connection()
df_properties = pd.read_sql_query(query, conn, params=params)

# BACKEND MARKET AGGREGATE CALCULATION: Fetch overall neighborhood averages to locate bargains
df_all_market = pd.read_sql_query("SELECT locality, AVG(price / square_feet) as neighborhood_avg_sqft FROM listings GROUP BY locality", conn)
conn.close()

st.markdown("#### 📊 Dynamic Location Valuation Matrix")

if df_properties.empty:
    st.warning("No listings match your targeted inputs. Readjust your sidebar budget sliders to widen search scope.")
else:
    # Run analytical math primitives using Pandas
    avg_market_price = df_properties['price'].mean()
    avg_sqft_cost = df_properties['cost_per_sqft'].mean()
    total_options = len(df_properties)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Available Market Matches", f"{total_options} Properties")
    m2.metric("Average Neighborhood Valuation", f"₹{avg_market_price:,.0f}")
    m3.metric("Avg Rate Per Square Foot", f"₹{avg_sqft_cost:.0f}/sqft")
    
    st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
    
    # --- AUTOMATED BARGAIN VALUATION INTELLIGENCE GENERATOR ---
    st.markdown("#### 🏢 Smart Property Evaluation Catalog")
    
    # Merge current data streams with our market averages dataframe
    df_evaluated = pd.merge(df_properties, df_all_market, on='locality', how='left')
    
    # Loop over rows and print out customized smart badges layout
    for index, row in df_evaluated.iterrows():
        col_desc, col_badge = st.columns([4, 1])
        
        with col_desc:
            st.markdown(f"**{row['title']}** — located in *{row['locality']}* ({row['bedrooms']} BHK)")
            st.write(f"📐 Size: {row['square_feet']} sqft | 💰 Evaluation: ₹{row['price']:,.0f} | Rate: ₹{row['cost_per_sqft']:.0f}/sqft")
            
        with col_badge:
            # If the specific house rate is lower than the neighborhood average, it's an official bargain!
            if row['cost_per_sqft'] < row['neighborhood_avg_sqft']:
                savings_pct = ((row['neighborhood_avg_sqft'] - row['cost_per_sqft']) / row['neighborhood_avg_sqft']) * 100
                st.markdown(f'<div class="bargain-badge">🔥 BARGAIN ({savings_pct:.0f}% Under Market)</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="normal-badge">⚖️ Standard Market Rate</div>', unsafe_allow_html=True)
        st.write("---")
    
    # Draw vector charts via Plotly Express
    st.markdown("#### 📈 Market Value Distribution Scatter Chart Matrix")
    fig = px.scatter(df_properties, x="square_feet", y="price", text="title", size="bedrooms", 
                     color="locality", labels={"square_feet": "Property Size (Square Feet)", "price": "Total Evaluation (INR)"},
                     template="plotly_dark", color_continuous_scale="Tealgrn")
    fig.update_traces(textposition='top center', marker=dict(line=dict(width=1, color='White')))
    fig.update_layout(plot_bgcolor='rgba(15,23,42,0.5)', paper_bgcolor='rgba(15,23,42,1)')
    st.plotly_chart(fig, use_container_width=True)