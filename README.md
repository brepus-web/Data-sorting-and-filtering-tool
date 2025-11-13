# Data Sorting and Filtering Tool

A powerful Streamlit web application for sorting, filtering, and analyzing data files.

## Features

### File Upload
- Support for CSV and Excel files (.csv, .xls, .xlsx)
- Automatic handling of empty rows and columns
- Robust error handling for file reading

### Data Filtering
- **Column Filtering**: Select specific columns to include in your analysis
- **Redundant Data Filtering**: Identify and remove duplicate values with multiple options:
  - Keep first occurrence
  - Keep last occurrence  
  - Remove all duplicates entirely
- **Character-Based Filtering**:
  - Remove specific characters from columns
  - Keep only specified characters in columns
  - Keep rows containing specific characters

### Sorting Options
- **Alphanumeric Sorting**: Smart sorting that handles mixed numbers and text
- **Text Sorting**: Alphabetical sorting with case insensitivity
- **Number Sorting**: Proper numerical sorting
- **Direction Control**: Ascending or descending order

### Data Visualization
- **Line Charts**: Trend analysis between two columns
- **Scatter Plots**: Correlation visualization
- **Bar Charts**: Comparative analysis
- Real-time chart updates based on filtered data

### Export Options
- Download filtered and sorted data as CSV
- Download filtered and sorted data as Excel (XLSX)
- Preserves data integrity and formatting

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Method 1: Simple Run (Recommended)
1. Download `main.py` to your computer
2. Open terminal/command prompt in the same folder
3. Run: `streamlit run main.py`
4. The app will open in your browser automatically

### Method 2: With Virtual Environment
```bash
# Create virtual environment (optional)
python -m venv data_env
source data_env/bin/activate  # On Windows: data_env\Scripts\activate

# Install required packages
pip install streamlit pandas openpyxl

# Run the app
streamlit run main.py
```

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.