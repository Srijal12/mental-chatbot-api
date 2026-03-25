import os

if not os.path.exists("chatbot.db"):
    import db

from fastapi import FastAPI, Header, HTTPException
import sqlite3

app = FastAPI()

API_KEY = "mental123"


@app.get("/")
def home():
    return {"message": "API is running 🚀"}


@app.post("/chat")
def chat(user_id: int, message: str, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    # ======================
    # SESSION MANAGEMENT
    # ======================
    cursor.execute("""
    SELECT session_id FROM sessions
    WHERE user_id=? AND end_time IS NULL
    ORDER BY session_id DESC LIMIT 1
    """, (user_id,))

    session = cursor.fetchone()

    if session:
        session_id = session[0]
    else:
        cursor.execute("""
        INSERT INTO sessions (user_id, start_time)
        VALUES (?, datetime('now'))
        """, (user_id,))
        session_id = cursor.lastrowid

    # ======================
    # TEXT PROCESSING
    # ======================
    message_lower = message.lower()

    # ======================
    # CRISIS DETECTION
    # ======================
    cursor.execute("SELECT keyword_text FROM keywords")
    keywords = [k[0] for k in cursor.fetchall()]

    extra_words = ["wanna die"]
    all_keywords = keywords + extra_words

    is_crisis = any(word in message_lower for word in all_keywords)

    # ======================
    # EMOTION DETECTION
    # ======================
    emotion_map = {
        "sad": ["sad", "cry", "depressed"],
        "stress": ["stress", "tension", "pressure"]
    }

    emotion = "neutral"

    for key, words in emotion_map.items():
        for word in words:
            if word in message_lower:
                emotion = key
                break

    # ======================
    # RESPONSE LOGIC
    # ======================
    if is_crisis:
        response = (
            "I'm really sorry you're feeling this way 💙\n"
            "You are not alone. Please talk to someone you trust.\n"
            "Helpline (India): 9152987821"
        )
    else:
        cursor.execute(
            "SELECT response_text FROM templates WHERE emotion_type=?",
            (emotion,)
        )
        result = cursor.fetchone()

        if result:
            response = result[0]
        else:
            response = "I understand how you feel 💙"

    # ======================
    # STORE CHAT
    # ======================
    cursor.execute("""
    INSERT INTO chats 
    (session_id, message_text, emotion_label, sentiment_score, is_crisis_flag)
    VALUES (?, ?, ?, ?, ?)
    """, (session_id, message, emotion, 0.5, is_crisis))

    conn.commit()
    conn.close()

    return {
        "user_id": user_id,
        "session_id": session_id,
        "emotion": emotion,
        "crisis": is_crisis,
        "response": response
    }
