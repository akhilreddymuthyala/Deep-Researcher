import httpx
from mcp.server.fastmcp import FastMCP
from config import SEARCH_RESULTS_LIMIT

# Create MCP server
mcp = FastMCP("search-server")

@mcp.tool()
async def search_web(query: str) -> str:
    """Search the web using DuckDuckGo and return results."""
    
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
    
    results = []

    # Abstract (direct answer)
    if data.get("Abstract"):
        results.append(f"Summary: {data['Abstract']}")

    # Related topics
    for topic in data.get("RelatedTopics", [])[:SEARCH_RESULTS_LIMIT]:
        if "Text" in topic:
            results.append(f"- {topic['Text']}")

    if not results:
        return "No results found."

    return "\n".join(results)


if __name__ == "__main__":
    mcp.run()