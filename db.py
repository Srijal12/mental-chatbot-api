import sqlite3

conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# DROP old tables (clean start)
cursor.execute("DROP TABLE IF EXISTS admin")
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS templates")
cursor.execute("DROP TABLE IF EXISTS keywords")
cursor.execute("DROP TABLE IF EXISTS sessions")
cursor.execute("DROP TABLE IF EXISTS chats")

# ADMIN
cursor.execute("""
CREATE TABLE admin (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password_hash TEXT,
    role TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# USERS
cursor.execute("""
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password_hash TEXT,
    is_anonymous BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# TEMPLATES
cursor.execute("""
CREATE TABLE templates (
    template_id INTEGER PRIMARY KEY AUTOINCREMENT,
    emotion_type TEXT,
    response_text TEXT,
    category TEXT
)
""")

# KEYWORDS
cursor.execute("""
CREATE TABLE keywords (
    keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword_text TEXT,
    severity_level TEXT
)
""")

# SESSIONS
cursor.execute("""
CREATE TABLE sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    start_time TIMESTAMP,
    end_time TIMESTAMP
)
""")

# CHATS
cursor.execute("""
CREATE TABLE chats (
    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    message_text TEXT,
    emotion_label TEXT,
    sentiment_score FLOAT,
    is_crisis_flag BOOLEAN,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# INSERT DATA

# Templates
cursor.execute("INSERT INTO templates VALUES (NULL,'sad','I am here for you 💙','normal')")
cursor.execute("INSERT INTO templates VALUES (NULL,'stress','Take a deep breath. You are doing your best 🌿','coping')")
cursor.execute("INSERT INTO templates VALUES (NULL,'neutral','I understand how you feel 💙','general')")

# Keywords
crisis_words = [
    "die", "died", "want to die", "wanna die",
    "kill myself", "suicide", "end my life"
]

for word in crisis_words:
    cursor.execute("INSERT INTO keywords VALUES (NULL,?, 'high')", (word,))

conn.commit()
conn.close()

print("Database ready ")