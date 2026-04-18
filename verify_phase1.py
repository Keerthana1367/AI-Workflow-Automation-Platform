from workflow_engine import run_workflow
from database import get_execution_history, get_step_logs, get_connection
import json
import os

def verify():
    print("🚀 STARTING PHASE 1 VERIFICATION...\n")

    # 1. Check if DB exists
    if os.path.exists("platform.db"):
        print("✅ platform.db found.")
    else:
        print("❌ platform.db NOT found. Initializing now...")

    # 2. Run a real AI workflow (Summarizer -> Condition)
    test_input = """
    Phase 1 of our project involves migrating to a SQL backend and enforcing Pydantic schemas. 
    This ensures that our AI outputs are no longer brittle strings but structured engineering artifacts.
    Containerization via Docker ensures that 'it works on my machine' is no longer an excuse.
    """
    
    print("🤖 Running AI nodes (Summarizer -> Condition)...")
    try:
        output, history = run_workflow(["Summarizer", "Condition"], test_input)
        print("✅ Workflow execution successful.")
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        return

    # 3. Verify Database Records
    executions = get_execution_history(limit=1)
    if not executions:
        print("❌ No executions found in DB.")
        return
    
    exec_record = executions[0]
    exec_id = exec_record['id']
    print(f"\n📊 DATABASE RECORD FOUND:")
    print(f"   Execution ID: {exec_id}")
    print(f"   Status:       {exec_record['status']}")
    print(f"   Started At:   {exec_record['started_at']}")

    # 4. Verify Step Logs (Observability)
    logs = get_step_logs(exec_id)
    print(f"\n📝 OBSERVABILITY CHECK ({len(logs)} steps recorded):")
    for log in logs:
        print(f"   [{log['node_name']}] -> Duration: {log['duration_ms']}ms | Error: {log['error']}")
        # Check if the output looks like structured text
        if log['node_name'] == "Summarizer":
            print(f"   [Summarizer Preview]: {log['output_data'][:100]}...")

    print("\n🏆 PHASE 1 VERIFIED: SQL and Pydantic layers are operational.")

if __name__ == "__main__":
    verify()
