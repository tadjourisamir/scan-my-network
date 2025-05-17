import sqlite3

DB_NAME = 'scanner.db'

# Expected columns and their SQLite types
COLUMNS = {
    "name": "TEXT",
    "type": "TEXT",
    "ip": "TEXT NOT NULL",
    "mac": "TEXT UNIQUE",  # ✅ Must be UNIQUE
    "vlan": "INTEGER",
    "location": "TEXT",
    "status": "TEXT NOT NULL",
    "scan_time": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Step 1 — Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scanned_devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    ''')

    # Step 2 — Get existing columns
    cursor.execute("PRAGMA table_info(scanned_devices)")
    existing_columns = {col[1] for col in cursor.fetchall()}

    # Step 3 — Add missing columns (handling UNIQUE constraints separately)
    for column, column_type in COLUMNS.items():
        if column not in existing_columns:
            if "UNIQUE" in column_type:
                base_type = column_type.replace("UNIQUE", "").strip()
                print(f"➕ Adding column: {column} (without constraint, index added separately)")
                cursor.execute(f"ALTER TABLE scanned_devices ADD COLUMN {column} {base_type}")
                cursor.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{column} ON scanned_devices({column})")
            else:
                print(f"➕ Adding column: {column}")
                cursor.execute(f"ALTER TABLE scanned_devices ADD COLUMN {column} {column_type}")

    conn.commit()
    conn.close()
