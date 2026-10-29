# Тестовое Recruto

1. Код на `/` — новый при каждом обновлении.
2. Код на `/auth/` — только после логина; после обновления страницы сессия сбрасывается.

## Запуск

```bash
cp .env.example .env   # заполнить AUTH_*, SESSION_SECRET, PORT
docker compose up -d --build
```

Остановка: `docker compose down`.
