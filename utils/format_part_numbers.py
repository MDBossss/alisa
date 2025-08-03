import re

def format_part_numbers(part_numbers_string):
    """
    Formats a string of part numbers into a list of part numbers.
    
    Args:
        part_numbers_string (str): A string containing part numbers separated by commas or spaces.
        
    Returns:
        list: A list of formatted part numbers.
    """
    if not part_numbers_string:
        return []

    # Split by comma or whitespace and strip each part
    part_numbers = [part.strip() for part in re.split(r'[,\s]+', part_numbers_string) if part.strip()]
    
    return part_numbers