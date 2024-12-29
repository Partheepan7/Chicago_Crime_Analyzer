# README: Crime Data Analysis and Dashboard Project

## Project Overview
This project involves analyzing crime data to uncover actionable insights and trends for law enforcement and policymakers. The analysis cleanses and processes raw data from an Excel file, saves the cleaned data to a new file, and uses the processed dataset to create a Power BI dashboard for visualization.

## Steps to Execute the Project

### Step 1: Data Loading
The raw data is loaded from an Excel file (`chicago_crime_20_new.xlsx`) into a Pandas DataFrame using Python.

**Key Operations:**
- Load all records from the Excel file for analysis.
- Print the first few rows of the data for validation.

### Step 2: Data Cleaning
The cleaning process ensures the dataset is accurate, consistent, and ready for analysis. The cleaning operations include:

1. **Date Standardization:**
   - Converts the `Date` and `Updated On` columns to a uniform datetime format for consistency.

2. **Handling Missing Values:**
   - Replaces missing values in `X Coordinate` and `Y Coordinate` with the mean of the respective columns to retain spatial information.
   - Fills missing values in `FBI Code` with "Unknown" to categorize uncoded crimes.
   - Fills missing `Community Area` and `Ward` values with `0`, indicating unclassified areas.

3. **Text Standardization:**
   - Standardizes text columns such as `Primary Type`, `Description`, and `Location Description` to title case for uniformity.
   - Replaces placeholders (e.g., "XX") in the `Block` column with "00" to improve address clarity.

4. **Coordinate Validation:**
   - Ensures latitude and longitude values fall within Chicago’s geographical boundaries.

5. **Duplicate Removal:**
   - Drops duplicate rows based on unique identifiers (`ID` and `Case Number`) to maintain data integrity.

6. **Location Reconstruction:**
   - Constructs a `Location` column using latitude and longitude values for geographic analysis.

### Step 3: Saving Cleaned Data
The cleaned dataset is saved to a new Excel file (`cleaned_chicago_crime.xlsx`) for further use.

**Key Features:**
- Data is saved in a structured format with a sheet named `Cleaned Data`.
- Ensures compatibility for external tools like Power BI.

### Step 4: Dashboard Creation
Using Power BI, a dashboard is built to visualize insights from the cleaned data. The dashboard includes:

1. **Crime Hotspots:**
   - A heatmap highlights locations with the highest crime density.
2. **Trend Analysis:**
   - Line and bar charts show crime trends by time (hour, day, month, year).
3. **Arrest Analysis:**
   - A donut chart visualizes arrest rates across crime types.
4. **Geographic Overview:**
   - A table lists community areas and their respective crime counts.
5. **Safety Rankings:**
   - A score or ranking for neighborhood safety is displayed.

## Requirements
### Software:
- Python 3.8 or higher
- Power BI Desktop
- Excel

### Libraries:
- pandas
- openpyxl

### Files:
- Input: `chicago_crime_20_new.xlsx`
- Output: `cleaned_chicago_crime.xlsx`

## How to Run the Project
1. Place the raw Excel file (`chicago_crime_20_new.xlsx`) in the working directory.
2. Execute the Python script to clean the data and generate the cleaned Excel file.
   ```bash
   python clean_crime_data.py
   ```
3. Open Power BI Desktop and load `cleaned_chicago_crime.xlsx` as the data source.
4. Customize the visuals to explore insights or use the provided dashboard template.

## Insights from Analysis
1. **Crime Patterns:**
   - Identify peak crime hours and seasonal trends.
2. **Hotspots:**
   - Highlight high-crime areas for targeted interventions.
3. **Arrest Rates:**
   - Evaluate law enforcement efficiency across crime categories.
4. **Safety Scores:**
   - Inform residents and policymakers about community safety.

## Future Enhancements
- Automate dashboard updates with real-time data.
- Use machine learning for predictive crime modeling.
- Integrate crime data APIs for dynamic analysis.

## Conclusion
This project demonstrates a comprehensive approach to analyzing crime data and presenting actionable insights through a user-friendly Power BI dashboard. It equips stakeholders with the tools needed for informed decision-making and effective crime prevention strategies.
