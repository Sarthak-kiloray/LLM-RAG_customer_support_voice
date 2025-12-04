# ingest.py (new version that uses your functions)

import os

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from fetch_utils import fetch_website_contents, fetch_website_links  # or inline them

load_dotenv()

PERSIST_DIR = "chroma_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

SEED_URLS = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
 
]


def crawl_and_collect(seed_urls: list[str], max_pages: int = 20) -> list[Document]:

    seen = set()
    docs: list[Document] = []

    to_visit = list(seed_urls)

    while to_visit and len(seen) < max_pages:
        url = to_visit.pop(0)
        if url in seen:
            continue
        seen.add(url)

        try:
            print(f"[CRAWL] Fetching {url}")
            text = fetch_website_contents(url)

            print(f"[DEBUG] Raw text from {url} (len={len(text.strip())}):")
            print(text[:400].replace("\n", " "), "...\n")

            if not text or len(text.strip()) < 50:
                print(f"[SKIP] Too little text at {url}")
                continue

            docs.append(Document(page_content=text, metadata={"source": url}))

            # OPTIONAL: get more links from this page (depth 1 crawl)
            # links = fetch_website_links(url)
            # for link in links:
                # if link.startswith("https://your-docs-site.com/docs") and link not in seen:
                #     to_visit.append(link)

        except Exception as e:
            print(f"[ERROR] {url}: {e}")

    print(f"[CRAWL] Collected {len(docs)} documents.")
    return docs


def build_knowledge_base():
    docs = crawl_and_collect(SEED_URLS, max_pages=20)
    if not docs:
        print("[WARN] No docs collected, nothing to index.")
        return

    for i, d in enumerate(docs[:5]):
        print("=" * 80)
        print(f"[DOC {i}] source={d.metadata.get('source')}")
        print(d.page_content[:400].replace("\n", " "), "...")
        print("=" * 80)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(docs)
    print(f"[SPLIT] Generated {len(chunks)} chunks.")

    for i, ch in enumerate(chunks[:10]):
        print(f"[CHUNK {i}] src={ch.metadata.get('source')}")
        print(ch.page_content[:300].replace("\n", " "), "...")
        print("-" * 60)

    embeddings = OpenAIEmbeddings()
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )
    print(f"[DONE] Indexed {len(chunks)} chunks into {PERSIST_DIR}")


if __name__ == "__main__":
    build_knowledge_base()
