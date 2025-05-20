import os
import sqlite3
import re
from pathlib import Path
from tqdm.auto import tqdm

def find_db_files(directory):
    """Find all SQLite database files in the given directory."""
    db_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.db') or file.endswith('.sqlite'):
                db_files.append(os.path.join(root, file))
    return db_files

def safe_connect(db_path):
    """Connect to a database with fallback options if it fails."""
    try:
        # First try normal connection
        conn = sqlite3.connect(db_path)
        return conn, "normal"
    except sqlite3.OperationalError:
        try:
            # Try read-only mode if normal fails
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            return conn, "readonly"
        except:
            print(f"Could not connect to {db_path}")
            return None, "failed"

def get_all_tables(conn):
    """Get all table names from a database, excluding obvious system tables."""
    try:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall() 
                 if not row[0].startswith('sqlite_') and 
                    not row[0].startswith('_')]
        return tables
    except Exception as e:
        print(f"Error getting tables: {e}")
        return []

def get_table_row_count(conn, table_name):
    """Get row count for a table, handling special characters in table names."""
    try:
        # Properly quote table name to handle spaces and special chars
        quoted_name = f'"{table_name}"'
        cursor = conn.execute(f"SELECT COUNT(*) FROM {quoted_name};")
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error counting rows in {table_name}: {e}")
        return 0

def fix_create_statement(sql):
    """Fix CREATE TABLE statement to be compatible with SQLite."""
    if not sql:
        return None
        
    # Convert to string if it's bytes
    if isinstance(sql, bytes):
        try:
            sql = sql.decode('utf-8')
        except UnicodeDecodeError:
            sql = sql.decode('latin-1', errors='replace')
    
    # Replace square brackets with double quotes
    sql = re.sub(r'\[([^\]]+)\]', r'"\1"', sql)
    
    # Fix any other syntax issues
    sql = sql.replace('IDENTITY', '')  # Remove SQL Server IDENTITY
    sql = re.sub(r'DEFAULT\s+NEWID\(\)', 'DEFAULT NULL', sql)  # Replace NEWID()
    
    return sql

def copy_table_schema(src_conn, dest_conn, table_name, new_table_name):
    """Copy table schema with fixes for compatibility."""
    try:
        # Get the CREATE statement
        cursor = src_conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", 
            (table_name,))
        result = cursor.fetchone()
        if not result or not result[0]:
            print(f"No CREATE statement found for {table_name}")
            return False
            
        create_sql = fix_create_statement(result[0])
        if not create_sql:
            return False
            
        # Replace the original table name with the new one
        pattern = re.compile(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(["\']?)(\w+|`.+?`|\[.+?\]|".+?")(["\']?)', 
                            re.IGNORECASE)
        
        def replacer(match):
            return f'CREATE TABLE "{new_table_name}"'
            
        new_create_sql = pattern.sub(replacer, create_sql, count=1)
        
        # Execute the modified CREATE statement
        dest_conn.execute(new_create_sql)
        return True
    except Exception as e:
        print(f"Error copying schema for {table_name}: {e}")
        return False

def safe_fetch_data(conn, table_name, limit=1000):
    """Fetch data from a table, handling encoding and other issues."""
    try:
        quoted_name = f'"{table_name}"'
        cursor = conn.execute(f"SELECT * FROM {quoted_name} LIMIT {limit};")
        rows = cursor.fetchall()
        return rows, cursor.description
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print(f"Table {table_name} doesn't exist")
            return None, None
        elif "UTF-8" in str(e):
            # Try with bytes mode for encoding issues
            conn.text_factory = bytes
            try:
                cursor = conn.execute(f"SELECT * FROM {quoted_name} LIMIT {limit};")
                rows = cursor.fetchall()
                return rows, cursor.description
            except Exception as inner_e:
                print(f"Error fetching data with bytes mode: {inner_e}")
                return None, None
        else:
            print(f"Error fetching data: {e}")
            return None, None
    except Exception as e:
        print(f"Unexpected error fetching data: {e}")
        return None, None

def decode_value(val):
    """Decode a value from bytes if needed."""
    if isinstance(val, bytes):
        try:
            return val.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return val.decode('latin-1')
            except Exception:
                return val.decode('utf-8', errors='replace')
    return val

def copy_table_data(src_conn, dest_conn, table_name, new_table_name, row_limit=1000):
    """Copy data from source to destination table with proper handling of encoding."""
    rows, description = safe_fetch_data(src_conn, table_name, row_limit)
    if not rows or not description:
        return False
        
    try:
        # Decode values if they're bytes
        decoded_rows = []
        for row in rows:
            decoded_row = tuple(decode_value(val) for val in row)
            decoded_rows.append(decoded_row)
            
        # Insert the data
        placeholders = ','.join(['?'] * len(description))
        insert_sql = f'INSERT INTO "{new_table_name}" VALUES ({placeholders})'
        dest_conn.executemany(insert_sql, decoded_rows)
        return True
    except Exception as e:
        print(f"Error copying data for {table_name}: {e}")
        return False

def extract_tables_to_db(directory, output_db_path, min_rows=5, row_limit=1000):
    """Extract tables from all databases in directory to a single output database."""
    # Find all database files
    db_files = find_db_files(directory)
    print(f"Found {len(db_files)} database files")
    
    # Create output database
    dest_conn = sqlite3.connect(output_db_path)
    
    # Count tables that meet criteria
    total_tables = 0
    tables_info = []
    
    print("Scanning databases for tables...")
    for db_file in db_files:
        src_conn, mode = safe_connect(db_file)
        if not src_conn:
            continue
            
        db_name = Path(db_file).stem
        tables = get_all_tables(src_conn)
        
        for table in tables:
            row_count = get_table_row_count(src_conn, table)
            if row_count >= min_rows:
                total_tables += 1
                tables_info.append((db_file, table, row_count))
                
        src_conn.close()
    
    print(f"Found {total_tables} tables with at least {min_rows} rows")
    
    # Process tables with progress bar
    successful = 0
    with tqdm(total=total_tables, desc="Extracting Tables") as pbar:
        for db_file, table, row_count in tables_info:
            src_conn, mode = safe_connect(db_file)
            if not src_conn:
                pbar.update(1)
                continue
                
            db_name = Path(db_file).stem
            new_table_name = f"{db_name}__{table}"
            
            # Copy schema and data
            schema_ok = copy_table_schema(src_conn, dest_conn, table, new_table_name)
            if schema_ok:
                data_ok = copy_table_data(src_conn, dest_conn, table, new_table_name, row_limit)
                if data_ok:
                    successful += 1
                    dest_conn.commit()  # Commit after each successful table
                    
            src_conn.close()
            pbar.set_postfix({"Table": new_table_name[:20], "Rows": min(row_count, row_limit)})
            pbar.update(1)
    
    print(f"Successfully extracted {successful} out of {total_tables} tables")
    print(f"Output database: {output_db_path}")
    dest_conn.close()
    return True

# Set your directory and output path
# directory = r"C:\path\to\your\databases"
# output_db_path = "DataLake.sqlite"
# extract_tables_to_db(directory, output_db_path, min_rows=4, row_limit=1000)

