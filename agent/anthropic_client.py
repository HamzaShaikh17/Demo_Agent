"""Minimal Anthropic client wrapper with logging and a mock fallback.

This wrapper will attempt to call Anthropic's completion endpoint if
`ANTHROPIC_API_KEY` is set in the environment. If it's not set or a
request fails, it returns a deterministic mock response to allow local
experimentation without network access.
"""
import os
import time
import json
from datetime import datetime

try:
    import requests
except Exception:
    requests = None


def _log_llm_call(prompt: str):
    ts = datetime.utcnow().isoformat() + "Z"
    print(f"[LLM CALL {ts}] prompt=\n{prompt[:1000]}\n---")


class AnthropicClient:
    def __init__(self, api_key: str = None, model: str = "claude-2"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model

    def complete(self, prompt: str, max_tokens: int = 512):
        _log_llm_call(prompt)
        if not self.api_key or requests is None:
            # Mock deterministic response for offline testing
            ts = datetime.utcnow().isoformat() + "Z"
            resp = {
                "id": "mock-1",
                "model": self.model,
                "object": "text_completion",
                "text": f"MOCK RESPONSE for prompt (truncated): {prompt[:200]}\n[time:{ts}]",
            }
            print(f"[LLM RESP {ts}] (mock) text=\n{resp['text'][:1000]}\n---")
            return resp

        url = "https://api.anthropic.com/v1/complete"
        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
        }
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=30)
            r.raise_for_status()
            j = r.json()
            ts = datetime.utcnow().isoformat() + "Z"
            print(f"[LLM RESP {ts}] status={r.status_code} keys={list(j.keys())}")
            return j
        except Exception as exc:
            ts = datetime.utcnow().isoformat() + "Z"
            print(f"[LLM ERROR {ts}] {exc}")
            # fallback mock
            return {
                "id": "mock-err",
                "model": self.model,
                "object": "text_completion",
                "text": f"MOCK FALLBACK: request failed: {exc}",
            }
