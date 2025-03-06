import mysql.connector                                     # Import MySQL connector to connect to the database
import getpass                                             # Import getpass to secure login by hiding password input

# Function to create a new database
def create_database():
    db_name = input("Enter the name of the database to create: ")                    # Get database name from user
    try:
        cursor.execute(f"CREATE DATABASE {db_name}")                                 # Execute command to create the database
        print(f"Database {db_name} created successfully.")                           # Print success message
    except mysql.connector.Error as err:                                             # Handle error if database creation fails
        print(f"Failed to create database {db_name}. Error: {err}")  


# Function to create a table in a specific database
def create_table():
    db_name = input("Enter the name of the database to use: ")                      # Get database name from user
    try:
        cursor.execute(f"USE {db_name}")                                            # Switch to the given database
    except mysql.connector.Error as err:                                            # Handle error if database selection fails
        print(f"Failed to use database {db_name}. Error: {err}")
        return

    table_name = input("Enter the name of the table to create: ")                    # Get table name from user
    columns = []                                                                     # Initialize list to store column definitions
    while True:                                                                      # Loop to get multiple column definitions
        choice = input("Enter 'column' to add a column or 'done' to finish: ").strip().lower()  # User choice to add column or finish
        if choice == 'done':                                                         # Exit loop if user is done
            break
        elif choice == 'column':                                                     # If user chooses to add a column
            column_name = input("Enter the column name: ")                           # Get column name
            data_type = input("Enter the data type (e.g., VARCHAR(255), INT): ")     # Get data type
            primary_key = input("Is this column a primary key? (yes/no): ").strip().lower()  # Check if column is primary key
            auto_increment = ""                                                      # Initialize auto increment option
            if primary_key == 'yes':                                                 # If the column is a primary key
                auto_increment = input("Should this primary key auto increment? (yes/no): ").strip().lower()  # Check auto increment
                if auto_increment == 'yes':
                    columns.append(f"{column_name} {data_type} PRIMARY KEY AUTO_INCREMENT")  # Define primary key with auto increment
                else:
                    columns.append(f"{column_name} {data_type} PRIMARY KEY")         # Define primary key without auto increment
            else:
                columns.append(f"{column_name} {data_type}")                         # Define a normal column
        else:
            print("Invalid choice. Please enter 'column' or 'done'.")                # Handle invalid input

    columns_str = ", ".join(columns)                                                 # Convert column definitions list to a comma-separated string
    try:
        cursor.execute(f"CREATE TABLE {table_name} ({columns_str})")                 # Execute query to create table
        print(f"Table {table_name} created successfully in database {db_name}.")     # Print success message
    except mysql.connector.Error as err:                                             # Handle error if table creation fails
        print(f"Failed to create table {table_name}. Error: {err}")


# Function to insert data into a table
def insert_data():
    db_name = input("Enter the name of the database to use: ")                      # Get database name
    try:
        cursor.execute(f"USE {db_name}")                                            # Switch to the selected database
    except mysql.connector.Error as err:                                            # Handle error if database selection fails
        print(f"Failed to use database {db_name}. Error: {err}")                        
        return

    table_name = input("Enter the name of the table to insert data into: ")          # Get table name
    try:
        cursor.execute(f"DESCRIBE {table_name}")                                     # Get table structure
        columns_info = cursor.fetchall()                                             # Fetch column details
    except mysql.connector.Error as err:                                             # Handle error if describing table fails
        print(f"Failed to describe table {table_name}. Error: {err}")
        return

    columns = [column[0] for column in columns_info]                                # Extract column names from table description
    print("Columns in the table:", ", ".join(columns))                              # Display available columns

    columns_input = input(f"Enter the columns from the above list (e.g., {', '.join(columns)}): ")  # Get columns to insert data into
    values = input("Enter the values (e.g., 'John', 30): ")                                 # Get corresponding values
    try:
        cursor.execute(f"INSERT INTO {table_name} ({columns_input}) VALUES ({values})")     # Execute insert query
        dataBase.commit()                                                                  # Commit the transaction
        print(f"Data inserted successfully into table {table_name}.")                       # Print success message
    except mysql.connector.Error as err:                                                    # Handle error if data insertion fails
        print(f"Failed to insert data into table {table_name}. Error: {err}")

