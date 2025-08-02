import pandas as pd
import openpyxl

def save_to_excel(data, sheet_name="Parts", filename="output.xlsx"):
    """
    Saves a list of dictionaries to an Excel file with nice formatting.
    - Auto-adjusts column widths to fit the content.
    - Freezes the header row.
    """
    if not data:
        print("No data to save.")
        return

    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(data)

    # Use the Pandas ExcelWriter to write the DataFrame
    # 'with' statement ensures the file is properly closed
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=f"p_{sheet_name}", index=False)

        # Get the worksheet object from the writer for formatting
        worksheet = writer.sheets[f"p_{sheet_name}"]
        
        # --- Formatting Section ---

        # 1. Freeze the header row (the first row)
        worksheet.freeze_panes = 'A2'

        # 2. Auto-adjust column widths based on content
        for column in worksheet.columns:
            column_letter = column[0].column_letter  # Get the column letter (e.g., 'A', 'B', 'C')
            max_length = 0
            
            # Find the maximum length of content in the column
            for cell in column:
                try:
                    # Convert to string and find length; default to 0 for non-text values
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except (TypeError, ValueError):
                    pass # Handle cases where cell.value is None
            
            # Add a small buffer (e.g., 2 characters) for padding
            adjusted_width = (max_length + 2)
            
            # Set the column width
            worksheet.column_dimensions[column_letter].width = adjusted_width

    print(f"Data saved to {filename} successfully with auto-formatting.")