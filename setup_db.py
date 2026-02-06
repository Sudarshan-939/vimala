import sqlite3
import datetime
import json

def create_connection():
    try:
        conn = sqlite3.connect('cine_rental.db')
        return conn
    except Exception as e:
        print(e)
    return None

def create_tables(conn):
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT,
        role TEXT DEFAULT 'user',
        phone TEXT,
        company TEXT,
        created_at TEXT
    )
    ''')

    # Equipment Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        price REAL NOT NULL,
        image TEXT,
        description TEXT,
        stock INTEGER DEFAULT 0,
        created_at TEXT,
        updated_at TEXT
    )
    ''')
    
    # Bookings Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id TEXT UNIQUE NOT NULL,
        customer_json TEXT NOT NULL,
        items_json TEXT NOT NULL,
        project_details_json TEXT NOT NULL,
        total_amount REAL NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TEXT,
        updated_at TEXT
    )
    ''')
    
    # Gallery Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS gallery (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_url TEXT NOT NULL
    )
    ''')
    
    # Contact Info Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contact_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        phone TEXT,
        email TEXT,
        hours TEXT
    )
    ''')
    
    conn.commit()
    print("Tables created successfully.")

def seed_data(conn):
    cursor = conn.cursor()
    
    # Seed Admin User
    cursor.execute("SELECT * FROM users WHERE email = 'vimala'")
    if not cursor.fetchone():
        cursor.execute('''
        INSERT INTO users (email, password, name, role, created_at)
        VALUES (?, ?, ?, ?, ?)
        ''', ('vimala', 'vimala', 'Vimala Admin', 'admin', datetime.datetime.now().isoformat()))
        print("Admin user seeded.")
        
    # Seed Contact Info
    cursor.execute("SELECT * FROM contact_info")
    if not cursor.fetchone():
        cursor.execute('''
        INSERT INTO contact_info (address, phone, email, hours)
        VALUES (?, ?, ?, ?)
        ''', ('123 Film Street, Mumbai, India', '+91 98765 43210', 'info@vimalaenterprises.com', 'Mon-Sat: 9AM-7PM'))
        print("Contact info seeded.")
        
    # Seed Gallery
    cursor.execute("SELECT * FROM gallery")
    if not cursor.fetchone():
        images = [
            'https://images.unsplash.com/photo-1594909122845-11baa439b7bf?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'https://images.unsplash.com/photo-1588681664899-f142ff2dc9b1?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'https://images.unsplash.com/photo-1591862719729-6e15bd642900?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'https://images.unsplash.com/photo-1571844307880-751c6d86f3f3?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'https://images.unsplash.com/photo-1563298258-c2c4df7b9070?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
        ]
        
        for img in images:
            cursor.execute("INSERT INTO gallery (image_url) VALUES (?)", (img,))
        print("Gallery images seeded.")

    # Seed Equipment
    cursor.execute("SELECT * FROM equipment")
    if not cursor.fetchone():
        equipment_list = [
            ("Sony FX6 Cinema Camera", "camera", 13500, "", "Full-frame cinema camera with advanced autofocus and 4K 120p recording", 5),
            ("ARRI SkyPanel S60-C", "light", 9000, "", "High-output LED soft light with full color spectrum control", 3),
            ("Canon C70 Cinema Camera", "camera", 11250, "", "Compact cinema camera with RF mount and dual gain output", 4),
            ("Kino Flo Celeb 200", "light", 6375, "", "LED fixture with high CRI and flicker-free operation", 7),
            ("Sigma 18-35mm T2 Cine Lens", "lens", 6750, "", "High-speed zoom lens with consistent T-stop throughout range", 2),
            ("Blackmagic Ursa Mini Pro 12K", "camera", 18750, "", "Professional cinema camera with 12K sensor and EF lens mount", 2)
        ]
        
        for item in equipment_list:
            cursor.execute('''
            INSERT INTO equipment (name, type, price, image, description, stock, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (item[0], item[1], item[2], item[3], item[4], item[5], datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat()))
        print("Equipment seeded.")
            
    conn.commit()

def main():
    conn = create_connection()
    if conn is not None:
        create_tables(conn)
        seed_data(conn)
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
