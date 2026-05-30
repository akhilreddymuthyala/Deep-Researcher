import asyncio
from agent.orchestrator import run_agent
from agent.synthesizer import synthesize_report
from config import FINDINGS_DIR

async def main():
    query = input("Enter research query: ")
    
    print("\n--- Phase 1: Researching ---")
    await run_agent(query)
    
    print("\n--- Phase 2: Synthesizing Report ---")
    report = await synthesize_report(query, FINDINGS_DIR)
    
    print("\n========== FINAL REPORT ==========")
    print(report)
    print("===================================")
    
    # Save final report
    with open("final_report.txt", "w", encoding="utf-8") as f:
        f.write(f"Query: {query}\n\n{report}")
    
    print("\nReport saved to final_report.txt")

if __name__ == "__main__":
    asyncio.run(main())