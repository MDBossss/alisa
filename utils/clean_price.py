import re

def clean_price(price_str):
    try:
        # Remove quotes, newlines, and leading/trailing whitespace
        cleaned = price_str.replace('"', '').replace('\n', '').strip()
        # Remove Euro symbol and "ab" prefix
        cleaned = re.sub(r'ab\s*|\s*€', '', cleaned, flags=re.IGNORECASE)
        # Replace comma with period for decimal
        cleaned = cleaned.replace(',', '.')
        # Convert to float
        return f"{float(cleaned)}€"
    except (ValueError, TypeError) as e:
        print(f"Error cleaning price '{price_str}': {e}")
        return None  # Return None for invalid prices