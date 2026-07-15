import requests
from bs4 import BeautifulSoup

# Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

def normalize_text(text: str) -> str:
    return text.lower()

def contains_keyword(text: str, keywords: list[str]) -> bool:
    text_norm = normalize_text(text)
    return any(kw in text_norm for kw in keywords)

def parse_habr_all():
    url = "https://habr.com/ru/all/"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    article_items = soup.find_all("a", class_="tm-title__link")
    print(f"Найдено статей на главной: {len(article_items)}")

    articles = []

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
            print(f"Пример статьи:")
            print(f"  дата: {date_str}")
            print(f"  заголовок: {title}")
            print(f"  ссылка: {link}")
            print(f"  preview_text: {preview_text[:200]}")
            print(f"  содержит ли ключевое слово: {contains_keyword(preview_text, KEYWORDS)}")
            print()

        if contains_keyword(preview_text, KEYWORDS):
            articles.append((date_str, title, link))

    print(f"Подходящих статей: {len(articles)}")
    return articles

def main():
    articles = parse_habr_all()
    print("Список подходящих статей:")
    for date_str, title, link in articles:
        print(f"{date_str} – {title} – {link}")

if __name__ == "__main__":
    main()