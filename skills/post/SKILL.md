# Skill: post

Создание поста для Telegram канала.

## Workflow

### 1. Поиск информации
Используй web_search для поиска актуальной информации по теме.

### 2. Поиск фото через Unsplash
Выполни bash команду:
```bash
UNSPLASH_ACCESS_KEY="api-key" python3 /root/Bot/scripts/unsplash_search.py "keywords in english" 3
```

Запомни значения url_regular из результата — это URL фотографий.

### 3. Написание текста
Напиши пост на русском:
- 300-800 символов
- HTML форматирование: <b>жирный</b>, <i>курсив</i>
- Умеренно эмодзи
- БЕЗ хештегов
- БЕЗ источников
- БЕЗ "Фото: Unsplash"

### 4. Отправка превью админу
⚠️ ВАЖНО: НЕ используй telegram tool!

Выполни bash команду (замени значения):
```bash
BOT_TOKEN="token" python3 /root/Bot/scripts/send_media_group.py "user_tg_id" "ТЕКСТ ПОСТА ЗДЕСЬ" "URL_ФОТО_1" "URL_ФОТО_2" "URL_ФОТО_3"
```

### 5. Ожидание ответа
- "ок", "да", "пост", "публикуй" → публикуй в канал
- Другой текст → это правки, исправь и повтори шаг 4

### 6. Публикация в канал
```bash
BOT_TOKEN="token" python3 /root/Bot/scripts/send_media_group.py "channel_tg_id" "ТЕКСТ ПОСТА" "URL1" "URL2" "URL3"
```

## Запрещено

- НЕ используй telegram tool для отправки фото
- НЕ придумывай URL — только реальные из unsplash_search.py
- НЕ отправляй фото и текст отдельно
