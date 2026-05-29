from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from config import OPENROUTER_API_KEY, BASE_URL, MODEL

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL
)

async def get_tools(session: ClientSession) -> list:
    """Fetch available tools from MCP server."""
    response = await session.list_tools()
    tools = []
    for tool in response.tools:
        tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        })
    return tools


async def run_agent(query: str):
    """Main agent loop — thinks, calls tools, collects findings."""
    
    # Connect to all 3 MCP servers
    search_params  = StdioServerParameters(command="python", args=["servers/search.py"])
    scraper_params = StdioServerParameters(command="python", args=["servers/scraper.py"])
    fs_params      = StdioServerParameters(command="python", args=["servers/filesystem.py"])

    async with stdio_client(search_params) as (sr, sw), \
               stdio_client(scraper_params) as (scr, scw), \
               stdio_client(fs_params) as (fr, fw):

        async with ClientSession(sr, sw) as search_session, \
                   ClientSession(scr, scw) as scraper_session, \
                   ClientSession(fr, fw) as fs_session:

            # Initialize sessions
            await search_session.initialize()
            await scraper_session.initialize()
            await fs_session.initialize()

            # Collect all tools
            all_tools = (
                await get_tools(search_session) +
                await get_tools(scraper_session) +
                await get_tools(fs_session)
            )

            # Map tool name → session
            tool_session_map = {}
            for tool in await search_session.list_tools():
                tool_session_map[tool.name] = search_session
            for tool in await scraper_session.list_tools():
                tool_session_map[tool.name] = scraper_session
            for tool in await fs_session.list_tools():
                tool_session_map[tool.name] = fs_session

            # Agent loop
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a deep research agent. "
                        "Use search, scrape, and save tools to research the query thoroughly. "
                        "Save each finding. Stop when you have enough information."
                    )
                },
                {"role": "user", "content": query}
            ]

            print(f"\nResearching: {query}\n")

            while True:
                response = await client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=all_tools,
                    tool_choice="auto"
                )

                message = response.choices[0].message

                # No tool call = LLM done thinking
                if not message.tool_calls:
                    print("\nAgent finished.")
                    print(message.content)
                    break

                # Process each tool call
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = eval(tool_call.function.arguments)

                    print(f"Calling tool: {tool_name} with {tool_args}")

                    session = tool_session_map[tool_name]
                    result  = await session.call_tool(tool_name, tool_args)
                    result_text = result.content[0].text

                    # Add tool result back to messages
                    messages.append({"role": "assistant", "content": None, "tool_calls": [tool_call]})
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result_text
                    })