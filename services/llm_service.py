import json
from typing import Type, Optional, Any
from pydantic import BaseModel
from config import model, genai

def generate_response(prompt: str, schema: Optional[Type[BaseModel]] = None) -> Any:
    """
    Generates a response from Gemini. Supports structured output via Pydantic.
    """
    try:
        generation_config = {}
        if schema:
            generation_config = {
                "response_mime_type": "application/json",
                "response_schema": schema
            }
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(**generation_config) if generation_config else None
        )

        # Handle response safely
        if hasattr(response, "text"):
            text_output = response.text
            if schema:
                try:
                    # Validate and return as Pydantic model
                    data = json.loads(text_output)
                    return schema(**data)
                except Exception as ve:
                    return f"Validation Error: {str(ve)} | Raw: {text_output}"
            return text_output
        else:
            return str(response)

    except Exception as e:
        return f"Error: {str(e)}"