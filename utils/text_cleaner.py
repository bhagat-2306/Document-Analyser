import re


def clean_text(text: str) -> str:
    """
    Basic text cleaning for extracted document text.
    """

    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r", "\n")

    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Remove multiple spaces
    text = re.sub(r"[ ]+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n+", "\n", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text