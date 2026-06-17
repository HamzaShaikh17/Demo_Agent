"""Minimal ReAct-style agent implemented in plain Python using Anthropic API.

Supports registering simple tools and running a short reasoning loop where
the model may choose to call a tool or return a final answer. Logs every
LLM and tool call with timestamps.
"""
from datetime import datetime
from typing import Dict, Any
from agent.anthropic_client import AnthropicClient
from agent.openai_client import OpenAIClient
from agent.huggingface_client import HuggingFaceClient


def create_llm_client(provider: str, **kwargs):
    provider = provider.lower()
    match provider:
        case "anthropic":
            return AnthropicClient(**kwargs)
        case "openai":
            return OpenAIClient(**kwargs)
        case "huggingface":
            return HuggingFaceClient(**kwargs)
        case _:
            raise ValueError(f"Unknown provider: {provider}")


def _log_tool_call(tool_name: str, args: Any):
    ts = datetime.utcnow().isoformat() + "Z"
    print(f"[TOOL CALL {ts}] {tool_name} args={args}")


class Agent:
    def __init__(self, llm: Any, tools: Dict[str, Dict]):
        self.llm = llm
        self.tools = tools

    def _build_prompt(self, query: str, history: str, style: str = "cot"):
        tools_desc = "\n".join([f"{k}: {v['description']}" for k, v in self.tools.items()])
        if style == "cot":
            instr = (
                "You are an assistant that reasons step-by-step (Chain-of-Thought).\n"
                "When you want to use a tool, output: <ACTION>tool_name args</ACTION>.\n"
                "When finished, output: <FINAL>your answer</FINAL>.\n"
            )
        else:
            instr = (
                "You are an assistant that reasons using Thoughts-of-Thoughts (ToT).")
        prompt = f"{instr}\nTOOLS:\n{tools_desc}\n\nHistory:\n{history}\n\nUser: {query}\nAssistant:"
        return prompt

    def run(self, query: str, max_steps: int = 4, style: str = "cot"):
        history = ""
        for step in range(max_steps):
            prompt = self._build_prompt(query, history, style=style)
            resp = self.llm.complete(prompt)
            text = resp.get("text") or resp.get("completion") or ""
            history += f"Assistant (step {step}): {text}\n"
            # naive parse for action markers
            if "<ACTION>" in text and "</ACTION>" in text:
                start = text.index("<ACTION>") + len("<ACTION>")
                end = text.index("</ACTION>")
                action_text = text[start:end].strip()
                # expected format: tool_name args (args can be freeform)
                parts = action_text.split(" ", 1)
                tool_name = parts[0]
                tool_args = parts[1] if len(parts) > 1 else ""
                tool = self.tools.get(tool_name)
                if tool:
                    _log_tool_call(tool_name, tool_args)
                    try:
                        result = tool["func"](tool_args)
                    except TypeError:
                        # try calling without args
                        result = tool["func"]()
                    history += f"Tool {tool_name} returned: {result}\n"
                    continue
                else:
                    history += f"Unknown tool: {tool_name}\n"
                    continue

            if "<FINAL>" in text and "</FINAL>" in text:
                start = text.index("<FINAL>") + len("<FINAL>")
                end = text.index("</FINAL>")
                final = text[start:end].strip()
                return {"final": final, "history": history}

        # If loop exhausted, return last assistant text as best effort
        return {"final": text.strip(), "history": history}
