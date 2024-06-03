#!/bin/bash

# Зупинка та видалення наявних контейнерів, якщо вони є
docker-compose down

# Побудова образу Docker та запуск контейнерів
docker-compose up --build -d

# Очікування запуску контейнерів
sleep 10

# Перевірка статусу контейнерів
docker-compose ps

echo "Application is deployed and running."

