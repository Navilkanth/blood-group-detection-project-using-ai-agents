import os
import sqlite3
import json
import numpy as np
from datetime import datetime
from backend.config import Config
from typing import Dict, Any, List
from pymongo import MongoClient

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        if isinstance(obj, (bool, np.bool_)): return bool(obj)
        return super(NpEncoder, self).default(obj)

class HybridDatabaseManager:
    """Handles MongoDB with automatic local SQLite fallback for reliability"""
    def __init__(self):
        self.mongo_client = None
        self.mongo_db = None
        self.mode = "PENDING"
        self.sqlite_path = "local_reports.db"
        
    def connect(self):
        # 1. Try MongoDB
        try:
            uri = Config.MONGODB_URI
            # Only try if it's not the placeholder or if forced
            self.mongo_client = MongoClient(uri, serverSelectionTimeoutMS=2000)
            self.mongo_client.server_info() # Test connection
            self.mongo_db = self.mongo_client[Config.MONGODB_DB]
            self.mode = "MONGODB"
            print(f"✅ High-Performance Mode: Connected to MongoDB ({Config.MONGODB_DB})")
        except Exception as e:
            # 2. Fallback to SQLite
            print(f"⚠️ MongoDB Unavailable: {e}")
            print("🚀 Reliability Mode: Falling back to local SQLite database")
            self.mode = "SQLITE"
            self._init_sqlite()

    def _init_sqlite(self):
        conn = sqlite3.connect(self.sqlite_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id TEXT PRIMARY KEY,
                data TEXT,
                created_at TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def save_prediction(self, data: Dict[str, Any]):
        if self.mode == "PENDING": self.connect()
        data_json = json.loads(json.dumps(data, cls=NpEncoder))
        data_json["created_at"] = datetime.now().isoformat()
        
        if self.mode == "MONGODB":
            try:
                self.mongo_db.predictions.insert_one(data_json)
                return
            except:
                self.mode = "SQLITE" # Flash-switch on failure
                self._init_sqlite()

        # SQLite fallback
        conn = sqlite3.connect(self.sqlite_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO reports (id, data, created_at) VALUES (?, ?, ?)", 
                      (data.get("prediction_id"), json.dumps(data_json), data_json["created_at"]))
        conn.commit()
        conn.close()

    def get_all_reports(self, limit=50):
        if self.mode == "PENDING": self.connect()
        
        if self.mode == "MONGODB":
            try:
                return list(self.mongo_db.predictions.find({}, {"_id": 0}).sort("created_at", -1).limit(limit))
            except:
                pass

        # SQLite fallback
        conn = sqlite3.connect(self.sqlite_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM reports ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [json.loads(row["data"]) for row in rows]

# Global Instance
db_manager = HybridDatabaseManager()

def init_db():
    db_manager.connect()

def save_prediction(prediction_id, image_filename, blood_type, confidence, consensus_met, agent_votes, reasoning, cbc_data=None):
    db_manager.save_prediction({
        "prediction_id": prediction_id,
        "image_filename": image_filename,
        "blood_type": blood_type,
        "confidence": confidence,
        "consensus_met": consensus_met,
        "agent_votes": agent_votes,
        "reasoning": reasoning,
        "cbc_data": cbc_data or {},
        "agent_assessments": []
    })

def save_agent_assessment(prediction_id, agent_id, agent_name, prediction, confidence, reasoning, metadata):
    # For now, we update the existing record if possible
    # In a simple hybrid, we'll focus on the main prediction record
    pass

def get_reports():
    return db_manager.get_all_reports()

def get_prediction(prediction_id):
    reports = db_manager.get_all_reports()
    for r in reports:
        if r.get("prediction_id") == prediction_id: return r
    return None

def log_audit(prediction_id, action, user_id=None, ip_address=None, details=None):
    pass
