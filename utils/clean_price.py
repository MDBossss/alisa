import re

def clean_price(price_str):
    try:
        # Remove quotes, newlines, and leading/trailing whitespace
        cleaned = price_str.replace('"', '').replace('\n', '').strip()
        # Remove Euro symbol and "ab" prefix
        cleaned = re.sub(r'ab\s*|\s*€', '', cleaned, flags=re.IGNORECASE)
        # Remove non-breaking spaces and normal spaces
        cleaned = cleaned.replace('\xa0', '').replace(' ', '')
        # Remove thousands separator (periods before a comma or end)
        cleaned = re.sub(r'\.(?=\d{3}(,|$))', '', cleaned)
        # Replace decimal comma with period
        cleaned = cleaned.replace(',', '.')
        return f"{float(cleaned)}€"
    except (ValueError, TypeError) as e:
        print(f"Error cleaning price '{price_str}': {e}")
        return None  # Return None for invalid prices