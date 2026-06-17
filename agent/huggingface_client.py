"""Minimal HuggingFace inference client wrapper with logging and fallback.

This wrapper supports local transformers inference when the `transformers`
library is installed, or remote HuggingFace Inference API calls when
`HUGGINGFACEHUB_API_TOKEN` is configured.
"""
import os
from datetime import datetime

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    import torch
except Exception:
    pipeline = None
    AutoTokenizer = None
    AutoModelForCausalLM = None
    torch = None

try:
    import requests
except Exception:
    requests = None


def _log_llm_call(prompt: str):
    ts = datetime.utcnow().isoformat() + "Z"
    print(f"[LLM CALL {ts}] prompt=\n{prompt[:1000]}\n---")


class HuggingFaceClient:
    def __init__(self, model: str = None, api_token: str = None):
        self.model = model or os.getenv("HF_MODEL", "gpt2")
        self.api_token = api_token or os.getenv("HUGGINGFACEHUB_API_TOKEN")
        self._local_generator = None
        self._ensure_local_generator()

    def _ensure_local_generator(self):
        if pipeline is None:
            return
        try:
            device = 0 if torch is not None and torch.cuda.is_available() else -1
            self._local_generator = pipeline(
                "text-generation",
                model=self.model,
                device=device,
            )
        except Exception:
            self._local_generator = None

    def complete(self, prompt: str, max_tokens: int = 256, temperature: float = 0.0):
        _log_llm_call(prompt)
        if self._local_generator is not None:
            try:
                output = self._local_generator(
                    prompt,
                    max_new_tokens=max_tokens,
                    do_sample=temperature > 0,
                    temperature=temperature,
                    return_full_text=False,
                )
                text = output[0]["generated_text"]
                ts = datetime.utcnow().isoformat() + "Z"
                print(f"[LLM RESP {ts}] (local) text=\n{text[:1000]}\n---")
                return {"text": text}
            except Exception as exc:
                ts = datetime.utcnow().isoformat() + "Z"
                print(f"[LLM ERROR {ts}] local generation failed: {exc}")

        if self.api_token and requests is not None:
            url = f"https://api-inference.huggingface.co/models/{self.model}"
            headers = {"Authorization": f"Bearer {self.api_token}"}
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                },
            }
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=60)
                r.raise_for_status()
                data = r.json()
                if isinstance(data, dict) and data.get("error"):
                    raise RuntimeError(data["error"])
                text = data[0].get("generated_text") if isinstance(data, list) else None
                if text is None:
                    text = str(data)
                ts = datetime.utcnow().isoformat() + "Z"
                print(f"[LLM RESP {ts}] (hf-api) text=\n{text[:1000]}\n---")
                return {"text": text}
            except Exception as exc:
                ts = datetime.utcnow().isoformat() + "Z"
                print(f"[LLM ERROR {ts}] HuggingFace API failed: {exc}")

        ts = datetime.utcnow().isoformat() + "Z"
        text = f"MOCK RESPONSE for prompt (truncated): {prompt[:200]} [time:{ts}]"
        print(f"[LLM RESP {ts}] (mock) text=\n{text[:1000]}\n---")
        return {"text": text}
