import pandas as pd
import pymysql
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import text

# Database connection settings
DB_USERNAME = 'root'
DB_PASSWORD = '12345'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'mdt41'

# Step 1: Connect to the database
def connect_to_db():
    engine = create_engine(f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    return engine

# Step 2: Create table if not exists
def create_table_if_not_exists(engine):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS crime_incidents (
        id INT AUTO_INCREMENT PRIMARY KEY,
        case_number VARCHAR(50),
        date DATETIME,
        block VARCHAR(255),
        iucr VARCHAR(10),
        primary_type VARCHAR(100),
        description TEXT,
        location_description VARCHAR(255),
        arrest TINYINT(1),
        domestic TINYINT(1),
        beat INT,
        district INT,
        ward INT,
        community_area INT,
        fbi_code VARCHAR(10),
        x_coordinate FLOAT,
        y_coordinate FLOAT,
        year INT,
        updated_on DATETIME,
        latitude DECIMAL(9,6),
        longitude DECIMAL(9,6),
        location VARCHAR(50)
    );
    """
    # Execute the query to create the table if it doesn't exist
    with engine.connect() as conn:
        conn.execute(text(create_table_query))
    print("Table 'crime_incidents' created if it did not exist.")

# Step 3: Load the Excel file (with first 5 records)
def load_excel_file(file_path):
    print("Loading Excel file...")
    df = pd.read_excel(file_path)  # Load the entire Excel file
    print("Data Loaded Successfully!")
    print(df.head())  # Print the first few rows for validation (optional)
    return df

# Step 4: Clean the data
def clean_data(df):
    print("Cleaning data...")

    # Standardize date formats
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    df['Updated On'] = pd.to_datetime(df['Updated On'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

    # Fill missing values with more meaningful values
    df['X Coordinate'] = df['X Coordinate'].fillna(df['X Coordinate'].mean())
    df['Y Coordinate'] = df['Y Coordinate'].fillna(df['Y Coordinate'].mean())
    df['FBI Code'] = df['FBI Code'].fillna('Unknown')
    df['Community Area'] = df['Community Area'].fillna(0)
    df['Ward'] = df['Ward'].fillna(0)

    # Standardize text columns
    df['Primary Type'] = df['Primary Type'].str.title()
    df['Description'] = df['Description'].str.capitalize()
    df['Location Description'] = df['Location Description'].str.title()
    df['Block'] = df['Block'].str.replace(r"XX", "00", regex=True).str.title()

    # Validate coordinates (ensure they fall within the valid latitude and longitude range for Chicago)
    valid_latitude = (df['Latitude'] >= 41.6445) & (df['Latitude'] <= 42.0231)
    valid_longitude = (df['Longitude'] >= -87.9401) & (df['Longitude'] <= -87.5245)
    df = df[valid_latitude & valid_longitude]

    # Drop duplicates based on ID and Case Number
    df = df.drop_duplicates(subset=['ID', 'Case Number'])

    # Reconstruct Location column using latitude and longitude
    df['Location'] = df.apply(
        lambda x: f"({x['Latitude']}, {x['Longitude']})" if pd.notnull(x['Latitude']) and pd.notnull(x['Longitude']) else None,
        axis=1
    )

    print("Data Cleaning Completed!")
    print(df.head())  # Print the first few rows after cleaning
    return df

# Step 5: Insert data into SQL table (using pymysql)
def insert_into_database(df):
    print("Inserting data into the database...")

    # List of columns that should be inserted into the database (ensure it's 20 columns)
    columns = [
        'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
        'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code',
        'X Coordinate', 'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude'
    ]  # Note: Location column removed since it's not part of your table schema

    # Remove any extra columns that may be in the DataFrame
    df_clean = df[columns]

    # Convert DataFrame to a dictionary of records
    data = df_clean.to_dict(orient="records")

    # Set up the connection to the database
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    # Prepare the insert query with 20 placeholders (one for each column)
    insert_query = """
        INSERT INTO crime_incidents (
            case_number, date, block, iucr, primary_type, description, location_description,
            arrest, domestic, beat, district, ward, community_area, fbi_code,
            x_coordinate, y_coordinate, year, updated_on, latitude, longitude
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Insert data one by one using a for loop
    with connection.cursor() as cursor:
        for record in data:
            # Prepare values
            values = (
                record['Case Number'], 
                record['Date'], 
                record['Block'], 
                record['IUCR'], 
                record['Primary Type'], 
                record['Description'], 
                record['Location Description'], 
                int(record['Arrest']),  # Convert True/False to 1/0
                int(record['Domestic']),  # Convert True/False to 1/0
                record['Beat'], 
                record['District'], 
                record['Ward'], 
                record['Community Area'], 
                record['FBI Code'], 
                record['X Coordinate'], 
                record['Y Coordinate'], 
                record['Year'], 
                record['Updated On'], 
                float(record['Latitude']),  # Ensure compatibility with DECIMAL(9,6)
                float(record['Longitude'])  # Ensure compatibility with DECIMAL(9,6)
            )

            # Debugging: Print values to ensure correct number of columns
            print(f"Values being inserted: {values}")

            try:
                cursor.execute(insert_query, values)
            except Exception as e:
                print(f"Error inserting record: {e}")
        
        # Commit the transaction
        connection.commit()

    # Close the connection
    connection.close()
    print("Data insertion completed!")

# Main execution
if __name__ == "__main__":
    # Step 1: Database connection (for creating the table)
    engine = connect_to_db()

    # Step 2: Create table if not exists
    create_table_if_not_exists(engine)

    # Step 3: Load the dataset (only first 5 records)
    file_path = 'chicago_crime_20_new.xlsx'  # Replace with your file path
    df = load_excel_file(file_path)
    # print ("Going to Describe the Data")
    # description = df.describe().shape
    # print (description)
    # quit()
    # Step 4: Clean the dataset
    df = clean_data(df)

    # # Step 5: Insert data into the database (only for first 5 records)
    insert_into_database(df)

    print("Process completed successfully!")
