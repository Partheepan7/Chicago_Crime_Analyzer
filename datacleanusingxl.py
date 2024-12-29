import pandas as pd
from datetime import datetime

# Step 1: Load the Excel file (with first 5 records)
def load_excel_file(file_path):
    print("Loading Excel file...")
    df = pd.read_excel(file_path)  # Load the entire Excel file
    print("Data Loaded Successfully!")
    print(df.head())  # Print the first few rows for validation (optional)
    return df

# Step 2: Clean the data
def clean_data(df):
    print("Cleaning data...")

    # Standardize date formats (to ensure consistency in datetime columns)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    df['Updated On'] = pd.to_datetime(df['Updated On'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

    # Fill missing values with meaningful defaults or statistical values
    df['X Coordinate'] = df['X Coordinate'].fillna(df['X Coordinate'].mean())  # Replace NaN with the mean of the column
    df['Y Coordinate'] = df['Y Coordinate'].fillna(df['Y Coordinate'].mean())
    df['FBI Code'] = df['FBI Code'].fillna('Unknown')  # Replace missing FBI Code with 'Unknown'
    df['Community Area'] = df['Community Area'].fillna(0)  # Replace missing Community Area with 0 (default value)
    df['Ward'] = df['Ward'].fillna(0)  # Replace missing Ward with 0 (default value)

    # Standardize text columns (to maintain uniformity in data representation)
    df['Primary Type'] = df['Primary Type'].str.title()
    df['Description'] = df['Description'].str.capitalize()
    df['Location Description'] = df['Location Description'].str.title()
    df['Block'] = df['Block'].str.replace(r"XX", "00", regex=True).str.title()

    # Validate coordinates (ensure they are within the valid latitude and longitude range for Chicago)
    valid_latitude = (df['Latitude'] >= 41.6445) & (df['Latitude'] <= 42.0231)
    valid_longitude = (df['Longitude'] >= -87.9401) & (df['Longitude'] <= -87.5245)
    df = df[valid_latitude & valid_longitude]  # Keep only rows with valid coordinates

    # Drop duplicates based on unique identifiers (Case Number and ID)
    df = df.drop_duplicates(subset=['ID', 'Case Number'])

    # Reconstruct Location column using latitude and longitude (for consistency)
    df['Location'] = df.apply(
        lambda x: f"({x['Latitude']}, {x['Longitude']})" if pd.notnull(x['Latitude']) and pd.notnull(x['Longitude']) else None,
        axis=1
    )

    print("Data Cleaning Completed!")
    print(df.head())  # Print the first few rows after cleaning
    return df

# Step 3: Write cleaned data to another Excel file
def write_to_new_excel(df, new_file_path):
    print("Writing cleaned data to a new Excel file...")
    with pd.ExcelWriter(new_file_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Cleaned Data')  # Write to a new sheet named 'Cleaned Data'
    print("Cleaned data written to new Excel file successfully!")

# Main execution
if __name__ == "__main__":
    # Step 1: Load the dataset (only first 5 records)
    file_path = 'Crime_Data.xlsx'  # Replace with your file path
    new_file_path = 'cleaned_chicago_crime.xlsx'  # Path for the new Excel file
    df = load_excel_file(file_path)

    # Step 2: Clean the dataset
    df_cleaned = clean_data(df)

    # Step 3: Write cleaned data to a new Excel file
    write_to_new_excel(df_cleaned, new_file_path)

    print("Process completed successfully!")



