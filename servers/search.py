import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tavily import TavilyClient
from mcp.server.fastmcp import FastMCP
from config import SEARCH_RESULTS_LIMIT, TAVILY_API_KEY

mcp = FastMCP("search-server")

@mcp.tool()
async def search_web(query: str) -> str:
    """Search the web using Tavily and return results."""

    client = TavilyClient(api_key=TAVILY_API_KEY)
    response = client.search(query=query, max_results=SEARCH_RESULTS_LIMIT)

    results = []
    for r in response.get("results", []):
        results.append(
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Content: {r['content']}"
        )

    if not results:
        return "No results found."

    return "\n\n".join(results)

if __name__ == "__main__":
    mcp.run()