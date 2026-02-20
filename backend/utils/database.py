import sqlite3
import os
from datetime import datetime
from backend.config import Config

import json
import numpy as np

DATABASE_PATH = Config.DATABASE_URL.replace("sqlite:///", "")

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (bool, np.bool_)):
            return bool(obj)
        return super(NpEncoder, self).default(obj)

def init_db():
    """Initialize database with schema"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id TEXT PRIMARY KEY,
            image_filename TEXT NOT NULL,
            blood_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            consensus_met BOOLEAN NOT NULL,
            agent_votes TEXT,
            reasoning TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Agent assessments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_id TEXT NOT NULL,
            agent_id TEXT NOT NULL,
            agent_name TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            reasoning TEXT,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prediction_id) REFERENCES predictions(id)
        )
    ''')
    
    # Audit log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_id TEXT,
            action TEXT NOT NULL,
            user_id TEXT,
            ip_address TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prediction_id) REFERENCES predictions(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_prediction(
    prediction_id: str,
    image_filename: str,
    blood_type: str,
    confidence: float,
    consensus_met: bool,
    agent_votes: dict,
    reasoning: str
):
    """Save prediction to database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    import json
    cursor.execute('''
        INSERT INTO predictions (
            id, image_filename, blood_type, confidence,
            consensus_met, agent_votes, reasoning
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        prediction_id,
        image_filename,
        blood_type,
        confidence,
        bool(consensus_met),
        json.dumps(agent_votes, cls=NpEncoder),
        reasoning
    ))
    
    conn.commit()
    conn.close()

def save_agent_assessment(
    prediction_id: str,
    agent_id: str,
    agent_name: str,
    prediction: str,
    confidence: float,
    reasoning: str,
    metadata: dict
):
    """Save individual agent assessment"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    import json
    cursor.execute('''
        INSERT INTO agent_assessments (
            prediction_id, agent_id, agent_name,
            prediction, confidence, reasoning, metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        prediction_id,
        agent_id,
        agent_name,
        prediction,
        confidence,
        reasoning,
        json.dumps(metadata, cls=NpEncoder)
    ))
    
    conn.commit()
    conn.close()

def get_prediction(prediction_id: str) -> dict:
    """Retrieve prediction from database"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM predictions WHERE id = ?', (prediction_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return dict(result)
    return None

def log_audit(
    prediction_id: str,
    action: str,
    user_id: str = None,
    ip_address: str = None,
    details: str = None
):
    """Log action for audit trail"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO audit_logs (
            prediction_id, action, user_id, ip_address, details
        ) VALUES (?, ?, ?, ?, ?)
    ''', (prediction_id, action, user_id, ip_address, details))
    
    conn.commit()
    conn.close()
