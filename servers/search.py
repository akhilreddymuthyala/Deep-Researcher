import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from mcp.server.fastmcp import FastMCP
from config import SEARCH_RESULTS_LIMIT

mcp = FastMCP("search-server")

@mcp.tool()
async def search_web(query: str) -> str:
    """Search the web using DuckDuckGo HTML search and return results."""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers=headers,
            follow_redirects=True
        )

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, "lxml")

    results = []
    for result in soup.select(".result__body")[:SEARCH_RESULTS_LIMIT]:
        title = result.select_one(".result__title")
        snippet = result.select_one(".result__snippet")
        url = result.select_one(".result__url")

        if title and snippet:
            results.append(
                f"Title: {title.get_text(strip=True)}\n"
                f"URL: {url.get_text(strip=True) if url else 'N/A'}\n"
                f"Snippet: {snippet.get_text(strip=True)}"
            )

    if not results:
        return "No results found."

    return "\n\n".join(results)

if __name__ == "__main__":
    mcp.run()