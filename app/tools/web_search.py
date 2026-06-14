from ddgs import DDGS


def web_search(query: str, max_results: int = 3) -> list[str]:
    results = []

    with DDGS() as ddgs:
        search_results = ddgs.text(query, max_results=max_results)

        for result in search_results:
            title = result.get("title", "")
            body = result.get("body", "")
            url = result.get("href", "")

            results.append(f"Title: {title}\nSummary: {body}\nURL: {url}")

    return results