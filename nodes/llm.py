import os
from typing import Optional

from config import GROK_API_KEY, LLM_BACKEND, LLM_MODEL
from utils.prompts import GENERIC_PROMPT
import json


def _make_openai_client(api_key: str):
    try:
        from openai import OpenAI
    except Exception as e:
        raise RuntimeError("openai package not installed. Install with `pip install openai`") from e
    # Use Groq/OpenAI-compatible base URL from config when available.
    from config import LLM_API_BASE
    return OpenAI(api_key=api_key, base_url=LLM_API_BASE)


_API_KEY = GROK_API_KEY or os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_ADMIN_KEY")

# Initialize backend client lazily
_hf_pipe = None
_openai_client = None


def _init_transformers_pipeline(model_name: str):
    try:
        from transformers import pipeline
    except Exception as e:
        raise RuntimeError("transformers not installed. Install with `pip install transformers[torch]`") from e

    # Create a text-generation pipeline. Note: large Llama models require substantial RAM/GPU.
    pipe = pipeline("text-generation", model=model_name, device_map="auto")
    return pipe


def llm(state: dict):
    # Build context: prefer structured document_context, fall back to retrieved_context
    context = state.get('document_context') or state.get('retrieved_context') or ''
    memory = state.get('memory', {}) or {}
    # build history string
    history_items = state.get('qa_history', []) or []
    history_str = ''
    for h in history_items:
        q = h.get('question')
        a = h.get('answer')
        history_str += f'Q: {q}\nA: {a}\n\n'

    prompt = GENERIC_PROMPT.format(
        context=context,
        memory=json.dumps(memory, ensure_ascii=False),
        history=history_str,
        question=state.get('question', '')
    )

    backend = (LLM_BACKEND or "grok").lower()

    if backend == "transformers":
        global _hf_pipe
        if _hf_pipe is None:
            _hf_pipe = _init_transformers_pipeline(LLM_MODEL)

        # Generate answer
        outputs = _hf_pipe(prompt, max_new_tokens=256, do_sample=False)
        # The pipeline returns generated_text merged with prompt for many models; try to extract tail.
        gen = outputs[0].get("generated_text") or outputs[0].get("text") or str(outputs[0])
        answer = gen

    else:
        # Fallback to OpenAI/Grok API
        if not _API_KEY:
            raise RuntimeError(
                "OpenAI/Grok API key not found. Set GROK_API_KEY in config.py or OPENAI_API_KEY env var."
            )

        global _openai_client
        if _openai_client is None:
            _openai_client = _make_openai_client(_API_KEY)

        response = _openai_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        try:
            answer = response.choices[0].message.content
        except Exception:
            answer = getattr(response, 'content', '') or str(response)

    state["answer"] = answer
    return state