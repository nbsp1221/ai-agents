import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
from common.configs import REQUESTS_USER_AGENT

def get_geeknews_articles(page: int = 1) -> Dict[str, Any]:
    """
    Fetches a list of article summaries from GeekNews for a given page.

    Args:
        page: The page number to fetch articles from (default: 1).

    Returns:
        dict: A dictionary indicating status.
              On success, it includes `page` and `articles` (a list of article summaries).
              On error, it includes an error `message` and `page`.
    """

    try:
        url = f"https://news.hada.io/?page={page}"
        headers = {
            "User-Agent": REQUESTS_USER_AGENT,
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        article_elements = soup.find_all("div", class_="topic_row")

        articles = []

        for article_element in article_elements:
            # Article ID
            article_id = article_element.find("span", id=re.compile(r"^vote\d+")).get("id").replace("vote", "")

            # Title
            title = article_element.select_one("div.topictitle h1").get_text(strip=True)

            # Original source URL
            original_source_url = article_element.select_one("div.topictitle a").get("href")

            # Description
            description = article_element.select_one("div.topicdesc").get_text(strip=True)

            # Points
            points = int(article_element.select_one("div.topicinfo span").get_text(strip=True))

            # Author
            author = article_element.select_one("div.topicinfo a").get_text(strip=True)

            # Time ago
            time_ago = article_element.select_one("div.topicinfo").find_all(text=True, recursive=False)[1].strip()

            # Comments count
            comments_count = re.search(r'\d+', article_element.select_one("div.topicinfo a.u").get_text(strip=True))
            comments_count = int(comments_count.group()) if comments_count else 0

            articles.append({
                "id": article_id,
                "title": title,
                "original_source_url": original_source_url,
                "description": description,
                "points": points,
                "author": author,
                "time_ago": time_ago,
                "comments_count": comments_count
            })

        return {
            "status": "success",
            "page": page,
            "articles": articles
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch GeekNews articles: {str(e)}",
            "page": page
        }

def get_geeknews_article_content(article_id: str) -> Dict[str, Any]:
    """
    Fetches detailed content and metadata for a specific GeekNews article.
    This includes the article's title, main content (in both HTML and plain text), and other metadata.

    Args:
        article_id: The ID of the GeekNews article to fetch.

    Returns:
        dict: A dictionary indicating status.
              On success, it includes comprehensive article details (like title, content, author, points, etc.).
              On error, it includes an error `message`, `id`, and `page_url`.
    """

    page_url = f"https://news.hada.io/topic?id={article_id}"

    try:
        headers = {
            "User-Agent": REQUESTS_USER_AGENT,
        }
        response = requests.get(page_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Title
        title = "N/A"
        title_h1_el = soup.select_one("div.topic-table div.topictitle.link h1")
        if title_h1_el:
            title = title_h1_el.get_text(strip=True)
        else:
            title_head_el = soup.find("title")
            if title_head_el:
                title_head_text = title_head_el.get_text(strip=True)
                title = title_head_text.split("| GeekNews")[0].strip() if "| GeekNews" in title_head_text else title_head_text

        # Content
        content_html = ""
        content_text = ""
        content_el = soup.find("span", id="topic_contents")
        if content_el:
            content_html = content_el.decode_contents()
            content_text = content_el.get_text(separator="\n", strip=True)

        # Original source URL
        original_source_url = None
        original_source_url_el = soup.select_one("div.topictitle.link > a.bold.ud")
        if original_source_url_el and original_source_url_el.has_attr("href"):
            href_value = original_source_url_el["href"]
            original_source_url = f"https://news.hada.io{href_value}" if href_value.startswith("/") else href_value

        # Author
        author = "N/A"
        author_el = soup.select_one("div.topic-table div.topicinfo a[href^='/user?id=']")
        if author_el:
            author = author_el.get_text(strip=True)

        # Points
        points = 0
        points_el = soup.select_one(f"span#tp{article_id}")
        if points_el:
            points_text = points_el.get_text(strip=True)
            points_text_match = re.search(r"\d+", points_text)
            if points_text_match:
                points = int(points_text_match.group())

        # Time ago
        time_ago = "N/A"
        time_ago_el = soup.select_one("div.topic-table div.topicinfo span[title]")
        if time_ago_el:
            time_ago = time_ago_el.get_text(strip=True)

        # Comments count
        comments_count = 0
        comments_count_el = soup.select_one("div#comment_thread")
        if comments_count_el:
            comments_count = len(comments_count_el.select("div.comment_row"))

        return {
            "status": "success",
            "id": article_id,
            "page_url": page_url,
            "title": title,
            "content_html": content_html,
            "content_text": content_text,
            "original_source_url": original_source_url,
            "author": author,
            "points": points,
            "time_ago": time_ago,
            "comments_count": comments_count
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch GeekNews article content: {str(e)}",
            "id": article_id,
            "page_url": page_url
        }
