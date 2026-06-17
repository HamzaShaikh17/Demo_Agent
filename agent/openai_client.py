"""Minimal OpenAI client wrapper with logging and fallback."""
import os
from datetime import datetime

try:
    import requests
except Exception:
    requests = None


def _log_llm_call(prompt: str):
    ts = datetime.utcnow().isoformat() + "Z"
    print(f"[LLM CALL {ts}] prompt=\n{prompt[:1000]}\n---")


class OpenAIClient:
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

    def complete(self, prompt: str, max_tokens: int = 256, temperature: float = 0.0):
        _log_llm_call(prompt)
        if self.api_key and requests is not None:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=60)
                r.raise_for_status()
                data = r.json()
                text = data["choices"][0]["message"]["content"]
                ts = datetime.utcnow().isoformat() + "Z"
                print(f"[LLM RESP {ts}] (openai) text=\n{text[:1000]}\n---")
                return {"text": text}
            except Exception as exc:
                ts = datetime.utcnow().isoformat() + "Z"
                print(f"[LLM ERROR {ts}] OpenAI API failed: {exc}")

        ts = datetime.utcnow().isoformat() + "Z"
        text = f"MOCK RESPONSE for prompt (truncated): {prompt[:200]} [time:{ts}]"
        print(f"[LLM RESP {ts}] (mock) text=\n{text[:1000]}\n---")
        return {"text": text}
