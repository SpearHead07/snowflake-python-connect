# Import necessary libraries for environment variables, Snowflake connection, and file path handling
import os
from pathlib import Path

import snowflake.connector
from dotenv import load_dotenv

# Load environment variables from .env file in the script's directory
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

def get_connection():
    # Retrieve Snowflake connection credentials from environment variables
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    database = os.getenv("SNOWFLAKE_DATABASE")
    schema = os.getenv("SNOWFLAKE_SCHEMA")
    role = os.getenv("SNOWFLAKE_ROLE")

    # Check for missing required environment variables
    missing = [k for k,v in {
        "SNOWFLAKE_ACCOUNT": account,
        "SNOWFLAKE_USER": user,
        "SNOWFLAKE_PASSWORD": password,
        "SNOWFLAKE_WAREHOUSE": warehouse,
        "SNOWFLAKE_DATABASE": database,
        "SNOWFLAKE_SCHEMA": schema,
        "SNOWFLAKE_ROLE": role,
    }.items() if not v]

    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    # Establish and return a Snowflake database connection
    return snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role,
    )


def run_query(sql, params=None, fetch="all"):
    # Execute SQL query on Snowflake and return results with metadata
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            query_id = cur.sfqid

            # Return empty result set for non-SELECT queries
            if cur.description is None:
                return {"query_id": query_id, "rows": [], "columns": []}

            # Extract column names from query result metadata
            columns = [col[0] if isinstance(col, tuple) else col.name for col in cur.description]

            # Retrieve rows based on fetch parameter (one, many, or all)
            if fetch == "one":
                rows = cur.fetchone()
            elif fetch == "many":
                rows = cur.fetchmany(10)
            else:
                rows = cur.fetchall()

            return {"query_id": query_id, "columns": columns, "rows": rows}
    finally:
        # Always close the connection to release resources
        conn.close()

def format_table(columns, rows):
    # Format query results into a readable ASCII table string
    if not rows:
        return "Rows: []"

    # Calculate column widths based on header and data content
    col_widths = [len(str(col)) for col in columns]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    # Build table header, separator, and data rows with proper alignment
    header = " | ".join(str(col).ljust(col_widths[i]) for i, col in enumerate(columns))
    sep = "-+-".join("-" * w for w in col_widths)
    body_lines = [header, sep]

    # Format each data row with consistent column spacing
    for row in rows:
        line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        body_lines.append(line)

    return "\n".join(body_lines)


def main():
    # Create Streamlit web UI for Snowflake SQL query execution
    import streamlit as st
    import pandas as pd

    # Configure Streamlit page setup with title and icon
    st.set_page_config(page_title="Snowflake SQL Runner", page_icon="❄️", layout="wide")
    st.title("Snowflake SQL Runner")
    st.write("Enter SQL in the box below and click Run to execute against Snowflake.")

    # Create UI elements: text area for SQL input and button to execute
    query = st.text_area("SQL query", value="SELECT CURRENT_TIMESTAMP(), CURRENT_USER()", height=120)
    run = st.button("Run")

    # Execute query and display results when Run button is clicked
    if run:
        if not query.strip():
            st.error("Please enter a SQL query.")
        else:
            try:
                # Show spinner while executing query and fetch results
                with st.spinner("Executing query..."):
                    result = run_query(query)

                # Display query ID and results in both dataframe and text formats
                st.success(f"Query ID: {result['query_id']}")

                if not result["rows"]:
                    st.info("No rows returned.")
                else:
                    # Show results as interactive Pandas dataframe
                    df = pd.DataFrame(result["rows"], columns=result["columns"])
                    st.dataframe(df)

                    # Also display results as formatted ASCII table
                    st.markdown("**Result Table (text)**")
                    st.text(format_table(result["columns"], result["rows"]))

            except Exception as exc:
                # Display any errors encountered during query execution
                st.error(f"Error: {exc}")


if __name__ == "__main__":
    main()
