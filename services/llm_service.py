import json
from typing import Type, Optional, Any
from pydantic import BaseModel
from config import groq_client, MODEL_NAME

def generate_response(prompt: str, schema: Optional[Type[BaseModel]] = None) -> Any:
    """
    Generates a response from Groq. Supports structured output via Pydantic.
    """
    if not groq_client:
        return "Error: GROQ_API_KEY is not set."

    try:
        messages = []
        
        # Enforce structured output in the prompt if a schema is provided
        if schema:
            schema_json = json.dumps(schema.model_json_schema(), indent=2)
            prompt += f"\n\nYou MUST return ONLY a valid JSON object matching this schema. Do not add any extra text or markdown formatting:\n{schema_json}"

        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.2,
        }

        # Enable JSON mode for Groq
        if schema:
            kwargs["response_format"] = {"type": "json_object"}

        response = groq_client.chat.completions.create(**kwargs)
        
        text_output = response.choices[0].message.content

        # Handle response safely
        if schema:
            try:
                # Validate and return as Pydantic model
                data = json.loads(text_output)
                return schema(**data)
            except Exception as ve:
                return f"Validation Error: {str(ve)} | Raw: {text_output}"
        
        return text_output

    except Exception as e:
        return f"Error: {str(e)}"