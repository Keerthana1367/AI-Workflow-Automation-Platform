import sqlite3
import json
import uuid
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DATABASE_URL = os.getenv("DATABASE_URL")
DB_PATH = os.getenv("DB_PATH", "platform.db")

IS_POSTGRES = DATABASE_URL and DATABASE_URL.startswith("postgres")

if IS_POSTGRES:
    import psycopg2
    from psycopg2.extras import RealDictCursor

def get_connection():
    if IS_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def execute_query(query: str, params: tuple = (), fetchall=False, fetchone=False, commit=False):
    """Helper to execute query and handle placeholders."""
    conn = get_connection()
    try:
        if IS_POSTGRES:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            # Replace sqlite '?' with postgres '%s'
            pg_query = query.replace('?', '%s')
            cursor.execute(pg_query, params)
        else:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
        result = None
        if fetchall:
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
        elif fetchone:
            row = cursor.fetchone()
            result = dict(row) if row else None
            
        if commit:
            conn.commit()
            
        return result
    finally:
        conn.close()

def init_db():
    try:
        # 1. Workflows Table
        if IS_POSTGRES:
            execute_query("""
            CREATE TABLE IF NOT EXISTS workflows (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE,
                steps TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """, commit=True)
            
            execute_query("""
            CREATE TABLE IF NOT EXISTS executions (
                id TEXT PRIMARY KEY,
                workflow_id TEXT,
                status TEXT,
                started_at TIMESTAMP,
                finished_at TIMESTAMP,
                input_summary TEXT,
                final_output TEXT,
                FOREIGN KEY(workflow_id) REFERENCES workflows(id) ON DELETE CASCADE
            )
            """, commit=True)
            
            execute_query("""
            CREATE TABLE IF NOT EXISTS step_logs (
                id TEXT PRIMARY KEY,
                execution_id TEXT,
                node_name TEXT,
                input_data TEXT,
                output_data TEXT,
                duration_ms INTEGER,
                error TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(execution_id) REFERENCES executions(id) ON DELETE CASCADE
            )
            """, commit=True)
            
            execute_query("""
            CREATE TABLE IF NOT EXISTS prompt_evals (
                id TEXT PRIMARY KEY,
                prompt_version TEXT,
                input_hash TEXT,
                output_quality_score REAL,
                latency_ms INTEGER,
                token_count INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """, commit=True)
        else:
            # SQLite setup (same as before)
            execute_query("""
            CREATE TABLE IF NOT EXISTS workflows (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE,
                steps TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """, commit=True)
            
            execute_query("""
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
            """, commit=True)
            
            execute_query("""
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
            """, commit=True)
            
            execute_query("""
            CREATE TABLE IF NOT EXISTS prompt_evals (
                id TEXT PRIMARY KEY,
                prompt_version TEXT,
                input_hash TEXT,
                output_quality_score REAL,
                latency_ms INTEGER,
                token_count INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """, commit=True)
    except Exception as e:
        print(f"Database initialization error: {e}")

# --- Workflow Operations ---

def save_workflow_def(name: str, steps: List[str]):
    wf_id = str(uuid.uuid4())
    steps_json = json.dumps(steps)
    
    if IS_POSTGRES:
        query = """
            INSERT INTO workflows (id, name, steps) 
            VALUES (%s, %s, %s)
            ON CONFLICT (name) 
            DO UPDATE SET steps = EXCLUDED.steps
        """
        execute_query(query, (wf_id, name, steps_json), commit=True)
    else:
        query = "INSERT OR REPLACE INTO workflows (id, name, steps) VALUES (?, ?, ?)"
        execute_query(query, (wf_id, name, steps_json), commit=True)
        
    return wf_id

def get_all_workflow_defs():
    return execute_query("SELECT * FROM workflows ORDER BY created_at DESC", fetchall=True)

def delete_workflow_def(wf_id: str):
    execute_query("DELETE FROM workflows WHERE id = ?", (wf_id,), commit=True)

def get_workflow_id_by_name(name: str):
    row = execute_query("SELECT id FROM workflows WHERE name = ?", (name,), fetchone=True)
    return row['id'] if row else None

def get_workflow_steps_by_name(name: str):
    row = execute_query("SELECT steps FROM workflows WHERE name = ?", (name,), fetchone=True)
    return json.loads(row['steps']) if row else None

# --- Execution Operations ---

def create_execution(workflow_id: Optional[str], input_summary: str):
    exec_id = str(uuid.uuid4())
    execute_query("""
        INSERT INTO executions (id, workflow_id, status, started_at, input_summary)
        VALUES (?, ?, ?, ?, ?)
    """, (exec_id, workflow_id, "RUNNING", datetime.now(), input_summary[:200]), commit=True)
    return exec_id

def update_execution(exec_id: str, status: str, final_output: str = ""):
    execute_query("""
        UPDATE executions 
        SET status = ?, finished_at = ?, final_output = ? 
        WHERE id = ?
    """, (status, datetime.now(), final_output, exec_id), commit=True)

def log_step(exec_id: str, node_name: str, input_data: str, output_data: str, duration_ms: int, error: Optional[str] = None):
    execute_query("""
        INSERT INTO step_logs (id, execution_id, node_name, input_data, output_data, duration_ms, error)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (str(uuid.uuid4()), exec_id, node_name, input_data, output_data, duration_ms, error), commit=True)

def log_prompt_eval(version: str, input_text: str, score: float, latency: int, tokens: int):
    import hashlib
    input_hash = hashlib.md5(input_text.encode()).hexdigest()
    execute_query("""
        INSERT INTO prompt_evals (id, prompt_version, input_hash, output_quality_score, latency_ms, token_count)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (str(uuid.uuid4()), version, input_hash, score, latency, tokens), commit=True)

def get_execution_history(limit=10):
    return execute_query("""
        SELECT e.*, w.name as workflow_name 
        FROM executions e
        LEFT JOIN workflows w ON e.workflow_id = w.id
        ORDER BY e.started_at DESC
        LIMIT ?
    """, (limit,), fetchall=True)

def get_step_logs(exec_id: str):
    return execute_query("SELECT * FROM step_logs WHERE execution_id = ? ORDER BY timestamp ASC", (exec_id,), fetchall=True)

def get_execution_status(exec_id: str):
    return execute_query("SELECT status, final_output FROM executions WHERE id = ?", (exec_id,), fetchone=True)
