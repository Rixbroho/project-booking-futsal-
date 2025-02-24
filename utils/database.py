import sqlite3
import hashlib
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_file = "futsal_booking.db"
        self.initialize_database()

    def initialize_database(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create bookings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    location TEXT NOT NULL,
                    game TEXT NOT NULL,
                    customer_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    UNIQUE(date, time, location)
                )
            ''')
            
            conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, full_name, email):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                hashed_password = self.hash_password(password)
                cursor.execute('''
                    INSERT INTO users (username, password, full_name, email)
                    VALUES (?, ?, ?, ?)
                ''', (username, hashed_password, full_name, email))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, password, full_name FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            
            if result and result[1] == self.hash_password(password):
                return {'id': result[0], 'full_name': result[2]}
        return None

    def add_booking(self, user_id, date, time, location, game, customer_name):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO bookings (user_id, date, time, location, game, customer_name)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, date, time, location, game, customer_name))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def get_bookings(self, user_id=None):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            if user_id:
                cursor.execute('''
                    SELECT date, time, location, game, customer_name
                    FROM bookings
                    WHERE user_id = ?
                    ORDER BY date, time
                ''', (user_id,))
            else:
                cursor.execute('''
                    SELECT date, time, location, game, customer_name
                    FROM bookings
                    ORDER BY date, time
                ''')
            
            bookings = {}
            for row in cursor.fetchall():
                date, time, location, game, customer_name = row
                if date not in bookings:
                    bookings[date] = {}
                bookings[date][time] = {
                    'location': location,
                    'game': game,
                    'customer_name': customer_name
                }
            return bookings

    def cancel_booking(self, date, time):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM bookings
                WHERE date = ? AND time = ?
            ''', (date, time))
            conn.commit()
            return cursor.rowcount > 0