from config import model

def generate_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)

        # Handle response safely
        if hasattr(response, "text"):
            return response.text
        else:
            return str(response)

    except Exception as e:
        return f"Error: {str(e)}"