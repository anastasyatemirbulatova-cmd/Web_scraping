import requests
from bs4 import BeautifulSoup
import time

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

def normalize_text(text: str) -> str:
    return text.lower()

def contains_keyword(text: str, keywords: list[str]) -> bool:
    text_norm = normalize_text(text)
    return any(kw in text_norm for kw in keywords)

def get_article_full_text(article_url: str) -> str:
    resp = requests.get(article_url)
    if resp.status_code != 200:
        return ""
    soup = BeautifulSoup(resp.text, "lxml")

    article_tag = soup.find("article", class_="tm-article")
    if article_tag is None:
        return ""

    body = article_tag.find(class_="tm-article-body")
    if body is None:
        body = article_tag

    full_text = body.get_text(separator=" ", strip=True)
    return full_text

def parse_habr_all_with_full_text():
    url = "https://habr.com/ru/all/"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    article_items = soup.find_all("a", class_="tm-title__link")
    print(f"Найдено статей на главной: {len(article_items)}")

    articles = []
    checked_count = 0

    for i, a in enumerate(article_items):
        span = a.find("span")
        if span is None:
            continue
        title = span.get_text(strip=True)

        href = a.get("href")
        if not href:
            continue
        link = "https://habr.com" + href if href.startswith("/") else href

        article_tag = a.find_parent("article")
        if article_tag is None:
            continue
        time_tag = article_tag.find("time")
        if time_tag is None:
            continue

        datetime_attr = time_tag.get("datetime")
        date_str = datetime_attr[:10] if datetime_attr else time_tag.get_text(strip=True)

        preview_text = title
        snippet_text = article_tag.find(class_="tm-article-snippet__post-text")
        if snippet_text:
            preview_text += " " + snippet_text.get_text(strip=True)

        if i < 3:
            print(f"Пример статьи (preview):")
            print(f"  дата: {date_str}")
            print(f"  заголовок: {title}")
            print(f"  ссылка: {link}")
            print(f"  preview_text: {preview_text[:200]}")
            print(f"  содержит ли ключевое слово (preview): {contains_keyword(preview_text, KEYWORDS)}")
            print()

        if not contains_keyword(preview_text, KEYWORDS):
            continue

        checked_count += 1
        full_text = get_article_full_text(link)
        if not full_text:
            print(f"Не удалось получить полный текст для: {link}")
            continue

        if i < 3:
            print(f"Пример статьи (полный текст):")
            print(f"  ссылка: {link}")
            print(f"  длина полного текста: {len(full_text)}")
            print(f"  содержит ли ключевое слово (full): {contains_keyword(full_text, KEYWORDS)}")
            print()

        if contains_keyword(full_text, KEYWORDS):
            articles.append((date_str, title, link))
        else:
            print(f"Статья прошла preview, но не прошла по полному тексту: {link}")

        time.sleep(0.3)

    print(f"Проверено статей по полному тексту: {checked_count}")
    print(f"Подходящих статей по полному тексту: {len(articles)}")
    return articles

def main():
    articles = parse_habr_all_with_full_text()
    print("Список подходящих статей:")
    for date_str, title, link in articles:
        print(f"{date_str} – {title} – {link}")

if __name__ == "__main__":
    main()