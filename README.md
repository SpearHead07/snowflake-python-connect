# Snowflake Python Connect

A Streamlit web application for executing SQL queries against Snowflake databases with a user-friendly interface.

## Features

- **SQL Query Execution**: Run SQL queries directly against your Snowflake warehouse
- **Environment-based Credentials**: Securely load connection credentials from environment variables
- **Result Visualization**: View results in both interactive dataframe and formatted ASCII table formats
- **Query Metadata**: Track query execution with Snowflake query IDs
- **Error Handling**: Comprehensive error reporting for debugging

## Prerequisites

- Python 3.8+
- Snowflake account with warehouse access
- Required packages: `snowflake-connector-python`, `streamlit`, `pandas`, `python-dotenv`

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Snowflake-Python-Connect.git
   cd Snowflake-Python-Connect
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root with the following variables:
   ```
   SNOWFLAKE_ACCOUNT=your_account_id
   SNOWFLAKE_USER=your_username
   SNOWFLAKE_PASSWORD=your_password
   SNOWFLAKE_WAREHOUSE=your_warehouse
   SNOWFLAKE_DATABASE=your_database
   SNOWFLAKE_SCHEMA=your_schema
   SNOWFLAKE_ROLE=your_role
   ```

5. **Run the application**:
   ```bash
   streamlit run Snowflake-Python-Connect.py
   ```

## Usage

1. Open the application in your browser (typically `http://localhost:8501`)
2. Enter your SQL query in the text area
3. Click **Run** to execute
4. View results in the interactive table or text format

## File Structure

- `Snowflake-Python-Connect.py` - Main Streamlit application
- `requirements.txt` - Python package dependencies
- `.env` - Environment variables (should not be committed)
- `.gitignore` - Git ignore rules

## Security

⚠️ **Important**: Never commit your `.env` file to version control. Keep your Snowflake credentials secure by:
- Using `.env` file for local development
- Using environment variables or secrets management in production

## License

MIT License - feel free to use this project for your own purposes.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.
