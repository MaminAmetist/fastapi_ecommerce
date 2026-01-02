# fastapi_ecommerce

Бэкенд e-commerce API на **FastAPI**, **SQLAlchemy** и **Pydantic**

REST API для интернет-магазина: пользователи, аутентификация, товары, категории, корзина и заказы.  
Проект построен с применением асинхронных запросов к базе и стандартной Swagger-документации.

---

## Возможности

- Регистрация и вход пользователей (JWT аутентификация)  
- CRUD для товаров, категорий 
- Просмотр списка товаров и фильтрация  
- Добавление/удаление товаров в корзине  
- Оформление заказов  
- Защищённые эндпоинты для авторизованных пользователей

---

## Быстрый старт

### 1. Клонирование

```bash
git clone https://github.com/MaminAmetist/fastapi_ecommerce.git
cd fastapi_ecommerce
```

2. Виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate         # Linux / macOS
# или
venv\Scripts\activate            # Windows
```

3. Установка зависимостей

```bash
pip install -r requirements.txt
```

## Настройка базы данных

В корне проекта создай файл .env и пропиши параметры подключения:
```bash
DATABASE_URL=postgresql+asyncpg://username:passwords@localhost:5432/name_db
SECRET_KEY=твой_секрет_ключ
YOOKASSA_SHOP_ID=xxxxxx
YOOKASSA_SECRET_KEY = live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Применение миграций
```bash
alembic upgrade head
```

## Запуск
```bash
uvicorn app.main:app --reload
```

Сервер будет доступен по умолчанию по ссылке http://127.0.0.1:8000

## Документация API

FastAPI автоматически генерирует Swagger и ReDoc:

Swagger UI: /docs

OpenAPI JSON: /openapi.json

ReDoc UI: /redoc

Пример: http://127.0.0.1:8000/docs

## Основные эндпоинты

Категории
```
Метод	URL	                        Описание
GET	/categories	                Список категорий
POST	/categories	                Создать категорию
PUT	/categories/{category_id}	Обновить категорию
DELETE	/categories/{category_id}	Удалить категорию
```
Товары
```
Метод	URL	                                Описание
GET	/products	                        Список товаров
GET	/products/category/{category_id}	Получить список товаров по категории
GET	/products/{product_id}	                Получить товар по id
PUT	/products/{product_id}	                Обновить товар
POST	/products	                        Создать товар
DELETE	/products/{product_id}	                Удалить товар
GET     /products/reviews                       Получить отзывы о товарах
POST    /products/reviews                       Создать отзыв
GET     /products/{product_id}/reviews          Получить отзывы о товаре по его id
DELETE	/products/reviews/{review_id}	        Удалить отзыв
```
Пользователи и аутентификация
```
Метод	URL	                Описание
POST	/users	                Регистрация
POST	/users/token	        Вход 
POST	/users/refresh-token	Получение рефреш-токена
```
Корзина
```
Метод	URL	                        Описание
GET     /cart                           Получить список товаров в корзине
DELETE	/cart	                        Удалить корзину
POST	/cart/items	                Добавить товар в корзину
PUT     /cart/items/{product_id}        Обновить данные о товаре 
DELETE	/cart/items/{product_id}	Удалить товар из корзины
```
Заказы
```
Метод	URL	                        Описание
POST	/orders/checkout	        Оформить заказ
GET	/orders/	                История заказов пользователя
GET	/orders/{order_id}	        Информация о заказе
```

(Если в проекте другие маршруты — дополни раздел)

### Примеры запросов
#### Регистрация
```bash
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "пароль123"
}
```

#### Логин и получение токена
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "пароль123"
}
```

#### Ответ:

```json
{
  "access_token": "eyJ…",
  "token_type": "bearer"
}
```