import pandas as pandas

def save_to_excel(data, sheet_name="Parts", filename="output.xlsx"):
    if not data:
        print("No data to save.")
        return

    df = pandas.DataFrame(data)

    df.to_excel(filename, sheet_name=f"p_{sheet_name}", index=False)
    print(f"Data saved to {filename} successfully.")