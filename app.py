"""
Stock Market Analysis System
============================
A Streamlit-based web application for analyzing stock market data.
Built using Python, yfinance, Pandas, and Plotly.
"""

import streamlit as st
from datetime import datetime
from data_handler import StockDataHandler
from visualizer import StockVisualizer
from utils import format_number, format_currency, get_change_color

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="Stock Market Analysis System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Custom CSS Styling
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem;
    }
    .footer {
        text-align: center;
        color: #888;
        padding: 2rem 0 1rem 0;
        border-top: 1px solid #eee;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Header
# ============================================================
st.markdown('<div class="main-header">📈 Stock Market Analysis System</div>',
            unsafe_allow_html=True)

# ============================================================
# Sidebar - User Inputs
# ============================================================
with st.sidebar:
    st.header("⚙️ Settings")

    st.subheader("📊 Stock Selection")

    # Popular stock suggestions
    popular_stocks = {
        "Apple (AAPL)": "AAPL",
        "Microsoft (MSFT)": "MSFT",
        "Google (GOOGL)": "GOOGL",
        "Amazon (AMZN)": "AMZN",
        "Tesla (TSLA)": "TSLA",
        "Meta (META)": "META",
        "Netflix (NFLX)": "NFLX",
        "NVIDIA (NVDA)": "NVDA",
        "Custom": "CUSTOM"
    }

    selected = st.selectbox(
        "Choose a stock or enter custom:",
        list(popular_stocks.keys())
    )

    if popular_stocks[selected] == "CUSTOM":
        symbol = st.text_input(
            "Enter Stock Symbol:",
            value="AAPL",
            help="Example: AAPL, GOOGL, TSLA"
        ).upper().strip()
    else:
        symbol = popular_stocks[selected]
        st.info(f"Selected: **{symbol}**")

    st.subheader("📅 Time Period")
    period_options = {
        "7 Days": "7d",
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "5 Years": "5y"
    }
    selected_period = st.selectbox(
        "Select Time Period:",
        list(period_options.keys()),
        index=1
    )
    period = period_options[selected_period]

    st.subheader("📈 Chart Type")
    chart_type = st.radio(
        "Choose Chart Type:",
        ["Line Chart", "Candlestick", "Area Chart"]
    )

    st.subheader("🔧 Indicators")
    show_ma = st.checkbox("Show Moving Average (MA)", value=True)
    if show_ma:
        ma_period = st.slider("MA Period (days):", 5, 50, 20)
    else:
        ma_period = 20

    show_volume = st.checkbox("Show Volume Chart", value=True)

    analyze_btn = st.button("🔍 Analyze Stock", type="primary")

    st.markdown("---")
    st.caption("💡 **Tip:** Use stock symbols like AAPL, GOOGL, MSFT")
    st.caption(f"⏰ Last update: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ============================================================
# Main Content Area
# ============================================================
if analyze_btn or 'analyzed' in st.session_state:
    st.session_state['analyzed'] = True

    # Validate input
    if not symbol or len(symbol) < 1:
        st.error("⚠️ Please enter a valid stock symbol!")
        st.stop()

    # Initialize data handler
    handler = StockDataHandler(symbol)

    # Show loading spinner
    with st.spinner(f"📡 Fetching data for {symbol}..."):
        success, message = handler.fetch_data(period=period)

    if not success:
        st.error(f"❌ {message}")
        st.info("💡 Make sure the stock symbol is correct (e.g., AAPL, GOOGL)")
        st.stop()

    # Get stock info
    info = handler.get_stock_info()
    data = handler.get_data()

    # ========================================
    # Section 1: Stock Information Header
    # ========================================
    st.success(f"✅ Successfully loaded data for **{info['name']}**")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"🏢 {info['name']} ({info['symbol']})")
        st.caption(f"**Sector:** {info['sector']} | **Industry:** {info['industry']}")
    with col2:
        st.caption(f"**Currency:** {info['currency']}")
        st.caption(f"**Exchange:** {info['exchange']}")

    # ========================================
    # Section 2: Key Metrics
    # ========================================
    st.markdown("### 📊 Key Metrics")

    metrics = handler.get_key_metrics()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="💰 Current Price",
            value=format_currency(metrics['current_price']),
            delta=f"{metrics['daily_change_pct']:.2f}%"
        )

    with col2:
        st.metric(
            label="📈 Period High",
            value=format_currency(metrics['high'])
        )

    with col3:
        st.metric(
            label="📉 Period Low",
            value=format_currency(metrics['low'])
        )

    with col4:
        st.metric(
            label="📊 Avg Volume",
            value=format_number(metrics['avg_volume'])
        )

    # ========================================
    # Section 3: Price Chart
    # ========================================
    st.markdown("### 📈 Price Trend Chart")

    visualizer = StockVisualizer(data, symbol)

    if chart_type == "Line Chart":
        fig = visualizer.create_line_chart(
            show_ma=show_ma,
            ma_period=ma_period
        )
    elif chart_type == "Candlestick":
        fig = visualizer.create_candlestick_chart(
            show_ma=show_ma,
            ma_period=ma_period
        )
    else:  # Area Chart
        fig = visualizer.create_area_chart(
            show_ma=show_ma,
            ma_period=ma_period
        )

    st.plotly_chart(fig, use_container_width=True)

    # ========================================
    # Section 4: Volume Chart
    # ========================================
    if show_volume:
        st.markdown("### 📊 Trading Volume")
        volume_fig = visualizer.create_volume_chart()
        st.plotly_chart(volume_fig, use_container_width=True)

    # ========================================
    # Section 5: Statistics
    # ========================================
    st.markdown("### 📋 Statistical Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💹 Price Statistics")
        stats = handler.get_price_statistics()
        stats_df = stats.reset_index()
        stats_df.columns = ['Metric', 'Value']
        st.dataframe(stats_df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("#### 📅 Recent Data (Last 5 Days)")
        recent_data = handler.get_recent_data(days=5)
        st.dataframe(recent_data, use_container_width=True)

    # ========================================
    # Section 6: Performance Analysis
    # ========================================
    st.markdown("### 🎯 Performance Analysis")

    perf = handler.get_performance_analysis()

    col1, col2, col3 = st.columns(3)

    with col1:
        change_color = "🟢" if perf['total_return_pct'] >= 0 else "🔴"
        st.markdown(f"""
        <div class="metric-card">
            <h4>{change_color} Total Return</h4>
            <h2>{perf['total_return_pct']:.2f}%</h2>
            <p>Period: {selected_period}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>📊 Volatility</h4>
            <h2>{perf['volatility']:.2f}%</h2>
            <p>Standard Deviation</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>💹 Average Daily Change</h4>
            <h2>{perf['avg_daily_change']:.2f}%</h2>
            <p>Mean Return</p>
        </div>
        """, unsafe_allow_html=True)

    # ========================================
    # Section 7: Download Data
    # ========================================
    st.markdown("### 💾 Export Data")
    csv = data.to_csv()
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"{symbol}_{period}_data.csv",
        mime="text/csv"
    )

