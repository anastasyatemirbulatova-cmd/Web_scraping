# Habr Parser

Парсер свежих статей с Хабра (`https://habr.com/ru/all/`).

- Фильтрация по ключевым словам (в configurable списке `KEYWORDS`).
- Вариант 1: фильтрация по preview-информации (заголовок + краткое описание).
- Вариант 2: фильтрация по полному тексту статьи.

## Установка

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.venv\\Scripts\\activate   # Windows

pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

Вывод в консоль:

```text
<дата> – <заголовок> – <ссылка>
```

## Структура

- `main.py` — основной скрипт.
- `requirements.txt` — зависимости.
- `.gitignore` — исключения для Git.

## Примечания

- Не выкладывай `.venv` и `.env` в репозиторий.
- Ключевые слова можно менять в начале скрипта.