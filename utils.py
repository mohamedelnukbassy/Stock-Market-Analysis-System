"""
Utility Functions Module
========================
Helper functions used across the application.
"""


def format_number(num):
    """
    Format large numbers with K, M, B suffixes.

    Args:
        num (float): Number to format

    Returns:
        str: Formatted number string
    """
    if num is None:
        return "N/A"

    try:
        num = float(num)
    except (ValueError, TypeError):
        return "N/A"

    if abs(num) >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif abs(num) >= 1_000:
        return f"{num / 1_000:.2f}K"
    else:
        return f"{num:,.0f}"


def format_currency(amount, currency="$"):
    """
    Format a number as currency.

    Args:
        amount (float): Amount to format
        currency (str): Currency symbol

    Returns:
        str: Formatted currency string
    """
    if amount is None:
        return "N/A"

    try:
        return f"{currency}{amount:,.2f}"
    except (ValueError, TypeError):
        return "N/A"


def get_change_color(change):
    """
    Get color based on change value (green for positive, red for negative).

    Args:
        change (float): Change value

    Returns:
        str: Color name
    """
    if change > 0:
        return "green"
    elif change < 0:
        return "red"
    else:
        return "gray"


def validate_symbol(symbol):
    """
    Validate stock symbol format.

    Args:
        symbol (str): Stock symbol to validate

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not symbol:
        return False, "Symbol cannot be empty"

    symbol = symbol.strip().upper()

    if len(symbol) < 1 or len(symbol) > 10:
        return False, "Symbol must be 1-10 characters"

    if not symbol.replace('.', '').replace('-', '').isalnum():
        return False, "Symbol contains invalid characters"

    return True, symbol


def calculate_percentage_change(old_value, new_value):
    """
    Calculate percentage change between two values.

    Args:
        old_value (float): Original value
        new_value (float): New value

    Returns:
        float: Percentage change
    """
    if old_value == 0 or old_value is None:
        return 0
    return ((new_value - old_value) / old_value) * 100
