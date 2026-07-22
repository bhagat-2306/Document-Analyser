# Document Intelligence

A clean Streamlit document intelligence app using a graph-style pipeline.

## Project structure

- `app.py` — Streamlit entry point and UI only.
- `config.py` — API keys, constants, and folder paths.
- `graph/` — Processing graph orchestration and query flow.
- `nodes/` — Single-purpose nodes for extraction, preprocessing, metadata, chunking, embeddings, retrieval, and LLM calls.
- `utils/` — Reusable helpers for file handling, OCR, cleaning, and regex extraction.
- `models/` — Shared embedding model initialization.
- `uploads/` — Temporary user uploads.
- `vector_db/` — Optional FAISS index storage.

## Getting started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API key:

```env
GROK_API_KEY=your_api_key_here
```

3. Run the app:

```bash
streamlit run app.py
```

## Usage

1. Upload a document.
2. Click **Process document** once to load, extract, clean, chunk, and embed the document.
3. Ask multiple questions against the same processed document without rebuilding embeddings.

## Notes

- The app preserves the processed document in session state so repeated questions reuse the same vector store.
- Supported formats: PDF, DOCX, Excel, PNG, JPG, JPEG.
- PDF extraction uses text extraction first and falls back to OCR when needed.
