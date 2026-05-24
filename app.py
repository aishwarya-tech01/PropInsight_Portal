import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np
import io
import urllib.parse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configure the structural layout of our web viewport interface
st.set_page_config(page_title="PropInsight™ Analytics", page_icon="🏢", layout="wide")

# =====================================================================
# 🎨 BRANDING THEME SKIN INJECTION (#002244 & #FFFFFF) - FINAL POLISH
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
    
    /* FORCE ALL SLIDER LABEL TEXT AND NUMBERS TO WHITE */
    div[data-testid="stSlider"] label p,
    div[data-testid="stSlider"] span,
    div[data-testid="stSlider"] div,
    div[data-testid="stSlider"] [data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* FIX: FORCE SELECTBOX AND MAIN AREA WIDGET LABELS TO PURE WHITE */
    div[data-testid="stSelectbox"] label p,
    div[data-testid="stSelectbox"] [data-testid="stWidgetLabel"] p,
    .main label, 
    .main [data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-weight: 700 !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    
    /* FIXED FINANCING ANALYSIS SUMMARY BOX */
    .emi-container {
        background-color: #002244 !important;
        border: 2px solid #ffffff !important;
        padding: 25px !important;
        border-radius: 12px !important;
        margin-top: 15px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
        display: block !important;
        clear: both !important;
        overflow: visible !important;
    }
    .emi-container p, 
    .emi-container h3, 
    .emi-container h4,
    .emi-container b {
        color: #ffffff !important;
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
    
    # Core Listings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            property_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, locality TEXT, bedrooms INTEGER, price REAL, square_feet INTEGER
        )
    ''')
    
    # Historical Trend Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_trends (
            trend_id INTEGER PRIMARY KEY AUTOINCREMENT,
            locality TEXT, quarter TEXT, avg_rate_sqft REAL
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
        
    cursor.execute("SELECT COUNT(*) FROM price_trends")
    if cursor.fetchone()[0] == 0:
        trend_records = [
            ('Koregaon Park', 'Q1-25', 6200), ('Koregaon Park', 'Q2-25', 6450), ('Koregaon Park', 'Q3-25', 6600), ('Koregaon Park', 'Q4-25', 6818),
            ('Kothrud', 'Q1-25', 5900), ('Kothrud', 'Q2-25', 6100), ('Kothrud', 'Q3-25', 6300), ('Kothrud', 'Q4-25', 6551),
            ('Baner', 'Q1-25', 5200), ('Baner', 'Q2-25', 5500), ('Baner', 'Q3-25', 5800), ('Baner', 'Q4-25', 6140),
            ('Wagholi', 'Q1-25', 4100), ('Wagholi', 'Q2-25', 4400), ('Wagholi', 'Q3-25', 4650), ('Wagholi', 'Q4-25', 4842)
        ]
        cursor.executemany("INSERT INTO price_trends (locality, quarter, avg_rate_sqft) VALUES (?, ?, ?)", trend_records)
        
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

if selected_locality == "All Locations":
    df_trends = pd.read_sql_query("SELECT quarter, locality, avg_rate_sqft FROM price_trends ORDER BY quarter ASC", conn)
else:
    df_trends = pd.read_sql_query("SELECT quarter, locality, avg_rate_sqft FROM price_trends WHERE locality = ? ORDER BY quarter ASC", [selected_locality], conn)
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
    
    action_col1, action_col2 = st.columns([2, 5])
    
    with action_col1:
        speech_text = f"Analysis complete. Found {total_options} property matches. The average valuation is {int(avg_market_price)} Rupees."
        tts_html = f"""
            <script>
            function speakSummary() {{
                var msg = new SpeechSynthesisUtterance("{speech_text}");
                window.speechSynthesis.speak(msg);
            }}
            </script>
            <button onclick="speakSummary()" style="
                background-color: #002244; 
                color: white; 
                border: 2px solid white; 
                padding: 12px 20px; 
                border-radius: 8px; 
                cursor: pointer; 
                font-weight: bold;
                font-size: 0.95rem; 
                margin-top: 10px; 
                width: 100%;
                white-space: nowrap;
            ">🔊 Audio Summary</button>
        """
        st.components.v1.html(tts_html, height=75)
        
    with action_col2:
        def generate_pdf_report(dataframe, total_matches, avg_price, location_tag):
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
            story = []
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle('ReportTitle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#002244'), spaceAfter=15)
            meta_style = ParagraphStyle('ReportMeta', parent=styles['Normal'], fontSize=10, textColor=colors.gray, spaceAfter=20)
            body_style = ParagraphStyle('ReportBody', parent=styles['Normal'], fontSize=11, spaceAfter=12)
            
            story.append(Paragraph("PropInsight™ Valuation Summary Report", title_style))
            story.append(Paragraph(f"Target Cluster Region: {location_tag} | Dynamic Scope Audit Parameters", meta_style))
            story.append(Spacer(1, 10))
            
            summary_msg = f"<b>Executive Summary:</b> The localized matrix isolated <b>{total_matches} viable real estate assets</b> within the configured budget limitations. The mean capital valuation benchmark evaluates at <b>INR {avg_price:,.2f}</b>."
            story.append(Paragraph(summary_msg, body_style))
            story.append(Spacer(1, 15))
            
            table_data = [['Property Asset Title', 'Neighborhood', 'BHK', 'Market Pricing (INR)']]
            for _, row in dataframe.head(10).iterrows():
                table_data.append([row['title'], row['locality'], str(row['bedrooms']), f"{row['price']:,.0f}"])
                
            pdf_table = Table(table_data, colWidths=[200, 130, 50, 130])
            pdf_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002244')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 10),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F4F6F9')),
                ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ]))
            story.append(pdf_table)
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()

        pdf_data = generate_pdf_report(df_properties, total_options, avg_market_price, selected_locality)
        st.download_button(
            label="📄 Export Executive Analytics Report (PDF)",
            data=pdf_data,
            file_name="PropInsight_Market_Report.pdf",
            mime="application/pdf",
            key="pdf_download_btn",
            help="Generates an on-the-fly executive reporting overview asset"
        )

    st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
    
    # Symmetrical Chart Panel
    graph_col1, graph_col2 = st.columns(2)
    
    with graph_col1:
        st.markdown("### 📈 Price vs. Area Sizing Breakdown")
        df_plot = df_properties.copy()
        if not df_plot.empty:
            np.random.seed(42)
            df_plot['jittered_area'] = df_plot['square_feet'] + np.random.uniform(-25, 25, len(df_plot))
            df_plot['jittered_price'] = df_plot['price'] + np.random.uniform(-100000, 100000, len(df_plot))
        
        fig_scatter = px.scatter(
            df_plot, x="jittered_area", y="jittered_price", color="locality", size="cost_per_sqft", hover_name="title",
            hover_data={"square_feet": True, "price": True, "jittered_area": False, "jittered_price": False},
            labels={"jittered_area": "Property Size (Sqft)", "jittered_price": "Market Price (INR)", "locality": "Neighborhood"},
            template="plotly_dark"
        )
        fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with graph_col2:
        st.markdown("### 📉 Historical Neighborhood Price Trends")
        fig_line = px.line(
            df_trends, x="quarter", y="avg_rate_sqft", color="locality", markers=True,
            labels={"quarter": "Timeline Interval (Quarter)", "avg_rate_sqft": "Rate (INR / Sqft)", "locality": "Neighborhood"},
            title="Capital Growth Compounding Path (2025)", template="plotly_dark"
        )
        fig_line.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_line, use_container_width=True)
    
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
    
    # BONUS FEATURE LAYER: ON-THE-FLY LOAN & EMI ESTIMATOR ENGINE
    st.markdown("### 🧮 On-the-Fly Mortgage Loan & EMI Estimator")
    selected_property_title = st.selectbox("Isolate an Asset Row for Financial Estimation Analysis", df_merged['title'].unique())
    property_row = df_merged[df_merged['title'] == selected_property_title].iloc[0]
    property_price = property_row['price']
    
    calc_col1, calc_col2 = st.columns(2)
    with calc_col1:
        down_payment_pct = st.slider("Down Payment Allocation Percentage (%)", min_value=10, max_value=50, value=20, step=5)
        loan_tenure_years = st.slider("Loan Repayment Tenure Duration (Years)", min_value=5, max_value=30, value=20, step=5)
        interest_rate = st.slider("Annual Bank Interest Lending Rate (%)", min_value=5.0, max_value=15.0, value=8.5, step=0.1)
        
    with calc_col2:
        down_payment_amount = property_price * (down_payment_pct / 100)
        principal_loan_amount = property_price - down_payment_amount
        monthly_rate = (interest_rate / 12) / 100
        total_months = loan_tenure_years * 12
        
        if monthly_rate > 0:
            monthly_emi = principal_loan_amount * (monthly_rate * (1 + monthly_rate)**total_months) / ((1 + monthly_rate)**total_months - 1)
        else:
            monthly_emi = principal_loan_amount / total_months
            
        st.markdown(f"""
            <div class="emi-container">
                <h4 style="margin-top:0; margin-bottom:15px; font-weight:700;">📋 Financial Assessment Summary</h4>
                <p style="margin:8px 0;">💸 <b>Isolated Asset Price:</b> ₹{property_price:,.0f}</p>
                <p style="margin:8px 0;">🧱 <b>Upfront Down Payment Plan ({down_payment_pct}%):</b> ₹{down_payment_amount:,.0f}</p>
                <p style="margin:8px 0;">🛡️ <b>Principal Bank Financing Total:</b> ₹{principal_loan_amount:,.0f}</p>
                <hr style="border:0; height:1px; background-color:rgba(255,255,255,0.3); margin:15px 0;">
                <h3 style="color:#ffffff !important; margin-top:5px; margin-bottom:0; font-weight:800;">📉 Estimated Installment: ₹{monthly_emi:,.0f} / Month</h3>
            </div>
        """, unsafe_allow_html=True)

    # =====================================================================
    # 🌟 NEW FEATURE: INTERACTIVE WHATSAPP LEAD SHARING ENGINE
    # =====================================================================
    st.markdown("### 📲 Share Deal Briefing to WhatsApp")
    
    # Safely compile text block metrics from the currently selected property above
    raw_whatsapp_msg = (
        f"🏢 *PropInsight™ Deal Briefing Alert*\n\n"
        f"📍 *Property:* {property_row['title']}\n"
        f"🏘️ *Locality:* {property_row['locality']}\n"
        f"🛏️ *Configuration:* {property_row['bedrooms']} BHK\n"
        f"💰 *Market Valuation:* ₹{property_price:,.0f}\n"
        f"📐 *Sizing Area:* {property_row['square_feet']} Sqft\n"
        f"🏷️ *Status:* {property_row['Market Status']}\n\n"
        f"📉 _Estimated Loan EMI evaluates at approximately ₹{monthly_emi:,.0f}/month._"
    )
    
    # URL-encode the text string to pass safely to browser protocols
    encoded_message = urllib.parse.quote(raw_whatsapp_msg)
    whatsapp_api_url = f"https://wa.me/?text={encoded_message}"
    
    # Build button container styling
    whatsapp_btn_html = f"""
        <a href="{whatsapp_api_url}" target="_blank" style="text-decoration: none;">
            <button style="
                background-color: #25D366; 
                color: white; 
                border: none; 
                padding: 12px 24px; 
                border-radius: 8px; 
                cursor: pointer; 
                font-weight: bold;
                font-size: 1rem;
                display: flex;
                align-items: center;
                gap: 10px;
                box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
                margin-top: 10px;
            ">
                💬 Send Briefing via WhatsApp Web
            </button>
        </a>
    """
    st.markdown(whatsapp_btn_html, unsafe_allow_html=True)