import re


PATTERNS = {

    "document_id": [
        r"Document\s*(?:No|Number|#)?\s*[:\-]?\s*([A-Za-z0-9\-\/]+)"
    ],

    "document_date": [
        r"(\d{2}[/-]\d{2}[/-]\d{4})",
        r"(\d{4}[/-]\d{2}[/-]\d{2})"
    ],

    "total_amount": [
        r"Grand\s*Total\s*[:\-]?\s*₹?\s*([\d,]+\.\d{2})",
        r"Total\s*Amount\s*[:\-]?\s*₹?\s*([\d,]+\.\d{2})"
    ]
}


def extract_fields(text):

    metadata = {}

    for key, patterns in PATTERNS.items():

        value = None

        for pattern in patterns:

            match = re.search(pattern, text, re.IGNORECASE)

            if match:

                value = match.group(1)

                break

        metadata[key] = value

    return metadata
