import asyncio
from pathlib import Path
from app.rag.ingest import ingest_markdown

async def main():
    text = Path("data/benefits.md").read_text(encoding="utf-8")
    result = await ingest_markdown(text, source="data/benefits.md")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
