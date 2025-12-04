import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}


def fetch_website_contents(url: str, max_chars: int | None = None) -> str:

    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    body = soup.body
    if body:
        for irrelevant in body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = body.get_text(separator="\n", strip=True)
    else:
        text = soup.get_text(separator="\n", strip=True)

    full = (title + "\n\n" + text).strip()

    if max_chars:
        return full[:max_chars]
    return full


def fetch_website_links(url: str) -> list[str]:
  
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "html.parser")
    raw_links = [link.get("href") for link in soup.find_all("a") if link.get("href")]

    # Resolve relative links
    links = [urljoin(url, href) for href in raw_links]
    return links
