def route_document(state):

    ext = state["file_type"]

    if ext == ".pdf":
        return "pdf"

    elif ext == ".docx":
        return "docx"

    elif ext in [".xlsx", ".xls"]:
        return "excel"

    elif ext in [".png", ".jpg", ".jpeg"]:
        return "image"

    else:
        raise ValueError(f"Unsupported file type: {ext}")