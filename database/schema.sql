-- Predictions Table
CREATE TABLE predictions (
    id TEXT PRIMARY KEY,
    image_filename TEXT NOT NULL,
    blood_type TEXT NOT NULL,
    confidence REAL NOT NULL,
    consensus_met BOOLEAN NOT NULL,
    agent_votes TEXT,
    reasoning TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent Assessments Table
CREATE TABLE agent_assessments (
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
);

-- Audit Logs Table
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id TEXT,
    action TEXT NOT NULL,
    user_id TEXT,
    ip_address TEXT,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prediction_id) REFERENCES predictions(id)
);

-- Create indexes for performance
CREATE INDEX idx_predictions_blood_type ON predictions(blood_type);
CREATE INDEX idx_predictions_created_at ON predictions(created_at);
CREATE INDEX idx_agent_assessments_prediction_id ON agent_assessments(prediction_id);
CREATE INDEX idx_audit_logs_prediction_id ON audit_logs(prediction_id);
