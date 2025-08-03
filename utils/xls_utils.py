import pandas as pd
import openpyxl

def save_to_excel(data_dict, filename="output.xlsx"):
    """
    Saves multiple lists of dictionaries to an Excel file, each as a separate sheet.
    data_dict: dict of {sheet_name: list_of_dicts}
    - Auto-adjusts column widths to fit the content.
    - Freezes the header row.
    """
    if not data_dict:
        print("No data to save.")
        return

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        for sheet_name, data in data_dict.items():
            if not data:
                continue
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=f"p_{sheet_name}", index=False)
            worksheet = writer.sheets[f"p_{sheet_name}"]
            worksheet.freeze_panes = 'A2'
            for column in worksheet.columns:
                column_letter = column[0].column_letter
                max_length = 0
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except (TypeError, ValueError):
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    print(f"Data saved to {filename} successfully with auto-formatting.")