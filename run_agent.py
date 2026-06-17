"""Experiment runner: runs the agent on sample queries with CoT and ToT prompts.

Usage: set `HUGGINGFACEHUB_API_TOKEN` in environment to enable HuggingFace Inference API.
Run: `python run_agent.py`
"""
from agent.agent import Agent, create_llm_client
from tools import web_search, calculator, get_current_time
from datetime import datetime


def make_tools():
    return {
        "web_search": {"func": lambda q: web_search.search(q), "description": "Search the web for a query."},
        "calculator": {"func": lambda expr: calculator.calculate(expr), "description": "Evaluate a math expression."},
        "get_time": {"func": lambda _: get_current_time.now(), "description": "Get the current time."},
    }


TEST_QUERIES = [
    "What is ReAct agent? Give a short definition.",
    "Calculate 15 * (2 + 3). Show result.",
    "What's the current UTC time?",
    "Who wrote 'Pride and Prejudice'? Provide year.",
    "What's 1024 divided by 4?",
]


def run_experiment(provider: str = "huggingface"):
    client = create_llm_client(provider)
    tools = make_tools()
    agent = Agent(client, tools)

    results = {"cot": [], "tot": []}
    for style in ["cot", "tot"]:
        print(f"\n=== Running style: {style} ===\n")
        for q in TEST_QUERIES:
            print(f"-- Query: {q}")
            out = agent.run(q, style=("cot" if style == "cot" else "tot"))
            print("Final Answer:", out["final"])
            results[style].append(out)

    # Simple comparison
    print("\n=== Summary of differences between CoT and ToT ===\n")
    for i, q in enumerate(TEST_QUERIES):
        a = results["cot"][i]["final"]
        b = results["tot"][i]["final"]
        same = a.strip() == b.strip()
        print(f"Query {i+1}: same_answer={same}\n  CoT: {a}\n  ToT: {b}\n")


if __name__ == "__main__":
    run_experiment()
