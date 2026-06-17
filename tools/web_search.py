"""Simple web_search tool stub.

Provides a `search(query)` function that returns deterministic stubbed
results. Does not perform network calls so it's safe for offline runs
and testing.
"""
from datetime import datetime


def search(query: str):
	"""Return a list of fake search result dicts for the given query.

	Each result is a dict with `title`, `snippet`, and `url` keys.
	"""
	ts = datetime.utcnow().isoformat() + "Z"
	return [
		{
			"title": f"Result 1 for: {query}",
			"snippet": f"A concise summary for '{query}' (stub) - {ts}",
			"url": f"https://example.com/search?q={query.replace(' ', '+')}&r=1",
		},
		{
			"title": f"Result 2 for: {query}",
			"snippet": f"Another brief snippet about '{query}' (stub)",
			"url": f"https://example.com/search?q={query.replace(' ', '+')}&r=2",
		},
		{
			"title": f"Result 3 for: {query}",
			"snippet": f"Additional context for '{query}' (stub)",
			"url": f"https://example.com/search?q={query.replace(' ', '+')}&r=3",
		},
	]


if __name__ == "__main__":
	print(search("what is ReAct agent"))
