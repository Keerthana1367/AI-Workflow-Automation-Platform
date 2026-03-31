from services.llm_service import generate_response

def run(input_text: str) -> str:
    prompt = f"""
    You are a professional email writer.

    Task:
    Write a clear and professional email based on the input.

    Input:
    {input_text}

    Output format:
    Subject:
    Body:
    """

    return generate_response(prompt)