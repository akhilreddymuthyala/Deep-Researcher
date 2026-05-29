import os
from mcp.server.fastmcp import FastMCP
from config import FINDINGS_DIR

mcp = FastMCP("filesystem-server")

@mcp.tool()
async def save_finding(filename: str, content: str) -> str:
    """Save research finding to a local file."""
    
    os.makedirs(FINDINGS_DIR, exist_ok=True)
    
    filepath = os.path.join(FINDINGS_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    return f"Saved to {filepath}"


@mcp.tool()
async def read_finding(filename: str) -> str:
    """Read a saved research finding from file."""
    
    filepath = os.path.join(FINDINGS_DIR, filename)
    
    if not os.path.exists(filepath):
        return f"File not found: {filepath}"
    
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@mcp.tool()
async def list_findings() -> str:
    """List all saved research findings."""
    
    if not os.path.exists(FINDINGS_DIR):
        return "No findings saved yet."
    
    files = os.listdir(FINDINGS_DIR)
    
    if not files:
        return "No findings saved yet."
    
    return "\n".join(files)


if __name__ == "__main__":
    mcp.run()