else:
    # ========================================
    # Welcome Screen
    # ========================================
    st.markdown("## 👋 Welcome to Stock Market Analysis System")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("""
        ### 🎯 Features
        - Real-time stock prices
        - Historical data analysis
        - Interactive charts
        - Multiple indicators
        """)

    with col2:
        st.success("""
        ### 🚀 How to Use
        1. Select a stock from sidebar
        2. Choose time period
        3. Select chart type
        4. Click "Analyze Stock"
        """)

    with col3:
        st.warning("""
        ### 📚 Popular Stocks
        - **AAPL** - Apple
        - **GOOGL** - Google
        - **MSFT** - Microsoft
        - **TSLA** - Tesla
        """)

    st.markdown("---")
    st.markdown("""
    ### 🔍 About this System
    This Stock Market Analysis System helps you:
    - **Track** stock prices in real-time
    - **Visualize** price trends with interactive charts
    - **Analyze** historical performance
    - **Compare** different time periods
    - **Export** data for further analysis

    👈 **Get started by selecting a stock from the sidebar!**
    """)

# ============================================================
# Footer
# ============================================================
st.markdown("""
<div class="footer">
    <p>📈 <b>Stock Market Analysis System</b> | Built with Streamlit & Python</p>
    <p>Data Source: Yahoo Finance | © 2025 Project Team</p>
</div>
""", unsafe_allow_html=True)
