from nodes.summarizer import run as summarize
from nodes.email_generator import run as email
from nodes.code_analyzer import run as code_analyzer
from nodes.condition_node import run as condition

NODE_MAP = {
    "Summarizer": summarize,
    "Email Generator": email,
    "Code Analyzer": code_analyzer,
    "Condition": condition
}

def run_workflow(steps, input_text):
    data = input_text
    logs = []

    for step in steps:
        if step in NODE_MAP:
            data = NODE_MAP[step](data)
        else:
            data = f"Unknown step: {step}"

        logs.append({
            "step": step,
            "output": data
        })

    return data, logs