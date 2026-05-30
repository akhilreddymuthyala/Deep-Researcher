from openai import AsyncOpenAI
from config import OPENROUTER_API_KEY, BASE_URL, MODEL

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL
)

async def synthesize_report(query: str, findings_dir: str = "findings") -> str:
    """Read all findings and compile into a final research report."""
    
    import os
    
    # Read all saved findings
    all_findings = []
    
    if os.path.exists(findings_dir):
        for filename in os.listdir(findings_dir):
            filepath = os.path.join(findings_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                all_findings.append(f"--- {filename} ---\n{content}")
    
    if not all_findings:
        return "No findings to synthesize."
    
    combined = "\n\n".join(all_findings)
    
    # Final LLM call — compile report
    response = await client.chat.completions.create(
        model=MODEL,
        max_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a research analyst. "
                    "Given raw research findings, write a clean, structured, "
                    "insightful report. Include key findings, trends, and conclusions."
                )
            },
            {
                "role": "user",
                "content": f"Query: {query}\n\nFindings:\n{combined}"
            }
        ]
    )
    
    return response.choices[0].message.content