from workflow_engine import run_workflow

text = "I am applying for a software engineering role and need help writing a professional email."

steps = ["Summarizer", "Email Generator"]

final_output, logs = run_workflow(steps, text)

print("FINAL OUTPUT:\n", final_output)

print("\nLOGS:")
for log in logs:
    print(f"\nStep: {log['step']}")
    print(log["output"])