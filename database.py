import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = "platform.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Workflows Table (Definitions)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workflows (
        id TEXT PRIMARY KEY,
        name TEXT UNIQUE,
        steps TEXT, -- JSON list of step names
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 2. Executions Table (Specific Runs)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS executions (
        id TEXT PRIMARY KEY,
        workflow_id TEXT,
        status TEXT,
        started_at TIMESTAMP,
        finished_at TIMESTAMP,
        input_summary TEXT,
        final_output TEXT,
        FOREIGN KEY(workflow_id) REFERENCES workflows(id)
    )
    """)
    
    # 3. Step Logs Table (Individual Node Results)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS step_logs (
        id TEXT PRIMARY KEY,
        execution_id TEXT,
        node_name TEXT,
        input_data TEXT,
        output_data TEXT,
        duration_ms INTEGER,
        error TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(execution_id) REFERENCES executions(id)
    )
    """)

    # 4. Prompt Evals Table (Evaluation Framework)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prompt_evals (
        id TEXT PRIMARY KEY,
        prompt_version TEXT,
        input_hash TEXT,
        output_quality_score REAL,
        latency_ms INTEGER,
        token_count INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

# --- Workflow Operations ---

def save_workflow_def(name: str, steps: List[str]):
    conn = get_connection()
    cursor = conn.cursor()
    wf_id = str(uuid.uuid4())
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO workflows (id, name, steps) VALUES (?, ?, ?)",
            (wf_id, name, json.dumps(steps))
        )
        conn.commit()
        return wf_id
    finally:
        conn.close()

def get_all_workflow_defs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workflows ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_workflow_def(wf_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM workflows WHERE id = ?", (wf_id,))
    conn.commit()
    conn.close()

# --- Execution Operations ---

def create_execution(workflow_id: Optional[str], input_summary: str):
    conn = get_connection()
    cursor = conn.cursor()
    exec_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO executions (id, workflow_id, status, started_at, input_summary)
        VALUES (?, ?, ?, ?, ?)
    """, (exec_id, workflow_id, "RUNNING", datetime.now(), input_summary[:200]))
    conn.commit()
    conn.close()
    return exec_id

def update_execution(exec_id: str, status: str, final_output: str = ""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE executions 
        SET status = ?, finished_at = ?, final_output = ? 
        WHERE id = ?
    """, (status, datetime.now(), final_output, exec_id))
    conn.commit()
    conn.close()

def log_step(exec_id: str, node_name: str, input_data: str, output_data: str, duration_ms: int, error: Optional[str] = None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO step_logs (id, execution_id, node_name, input_data, output_data, duration_ms, error)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (str(uuid.uuid4()), exec_id, node_name, input_data, output_data, duration_ms, error))
    conn.commit()
    conn.close()

def log_prompt_eval(version: str, input_text: str, score: float, latency: int, tokens: int):
    import hashlib
    input_hash = hashlib.md5(input_text.encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prompt_evals (id, prompt_version, input_hash, output_quality_score, latency_ms, token_count)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (str(uuid.uuid4()), version, input_hash, score, latency, tokens))
    conn.commit()
    conn.close()

def get_execution_history(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.*, w.name as workflow_name 
        FROM executions e
        LEFT JOIN workflows w ON e.workflow_id = w.id
        ORDER BY e.started_at DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_step_logs(exec_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM step_logs WHERE execution_id = ? ORDER BY timestamp ASC", (exec_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
