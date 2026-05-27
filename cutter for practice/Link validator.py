import re


def is_youtube_url(url: str) -> bool:
    """
    проверяет является ли преерданная строка ссылкой на ЮТ ролик
    """
    # Паттерны для различных форматов YouTube ссылок
    youtube_patterns = [
        r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/',  # Основные домены
        r'(https?://)?(www\.)?youtube\.com/embed/',  # Embed ссылки
        r'(https?://)?youtu\.be/[a-zA-Z0-9_-]+',  # youtu.be сокращённые
    ]

    for pattern in youtube_patterns:
        if re.match(pattern, url, re.IGNORECASE):
            return True
    return False