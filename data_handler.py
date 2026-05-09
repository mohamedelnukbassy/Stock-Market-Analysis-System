"""
Data Handler Module
===================
Handles all stock data operations: fetching, cleaning, and processing.

Responsibilities:
- Member 1: API integration with yfinance
- Member 2: Data cleaning and processing with Pandas
"""

import yfinance as yf
import pandas as pd
import numpy as np


class StockDataHandler:
    """
    Class to handle stock data fetching and processing.
    Uses yfinance to get real-time and historical stock data.
    """

    def __init__(self, symbol):
        """
        Initialize the data handler with a stock symbol.

        Args:
            symbol (str): Stock ticker symbol (e.g., 'AAPL')
        """
        self.symbol = symbol.upper().strip()
        self.ticker = None
        self.data = None
        self.info = None

    def fetch_data(self, period="1mo"):
        """
        Fetch stock data from Yahoo Finance API.

        Args:
            period (str): Time period (e.g., '7d', '1mo', '3mo', '1y')

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Create ticker object
            self.ticker = yf.Ticker(self.symbol)

            # Fetch historical data
            self.data = self.ticker.history(period=period)

            # Validate that data was returned
            if self.data is None or self.data.empty:
                return False, f"No data found for symbol '{self.symbol}'. Please check the symbol and try again."

            # Clean the data
            self._clean_data()

            # Try to fetch additional info
            try:
                self.info = self.ticker.info
            except Exception:
                self.info = {}

            return True, "Data fetched successfully"

        except Exception as e:
            return False, f"Error fetching data: {str(e)}"

    def _clean_data(self):
        """
        Clean and prepare the stock data using Pandas.
        - Remove NaN values
        - Round numeric columns
        - Add calculated columns
        """
        if self.data is None or self.data.empty:
            return

        # Drop rows with all NaN values
        self.data = self.data.dropna(how='all')

        # Round price columns to 2 decimal places
        price_columns = ['Open', 'High', 'Low', 'Close']
        for col in price_columns:
            if col in self.data.columns:
                self.data[col] = self.data[col].round(2)

        # Calculate daily change percentage
        self.data['Daily_Change_%'] = (
            self.data['Close'].pct_change() * 100
        ).round(2)

        # Calculate moving averages
        self.data['MA_7'] = self.data['Close'].rolling(window=7).mean().round(2)
        self.data['MA_20'] = self.data['Close'].rolling(window=20).mean().round(2)

    def get_data(self):
        """Return the cleaned stock data."""
        return self.data

    def get_stock_info(self):
        """
        Get basic stock information.

        Returns:
            dict: Stock information including name, sector, industry, etc.
        """
        if self.info is None:
            self.info = {}

        return {
            'symbol': self.symbol,
            'name': self.info.get('longName', self.symbol),
            'sector': self.info.get('sector', 'N/A'),
            'industry': self.info.get('industry', 'N/A'),
            'currency': self.info.get('currency', 'USD'),
            'exchange': self.info.get('exchange', 'N/A'),
            'country': self.info.get('country', 'N/A'),
            'website': self.info.get('website', 'N/A'),
        }

    def get_key_metrics(self):
        """
        Calculate key metrics for the stock.

        Returns:
            dict: Key financial metrics
        """
        if self.data is None or self.data.empty:
            return {}

        current_price = float(self.data['Close'].iloc[-1])

        # Daily change
        if len(self.data) >= 2:
            previous_price = float(self.data['Close'].iloc[-2])
            daily_change = current_price - previous_price
            daily_change_pct = (daily_change / previous_price) * 100
        else:
            daily_change = 0
            daily_change_pct = 0

        return {
            'current_price': current_price,
            'previous_price': float(self.data['Close'].iloc[-2]) if len(self.data) >= 2 else current_price,
            'daily_change': round(daily_change, 2),
            'daily_change_pct': round(daily_change_pct, 2),
            'high': float(self.data['High'].max()),
            'low': float(self.data['Low'].min()),
            'avg_volume': float(self.data['Volume'].mean()),
            'total_volume': float(self.data['Volume'].sum()),
        }

    def get_price_statistics(self):
        """
        Calculate price statistics.

        Returns:
            pd.Series: Statistical summary of closing prices
        """
        if self.data is None or self.data.empty:
            return pd.Series()

        close_prices = self.data['Close']
        stats = pd.Series({
            'Mean Price': f"${close_prices.mean():.2f}",
            'Median Price': f"${close_prices.median():.2f}",
            'Standard Deviation': f"${close_prices.std():.2f}",
            'Maximum Price': f"${close_prices.max():.2f}",
            'Minimum Price': f"${close_prices.min():.2f}",
            'Price Range': f"${close_prices.max() - close_prices.min():.2f}",
        })

        return stats

    def get_recent_data(self, days=5):
        """
        Get the most recent N days of data.

        Args:
            days (int): Number of recent days to return

        Returns:
            pd.DataFrame: Recent stock data
        """
        if self.data is None or self.data.empty:
            return pd.DataFrame()

        recent = self.data.tail(days).copy()

        # Format for display
        display_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        recent_display = recent[display_columns].copy()

        # Format index as date strings
        recent_display.index = recent_display.index.strftime('%Y-%m-%d')

        # Format numbers
        for col in ['Open', 'High', 'Low', 'Close']:
            recent_display[col] = recent_display[col].apply(lambda x: f"${x:.2f}")
        recent_display['Volume'] = recent_display['Volume'].apply(lambda x: f"{int(x):,}")

        return recent_display

    def get_performance_analysis(self):
        """
        Perform performance analysis on the stock data.

        Returns:
            dict: Performance metrics
        """
        if self.data is None or self.data.empty:
            return {}

        first_price = float(self.data['Close'].iloc[0])
        last_price = float(self.data['Close'].iloc[-1])

        total_return = last_price - first_price
        total_return_pct = (total_return / first_price) * 100

        # Volatility (standard deviation of daily returns)
        daily_returns = self.data['Close'].pct_change().dropna() * 100
        volatility = daily_returns.std()

        # Average daily change
        avg_daily_change = daily_returns.mean()

        return {
            'first_price': round(first_price, 2),
            'last_price': round(last_price, 2),
            'total_return': round(total_return, 2),
            'total_return_pct': round(total_return_pct, 2),
            'volatility': round(volatility, 2) if not np.isnan(volatility) else 0,
            'avg_daily_change': round(avg_daily_change, 2) if not np.isnan(avg_daily_change) else 0,
            'best_day': round(daily_returns.max(), 2) if not daily_returns.empty else 0,
            'worst_day': round(daily_returns.min(), 2) if not daily_returns.empty else 0,
        }

    def calculate_moving_average(self, window=20):
        """
        Calculate moving average for given window.

        Args:
            window (int): Window size in days

        Returns:
            pd.Series: Moving average values
        """
        if self.data is None or self.data.empty:
            return pd.Series()

        return self.data['Close'].rolling(window=window).mean()
