"""
Visualizer Module
=================
Creates interactive charts and visualizations using Plotly.

Responsibility:
- Member 3: Charts and graphs visualization
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots


class StockVisualizer:
    """
    Class to create various stock chart visualizations.
    Uses Plotly for interactive charts.
    """

    # Color scheme
    COLORS = {
        'primary': '#1f77b4',
        'success': '#2ca02c',
        'danger': '#d62728',
        'warning': '#ff7f0e',
        'info': '#17a2b8',
        'background': '#ffffff',
        'grid': '#e6e6e6',
    }

    def __init__(self, data, symbol):
        """
        Initialize the visualizer.

        Args:
            data (pd.DataFrame): Stock data with OHLCV columns
            symbol (str): Stock symbol
        """
        self.data = data
        self.symbol = symbol

    def create_line_chart(self, show_ma=True, ma_period=20):
        """
        Create a line chart of closing prices.

        Args:
            show_ma (bool): Whether to show moving average
            ma_period (int): Moving average period

        Returns:
            plotly.graph_objects.Figure: Line chart figure
        """
        fig = go.Figure()

        # Main price line
        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=self.data['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color=self.COLORS['primary'], width=2.5),
            hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br>' +
                          '<b>Price:</b> $%{y:.2f}<extra></extra>'
        ))

        # Moving average
        if show_ma:
            ma_data = self.data['Close'].rolling(window=ma_period).mean()
            fig.add_trace(go.Scatter(
                x=self.data.index,
                y=ma_data,
                mode='lines',
                name=f'MA ({ma_period} days)',
                line=dict(color=self.COLORS['warning'], width=2, dash='dash'),
                hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br>' +
                              f'<b>MA{ma_period}:</b> $%{{y:.2f}}<extra></extra>'
            ))

        fig.update_layout(
            title=dict(
                text=f"{self.symbol} - Stock Price Trend",
                font=dict(size=20, color=self.COLORS['primary']),
                x=0.5,
                xanchor='center'
            ),
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white",
            hovermode='x unified',
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(showgrid=True, gridcolor=self.COLORS['grid']),
            yaxis=dict(showgrid=True, gridcolor=self.COLORS['grid']),
        )

        return fig

    def create_candlestick_chart(self, show_ma=True, ma_period=20):
        """
        Create a candlestick chart.

        Args:
            show_ma (bool): Whether to show moving average
            ma_period (int): Moving average period

        Returns:
            plotly.graph_objects.Figure: Candlestick chart figure
        """
        fig = go.Figure()

        # Candlestick chart
        fig.add_trace(go.Candlestick(
            x=self.data.index,
            open=self.data['Open'],
            high=self.data['High'],
            low=self.data['Low'],
            close=self.data['Close'],
            name='OHLC',
            increasing_line_color=self.COLORS['success'],
            decreasing_line_color=self.COLORS['danger']
        ))

        # Moving average
        if show_ma:
            ma_data = self.data['Close'].rolling(window=ma_period).mean()
            fig.add_trace(go.Scatter(
                x=self.data.index,
                y=ma_data,
                mode='lines',
                name=f'MA ({ma_period} days)',
                line=dict(color=self.COLORS['warning'], width=2)
            ))

        fig.update_layout(
            title=dict(
                text=f"{self.symbol} - Candlestick Chart",
                font=dict(size=20, color=self.COLORS['primary']),
                x=0.5,
                xanchor='center'
            ),
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white",
            height=500,
            showlegend=True,
            xaxis_rangeslider_visible=False,
            xaxis=dict(showgrid=True, gridcolor=self.COLORS['grid']),
            yaxis=dict(showgrid=True, gridcolor=self.COLORS['grid']),
        )

        return fig

    def create_area_chart(self, show_ma=True, ma_period=20):
        """
        Create a filled area chart.

        Args:
            show_ma (bool): Whether to show moving average
            ma_period (int): Moving average period

        Returns:
            plotly.graph_objects.Figure: Area chart figure
        """
        fig = go.Figure()

        # Area chart
        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=self.data['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color=self.COLORS['primary'], width=2),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)',
            hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br>' +
                          '<b>Price:</b> $%{y:.2f}<extra></extra>'
        ))

        # Moving average
        if show_ma:
            ma_data = self.data['Close'].rolling(window=ma_period).mean()
            fig.add_trace(go.Scatter(
                x=self.data.index,
                y=ma_data,
                mode='lines',
                name=f'MA ({ma_period} days)',
                line=dict(color=self.COLORS['warning'], width=2, dash='dash')
            ))

        # Calculate y-axis range to start near min price (not zero)
        min_price = self.data['Close'].min() * 0.95
        max_price = self.data['Close'].max() * 1.05

        fig.update_layout(
            title=dict(
                text=f"{self.symbol} - Area Chart",
                font=dict(size=20, color=self.COLORS['primary']),
                x=0.5,
                xanchor='center'
            ),
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white",
            hovermode='x unified',
            height=500,
            showlegend=True,
            yaxis=dict(
                range=[min_price, max_price],
                showgrid=True,
                gridcolor=self.COLORS['grid']
            ),
            xaxis=dict(showgrid=True, gridcolor=self.COLORS['grid']),
        )

        return fig

    def create_volume_chart(self):
        """
        Create a volume bar chart.

        Returns:
            plotly.graph_objects.Figure: Volume chart figure
        """
        # Color bars based on price movement
        colors = [
            self.COLORS['success'] if close >= open_ else self.COLORS['danger']
            for close, open_ in zip(self.data['Close'], self.data['Open'])
        ]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=self.data.index,
            y=self.data['Volume'],
            name='Volume',
            marker_color=colors,
            hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br>' +
                          '<b>Volume:</b> %{y:,.0f}<extra></extra>'
        ))

        fig.update_layout(
            title=dict(
                text=f"{self.symbol} - Trading Volume",
                font=dict(size=20, color=self.COLORS['primary']),
                x=0.5,
                xanchor='center'
            ),
            xaxis_title="Date",
            yaxis_title="Volume",
            template="plotly_white",
            height=350,
            showlegend=False,
            xaxis=dict(showgrid=True, gridcolor=self.COLORS['grid']),
            yaxis=dict(showgrid=True, gridcolor=self.COLORS['grid']),
        )

        return fig

    def create_combined_chart(self, show_ma=True, ma_period=20):
        """
        Create a combined chart with price and volume.

        Args:
            show_ma (bool): Whether to show moving average
            ma_period (int): Moving average period

        Returns:
            plotly.graph_objects.Figure: Combined chart figure
        """
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.7, 0.3],
            subplot_titles=("Price", "Volume")
        )

        # Price line
        fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=self.data['Close'],
                mode='lines',
                name='Close Price',
                line=dict(color=self.COLORS['primary'], width=2)
            ),
            row=1, col=1
        )

        # Moving average
        if show_ma:
            ma_data = self.data['Close'].rolling(window=ma_period).mean()
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=ma_data,
                    mode='lines',
                    name=f'MA ({ma_period})',
                    line=dict(color=self.COLORS['warning'], width=2, dash='dash')
                ),
                row=1, col=1
            )

        # Volume bars
        colors = [
            self.COLORS['success'] if close >= open_ else self.COLORS['danger']
            for close, open_ in zip(self.data['Close'], self.data['Open'])
        ]

        fig.add_trace(
            go.Bar(
                x=self.data.index,
                y=self.data['Volume'],
                name='Volume',
                marker_color=colors
            ),
            row=2, col=1
        )

        fig.update_layout(
            title=f"{self.symbol} - Price & Volume Analysis",
            template="plotly_white",
            height=700,
            showlegend=True,
            hovermode='x unified'
        )

        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)

        return fig
