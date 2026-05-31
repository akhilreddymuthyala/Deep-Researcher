import asyncio
from agent.orchestrator import run_agent
from agent.synthesizer import synthesize_report, save_as_docx
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

    # Save as Word document
    save_as_docx(query, report, "final_report.docx")
    print("\nReport saved to final_report.docx ✅")

if __name__ == "__main__":
    asyncio.run(main())