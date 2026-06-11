"""
数据库管理模块
包含所有数据库操作
"""

import sqlite3
import os
from datetime import datetime, date

DB_PATH = 'pets.db'

def init_database():
    """初始化数据库，创建所有表"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT CHECK(type IN ('cat', 'dog')),
        breed TEXT,
        birthday TEXT,
        gender TEXT CHECK(gender IN ('male', 'female')),
        avatar_path TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS vaccines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet_id INTEGER,
        vaccine_name TEXT,
        date TEXT,
        next_due TEXT,
        notes TEXT,
        FOREIGN KEY (pet_id) REFERENCES pets (id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS weight_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet_id INTEGER,
        weight REAL,
        date TEXT DEFAULT CURRENT_DATE,
        FOREIGN KEY (pet_id) REFERENCES pets (id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet_id INTEGER,
        title TEXT,
        due_date TEXT,
        type TEXT,
        is_completed INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pet_id) REFERENCES pets (id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS pet_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS foster_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet_id INTEGER,
        start_date TEXT NOT NULL,
        end_date TEXT,
        contact_name TEXT NOT NULL,
        contact_phone TEXT,
        contact_address TEXT,
        notes TEXT,
        status TEXT DEFAULT 'active',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pet_id) REFERENCES pets (id)
    )''')
    
    c.execute('INSERT OR IGNORE INTO pet_types (name, description) VALUES (?, ?)', ('猫', '猫咪'))
    c.execute('INSERT OR IGNORE INTO pet_types (name, description) VALUES (?, ?)', ('狗', '狗狗'))
    
    conn.commit()
    conn.close()

class PetDatabase:
    """宠物数据库操作类"""
    
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)
    
    @staticmethod
    def add_pet(name, pet_type, breed, birthday, gender, avatar_path=''):
        """添加新宠物"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO pets (name, type, breed, birthday, gender, avatar_path) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (name, pet_type, breed, birthday, gender, avatar_path))
        conn.commit()
        pet_id = c.lastrowid
        conn.close()
        return pet_id
    
    @staticmethod
    def get_all_pets():
        """获取所有宠物"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute("SELECT id, name, type, avatar_path FROM pets ORDER BY id DESC")
        pets = c.fetchall()
        conn.close()
        return pets
    
    @staticmethod
    def get_pet_by_id(pet_id):
        """根据ID获取宠物详情"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM pets WHERE id = ?", (pet_id,))
        pet = c.fetchone()
        conn.close()
        return pet
    
    @staticmethod
    def delete_pet(pet_id):
        """删除宠物及其所有关联记录"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
        c.execute("DELETE FROM vaccines WHERE pet_id = ?", (pet_id,))
        c.execute("DELETE FROM weight_records WHERE pet_id = ?", (pet_id,))
        c.execute("DELETE FROM reminders WHERE pet_id = ?", (pet_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def add_weight(pet_id, weight, record_date=None):
        """添加体重记录"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        if record_date:
            c.execute("INSERT INTO weight_records (pet_id, weight, date) VALUES (?, ?, ?)",
                      (pet_id, weight, record_date))
        else:
            today = date.today().isoformat()
            c.execute("INSERT INTO weight_records (pet_id, weight, date) VALUES (?, ?, ?)",
                      (pet_id, weight, today))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_weight_history(pet_id):
        """获取宠物体重历史"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute("SELECT date, weight FROM weight_records WHERE pet_id = ? ORDER BY date DESC LIMIT 10",
                  (pet_id,))
        records = c.fetchall()
        conn.close()
        return records
    
    @staticmethod
    def add_vaccine(pet_id, vaccine_name, vaccine_date, next_due, notes=''):
        """添加疫苗记录"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO vaccines (pet_id, vaccine_name, date, next_due, notes) 
                     VALUES (?, ?, ?, ?, ?)''',
                  (pet_id, vaccine_name, vaccine_date, next_due, notes))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_vaccines(pet_id):
        """获取宠物的疫苗记录"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute("SELECT id, vaccine_name, date, next_due, notes FROM vaccines WHERE pet_id = ? ORDER BY date DESC",
                  (pet_id,))
        vaccines = c.fetchall()
        conn.close()
        return vaccines
    
    @staticmethod
    def add_reminder(pet_id, title, due_date, reminder_type):
        """添加提醒"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO reminders (pet_id, title, due_date, type) 
                     VALUES (?, ?, ?, ?)''',
                  (pet_id, title, due_date, reminder_type))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_today_reminders():
        """获取今日提醒"""
        today = date.today().isoformat()
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute('''SELECT r.id, p.name, r.title, r.due_date, r.type 
                     FROM reminders r
                     JOIN pets p ON r.pet_id = p.id
                     WHERE r.due_date = ? AND r.is_completed = 0
                     ORDER BY r.due_date''', (today,))
        reminders = c.fetchall()
        conn.close()
        return reminders
    
    @staticmethod
    def complete_reminder(reminder_id):
        """标记提醒为已完成"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute("UPDATE reminders SET is_completed = 1 WHERE id = ?", (reminder_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete_reminder(reminder_id):
        """删除提醒"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all_reminders():
        """获取所有提醒"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute('''SELECT r.id, p.name, r.title, r.due_date, r.type, r.is_completed
                     FROM reminders r
                     JOIN pets p ON r.pet_id = p.id
                     ORDER BY r.due_date ASC''')
        reminders = c.fetchall()
        conn.close()
        return reminders
    
    @staticmethod
    def get_pet_statistics(pet_id):
        """获取宠物统计信息"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM vaccines WHERE pet_id = ?", (pet_id,))
        vaccine_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM weight_records WHERE pet_id = ?", (pet_id,))
        weight_count = c.fetchone()[0]
        
        c.execute("SELECT AVG(weight) FROM weight_records WHERE pet_id = ?", (pet_id,))
        avg_weight = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM reminders WHERE pet_id = ? AND is_completed = 0", (pet_id,))
        pending_reminders = c.fetchone()[0]
        
        conn.close()
        
        return {
            'vaccine_count': vaccine_count,
            'weight_count': weight_count,
            'avg_weight': round(avg_weight, 2) if avg_weight else 0,
            'pending_reminders': pending_reminders
        }
    
    @staticmethod
    def get_all_pet_types():
        """获取所有宠物种类"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute("SELECT id, name, description FROM pet_types ORDER BY id")
        types = c.fetchall()
        conn.close()
        return types
    
    @staticmethod
    def add_pet_type(name, description=''):
        """添加宠物种类"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO pet_types (name, description) VALUES (?, ?)', (name, description))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        conn.close()
        return success
    
    @staticmethod
    def delete_pet_type(type_id):
        """删除宠物种类"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute('DELETE FROM pet_types WHERE id = ?', (type_id,))
        conn.commit()
        affected = c.rowcount
        conn.close()
        return affected > 0
    
    @staticmethod
    def get_all_foster_records():
        """获取所有寄养记录"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute('''SELECT fr.id, p.name, fr.start_date, fr.end_date, 
                     fr.contact_name, fr.contact_phone, fr.contact_address, fr.notes, fr.status
                     FROM foster_records fr
                     JOIN pets p ON fr.pet_id = p.id
                     ORDER BY fr.start_date DESC''')
        records = c.fetchall()
        conn.close()
        return records
    
    @staticmethod
    def add_foster_record(pet_id, start_date, end_date, contact_name, contact_phone, contact_address, notes=''):
        """添加寄养记录"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO foster_records 
                     (pet_id, start_date, end_date, contact_name, contact_phone, contact_address, notes) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (pet_id, start_date, end_date, contact_name, contact_phone, contact_address, notes))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete_foster_record(record_id):
        """删除寄养记录"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        c.execute('DELETE FROM foster_records WHERE id = ?', (record_id,))
        conn.commit()
        affected = c.rowcount
        conn.close()
        return affected > 0
    
    @staticmethod
    def get_overall_stats():
        """获取整体统计信息"""
        conn = PetDatabase.get_connection()
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM pets")
        pet_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM vaccines")
        vaccine_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM weight_records")
        weight_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM reminders WHERE is_completed = 0")
        pending_reminders = c.fetchone()[0]
        
        c.execute("SELECT type, COUNT(*) FROM pets GROUP BY type")
        pet_types = c.fetchall()
        
        conn.close()
        
        return {
            'total_pets': pet_count,
            'total_vaccines': vaccine_count,
            'total_weights': weight_count,
            'pending_reminders': pending_reminders,
            'pet_types': pet_types
        }