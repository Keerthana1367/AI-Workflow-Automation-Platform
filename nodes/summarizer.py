from services.llm_service import generate_response

def run(input_text: str) -> str:
    prompt = f"""
    You are an expert summarizer.

    Task:
    Summarize the following text clearly and concisely.

    Text:
    {input_text}

    Output:
    - Use bullet points
    - Keep it short and clear
    """

    return generate_response(prompt)