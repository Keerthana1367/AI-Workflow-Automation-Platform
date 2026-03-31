def run(input_text: str) -> str:
    # simple condition example
    if len(input_text) < 100:
        return "SHORT_TEXT::" + input_text
    else:
        return "LONG_TEXT::" + input_text