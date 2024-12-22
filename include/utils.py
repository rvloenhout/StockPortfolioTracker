def get_company_info(required_stocks, required_columns_dict):
    import yfinance as yf
    import pandas as pd
    import warnings
    from datetime import datetime

    # Extract column names from the dictionary keys (excluding ID, stock, and date)
    column_names = [column for column in required_columns_dict.keys() if column not in ["ID", "stock", "date"]]
    Company_Info_df = pd.DataFrame(columns=column_names)
    
    # List to store the stock data as rows
    data_rows = []
    
    for stock in required_stocks:
        temp_list = []
        company_info = yf.Ticker(stock).info
        
        # Gather the data for the current stock, but skip the ID, stock, and date columns
        for column in column_names:
            if column in company_info:
                temp_list.append(company_info[column])
            else:
                temp_list.append(pd.NA)
                print(f"Column '{column}' not found for stock '{stock}'")
        
        # Get the current date (without time)
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
        
        # Generate the ID (stock + date as a unique identifier)
        unique_id = f"{stock} {current_date}"
        
        # Insert the ID, stock, and date at the start of the list
        temp_list.insert(0, unique_id)  # Insert the unique ID at the start
        temp_list.insert(1, stock)  # Insert the stock symbol after ID
        temp_list.insert(2, current_date)  # Insert the date after stock
        
        data_rows.append(temp_list)
    
    # Create a DataFrame with the collected rows
    columns = ["ID", "Symbol", "Datetime"] + column_names
    Company_Info_df = pd.DataFrame(data_rows, columns=columns)
    
    return Company_Info_df

def store_dataframe_in_mysql(df, table_name, column_definitions, db_config):
    import mysql.connector

    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Create table query
    columns_with_types = ", ".join([f"{col} {dtype}" for col, dtype in column_definitions.items()])
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})"  # Create table if it does not exist
    cursor.execute(create_table_query)

    # Check existing columns in the table
    cursor.execute(f"DESCRIBE {table_name}")
    existing_columns = [column[0] for column in cursor.fetchall()]

    # Add missing/new columns if necessary
    for column, dtype in column_definitions.items():
        if column not in existing_columns:
            alter_query = f"ALTER TABLE {table_name} ADD COLUMN {column} {dtype}"
            print(f"Adding missing column: {column} with type {dtype}")
            cursor.execute(alter_query)

    # Insert data into the table
    placeholders = ", ".join(["%s"] * len(column_definitions))  # Placeholder for values
    insert_query = f"INSERT INTO {table_name} ({', '.join(column_definitions.keys())}) VALUES ({placeholders})"
    
    # Prepare for checking duplicates before inserting
    check_exists_query = f"SELECT COUNT(*) FROM {table_name} WHERE Symbol = %s AND Datetime = %s"

    #print(df.to_string())
    #print(column_definitions)

    for _, row in df.iterrows():
        symbol = row['Symbol']
        datetime = row['Datetime']
        
        print(f"Insert query: {insert_query}")
        print(f"Row values: {tuple(row)}")
        
        # Check if the record with the same Symbol and Datetime exists
        cursor.execute(check_exists_query, (symbol, datetime))
        exists = cursor.fetchone()[0] > 0

        if not exists:
            print("Inserting:", tuple(row))
            cursor.execute(insert_query, tuple(row))
        else:
            print(f"Record for Symbol {symbol} and Datetime {datetime} already exists, skipping insertion.")

    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

def get_price_history(startDate, endDate, required_stocks, required_columns, interval="1h"):
    import pandas as pd
    import yfinance as yf

    Price_History_df = pd.DataFrame(columns=required_columns)
    for stock in required_stocks:
        # Fetch the historical data for the stock
        price_history = yf.Ticker(stock).history(
            start=startDate.strftime('%Y-%m-%d'),
            end=endDate.strftime('%Y-%m-%d'),
            interval=interval,
            actions=False
        )
        price_history['Symbol'] = stock
        price_history = price_history.reset_index()

        # Ensure Datetime is properly formatted
        price_history['Datetime'] = price_history['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Create the ID column by combining Symbol and Datetime
        price_history['ID'] = price_history['Symbol'] + " " + price_history['Datetime']

        # Add the data to the result DataFrame
        Price_History_df = pd.concat([Price_History_df, price_history])

    return Price_History_df