# Function to update data in a specific table
def update_data():
    db_name = input("Enter the name of the database to use: ")                              # Get database name
    try:
        cursor.execute(f"USE {db_name}")                                                    # Switch to the specified database
    except mysql.connector.Error as err:                                                    # Handle database selection error
        print(f"Failed to use database {db_name}. Error: {err}")  
        return                                                                              # Exit the function if database selection fails

    table_name = input("Enter the name of the table to update data in: ")                   # Get table name
    try:
        cursor.execute(f"DESCRIBE {table_name}")                                            # Get table structure
        columns_info = cursor.fetchall()                                                    # Fetch column details
    except mysql.connector.Error as err:                                                    # Handle error if table description fails
        print(f"Failed to describe table {table_name}. Error: {err}")
        return                                                                              # Exit the function if description fails

    columns = [column[0] for column in columns_info]                                        # Extract column names
    print("Columns in the table:", ", ".join(columns))                                      # Display available columns

    set_clause = input("Enter the SET clause (e.g., name='John'): ")                        # Get update clause
    where_clause = input("Enter the WHERE clause (e.g., id=1): ")                           # Get condition clause
    try:
        cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}")        # Execute update query
        dataBase.commit()                                                                   # Commit the transaction
        print(f"Data updated successfully in table {table_name}.")                          # Confirm update
    except mysql.connector.Error as err:                                                    # Handle errors in query execution
        print(f"Failed to update data in table {table_name}. Error: {err}")

# Function to delete data from a specific table
def delete_data():
    db_name = input("Enter the name of the database to use: ")                              # Get database name
    try:
        cursor.execute(f"USE {db_name}")                                                    # Switch to the specified database
    except mysql.connector.Error as err:                                                    # Handle database selection error
        print(f"Failed to use database {db_name}. Error: {err}")  
        return                                                                              # Exit the function if database selection fails

    table_name = input("Enter the name of the table to delete data from: ")                 # Get table name
    try:
        cursor.execute(f"DESCRIBE {table_name}")                                            # Get table structure
        columns_info = cursor.fetchall()                                                    # Fetch column details
    except mysql.connector.Error as err:                                                    # Handle error if table description fails
        print(f"Failed to describe table {table_name}. Error: {err}")
        return                                                                              # Exit the function if description fails

    columns = [column[0] for column in columns_info]                                        # Extract column names
    print("Columns in the table:", ", ".join(columns))                                      # Display available columns

    where_clause = input("Enter the WHERE clause (e.g., id=1): ")                           # Get condition clause
    try:
        cursor.execute(f"DELETE FROM {table_name} WHERE {where_clause}")                    # Execute delete query
        dataBase.commit()                                                                   # Commit the transaction
        print(f"Data deleted successfully from table {table_name}.")                        # Confirm deletion
    except mysql.connector.Error as err:                                                    # Handle errors in query execution
        print(f"Failed to delete data from table {table_name}. Error: {err}")

# Function to select and display data from a specific table
def select_data():
    db_name = input("Enter the name of the database to use: ")                              # Get database name
    try:
        cursor.execute(f"USE {db_name}")                                                    # Switch to the specified database
    except mysql.connector.Error as err:                                                    # Handle error if database selection fails
        print(f"Failed to use database {db_name}. Error: {err}")
        return                                                                              # Exit function if database selection fails

    table_name = input("Enter the name of the table to select data from: ")                 # Get table name
    try:
        cursor.execute(f"DESCRIBE {table_name}")                                            # Get table structure
        columns_info = cursor.fetchall()                                                    # Fetch column details
    except mysql.connector.Error as err:                                                    # Handle error if table description fails
        print(f"Failed to describe table {table_name}. Error: {err}")
        return                                                                              # Exit function if table description fails

    columns = [column[0] for column in columns_info]                                         # Extract column names
    print("Columns in the table:", ", ".join(columns))                                       # Display available columns

    columns_input = input(f"Enter the columns to select (e.g., * or {', '.join(columns)}): ")  # Get columns to retrieve
    try:
        cursor.execute(f"SELECT {columns_input} FROM {table_name}")                          # Execute select query
        results = cursor.fetchall()                                                          # Fetch query results
        for row in results:                                                                  # Iterate through results
            print(row)                                                                       # Print each row
    except mysql.connector.Error as err:                                                     # Handle errors in query execution
        print(f"Failed to select data from table {table_name}. Error: {err}")

