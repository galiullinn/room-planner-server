# Room Planner API

Создание файла для локальных переменных
```bash
# Windows
Copy-Item .env.example .env
# Linux / macOS
cp .env.example .env
```

Генерация ключа:
```bash
openssl rand -hex 32
```

Запуск контейнеров:
```bash
docker compose up --build -d
```

Проверка статусов контейнеров:
```bash
docker compose ps
```

Остановка контейнеров:
```bash
docker compose down
```

Остановка с удалением данных
```bash
docker compose down -v
```

- Документация API: http://localhost:8000/docs
- Веб-консоль управления S3-бакетами (SILO): http://localhost:9001
- Веб-интерфейс для управления PostgreSQL (Adminer): http://localhost:8080