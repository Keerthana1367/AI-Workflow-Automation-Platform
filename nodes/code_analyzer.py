from services.llm_service import generate_response

def run(input_text: str) -> str:
    prompt = f"""
    You are an expert software engineer.

    Analyze the following code and provide:

    1. What the code does
    2. Bugs or issues (if any)
    3. Suggested improvements
    4. Optimized version of the code
    5. give optimized code if needed only dont give optimised code all the time 
    6. explain bugs if present and also errors give suggestions to improve the code quality in bullet points
    Code:
    {input_text}

    Output format:
    - Explanation
    - Issues
    - Improvements(in bullet points)
    - Fixed Code(if majorly needed if minor issues just suggest particular line code where is the issue there.)
    """

    return generate_response(prompt)