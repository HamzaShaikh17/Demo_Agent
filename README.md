# My Agent Project

A structured Python framework for building agentic AI workflows — from a simple ReAct agent to enterprise-grade multi-agent systems.

---

## Directory Structure

![Project directory structure](./structure.png)

---

## Folder Breakdown

| Folder | Purpose |
|---|---|
| `agents/` | Agent logic — base loop + specialized agents |
| `tools/` | One file per callable tool |
| `memory/` | Short-term (context), long-term (JSON/DB), vector store |
| `graphs/` | LangGraph graphs, state definitions, checkpointers |
| `prompts/` | All prompt strings, never hardcoded in agent files |
| `evals/` | Benchmarks and test queries |
| `config/` | Env var loading, `.env.example` |

---

## Stack

- **Python** 3.11
- **LangChain** + **LangGraph** — agent orchestration
- **HuggingFace Inference API** — LLM backend (free tier)
- **Tavily** — agentic web search
- **uv** — package management

---

## Setup

```bash
# Install dependencies
uv pip install langchain langgraph huggingface_hub tavily-python

# Set environment variables
cp config/.env.example .env
# Fill in HUGGINGFACE_API_TOKEN and TAVILY_API_KEY

# Run
python main.py
```

---

## Agents Built

- [ ] ReAct agent (plain Python + HuggingFace)
- [ ] Plan-and-Execute agent
- [ ] LangGraph researcher + writer (2-node)
- [ ] LangGraph system with supervisor + HITL
- [ ] CrewAI 4-agent crew
- [ ] AutoGen GroupChat

---

## Week 1 Checkpoint

- [ ] ReAct agent with 3 tools (`web_search`, `calculator`, `get_current_time`)
- [ ] LangGraph 3-node system with conditional routing
- [ ] Same task implemented in LangGraph, CrewAI, AutoGen
- [ ] Framework comparison doc (`docs/framework_decision.md`)

---

## Notes

- All prompts live in `prompts/` — never hardcoded inside agent files
- Each tool is a standalone file in `tools/` exporting a single callable
- `graphs/state.py` holds the shared `TypedDict` flowing through all LangGraph graphs
- Eval scripts in `evals/` benchmark latency, token cost, and lines of code across frameworks