# Function to display all available databases
def show_databases():
    try:
        cursor.execute("SHOW DATABASES")                                                    # Execute query to list databases
        databases = cursor.fetchall()                                                       # Fetch all database names
        print("Databases:")                                                                 # Display header
        for db in databases:                                                                # Iterate through database list
            print(db[0])                                                                    # Print each database name
    except mysql.connector.Error as err:                                                    # Handle errors in query execution
        print(f"Failed to show databases. Error: {err}")

# Function to display all tables in a selected database
def show_tables():
    show_databases()                                                                        # Call function to list available databases
    db_name = input("Enter the name of the database to use: ")                              # Get database name
    try:
        cursor.execute(f"USE {db_name}")                                                    # Switch to the specified database
    except mysql.connector.Error as err:                                                    # Handle error if database selection fails
        print(f"Failed to use database {db_name}. Error: {err}")
        return                                                                              # Exit function if database selection fails
    
    try:
        cursor.execute("SHOW TABLES")                                                       # Execute query to list tables in the database
        tables = cursor.fetchall()                                                          # Fetch all table names
        print(f"Tables in database {db_name}:")                                             # Display header with database name
        for table in tables:                                                                # Iterate through table list
            print(table[0])                                                                 # Print each table name
    except mysql.connector.Error as err:                                                    # Handle errors in query execution
        print(f"Failed to show tables. Error: {err}")


while True:  # Infinite loop to repeatedly ask for login credentials until successful
    # Asking for user input
    username = input("Enter MySQL username: ")                                              # Prompt user for MySQL username
    password = getpass.getpass("Enter MySQL password: ")                                    # Securely prompt for password

    try:
        # Attempting to connect to MySQL
        dataBase = mysql.connector.connect(
            host="localhost",                                                               # Connecting to the local MySQL server
            user=username,                                                                  # Using the provided username
            passwd=password                                                                 # Using the provided password
        )
        
        cursor = dataBase.cursor()                                                          # Creating a cursor object to interact with the database
        
        # Menu
        print("Welcome! Connection successful.")                                            # Confirming successful connection
        while True:                                                                         # Infinite loop to keep displaying the menu until the user exits
            # Displaying the options menu
            print("---------------------------------")                                      # Displaying a separator
            print("Menu:")                                                                  # Displaying the menu options
            print("1: Create DataBase")                                                     # Option to create a new database
            print("2: Create Table")                                                        # Option to create a new table
            print("3: Insert")                                                              # Option to insert data into a table
            print("4: Update")                                                              # Option to update existing data
            print("5: Delete")                                                              # Option to delete data
            print("6: Select")                                                              # Option to retrieve and display data
            print("7: Show Databases")                                                      # Option to list all databases
            print("8: Show Tables")                                                         # Option to list tables in a selected database
            print("9: Exit")                                                                # Option to exit the program

            choice = input("Enter your choice: ")                                           # Getting user input for menu selection

            if choice == '1':                                                               # If user chooses 1, call function to create a database
                create_database()
            elif choice == '2':                                                             # If user chooses 2, call function to create a table
                create_table()
            elif choice == '3':                                                             # If user chooses 3, call function to insert data
                insert_data()
            elif choice == '4':                                                             # If user chooses 4, call function to update data
                update_data()
            elif choice == '5':                                                             # If user chooses 5, call function to delete data
                delete_data()
            elif choice == '6':                                                             # If user chooses 6, call function to select and display data
                select_data()
            elif choice == '7':                                                             # If user chooses 7, call function to show databases
                show_databases()
            elif choice == '8':                                                             # If user chooses 8, call function to show tables in a database
                show_tables()
            elif choice == '9':                                                             # If user chooses 9, exit the program
                print("Exiting...")                                                         # Notify user of exit
                dataBase.close()                                                            # Close the database connection
                break                                                                       # Exit the menu loop
            else:
                print("Invalid choice. Please try again.")                                  # Handle invalid input

    except mysql.connector.Error as err:                                                    # Catch any MySQL connection errors
        print("Wrong username or password! Please try again.", err)                         # Inform user of login failure
