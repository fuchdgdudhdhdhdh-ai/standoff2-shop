# Standoff 2 Shop Bot

Телеграм-бот-магазин: покупка голды, подписки, буст аккаунта, поддержка.
Работает на [aiogram 3](https://docs.aiogram.dev/), готов к деплою на [Render](https://render.com/).

## Возможности

- 🖼 Главное меню — фото + текст + кнопки (`/start`)
- 💰 Купить голду, ⭐ Купить подписку, 🚀 Буст аккаунта, 🛠 Поддержка
- При нажатии любой кнопки-раздела: предыдущее сообщение бота удаляется,
  отправляется новое фото с описанием и кнопкой «Оплатить» (пока заглушка)
- Быстрые команды: `/gold`, `/subscription`, `/boost`, `/support`
- Все тексты и ссылки на фото редактируются в одном файле — `content.py`
- Автопинг: каждые 10 минут (настраивается) бот шлёт в указанный канал
  сообщение «✅ Бот активен»
- Встроенный health-check веб-сервер (нужен для деплоя на Render как Web Service)

## Структура проекта

```
standoff2_shop_bot/
├── bot.py                 # точка входа
├── config.py               # переменные окружения
├── content.py                # ⭐ РЕДАКТИРУЙТЕ ТУТ тексты и ссылки на фото
├── keyboards.py             # инлайн-клавиатуры
├── utils.py                  # отправка раздела + удаление предыдущего сообщения
├── heartbeat.py                # автопинг канала каждые N минут
├── handlers/
│   ├── menu.py                  # обработка кнопок
│   └── commands.py               # команды /gold /subscription /boost /support
├── requirements.txt
├── Procfile
├── render.yaml
├── .env.example
└── .gitignore
```

## 1. Настройка бота в Telegram

1. Создайте бота через [@BotFather](https://t.me/BotFather), получите `BOT_TOKEN`.
2. Создайте канал/группу, куда бот будет слать «я живой», добавьте бота туда админом.
3. Узнайте ID канала — перешлите любое сообщение из канала боту [@getidsbot](https://t.me/getidsbot)
   (или [@username_to_id_bot](https://t.me/username_to_id_bot)). Обычно выглядит как `-100xxxxxxxxxx`.
4. Узнайте свой `ADMIN_ID` через [@userinfobot](https://t.me/userinfobot).

## 2. Локальный запуск

```bash
git clone <ваш-репозиторий>
cd standoff2_shop_bot
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# заполните .env своими значениями

python bot.py
```

## 3. Публикация на GitHub

```bash
cd standoff2_shop_bot
git init
git add .
git commit -m "Initial commit: Standoff 2 shop bot"
git branch -M main
git remote add origin https://github.com/<ваш-логин>/<название-репозитория>.git
git push -u origin main
```

⚠️ Файл `.env` в `.gitignore` — токен на GitHub не попадёт. Это нормально,
переменные окружения задаются отдельно на Render (см. ниже).

## 4. Деплой на Render

### Вариант А — через render.yaml (Blueprint), автоматически
1. Зайдите на [render.com](https://render.com), New → Blueprint.
2. Укажите ваш GitHub-репозиторий — Render сам подхватит `render.yaml`.
3. Заполните переменные окружения (`BOT_TOKEN`, `ADMIN_ID`, `HEARTBEAT_CHANNEL_ID`,
   `SUPPORT_USERNAME`), которые запросит форма.
4. Нажмите Deploy.

### Вариант Б — вручную
1. New → Web Service → выберите репозиторий.
2. Runtime: Python 3.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python bot.py`
5. В разделе Environment добавьте переменные:
   - `BOT_TOKEN`
   - `ADMIN_ID`
   - `HEARTBEAT_CHANNEL_ID`
   - `HEARTBEAT_INTERVAL_MINUTES` = `10`
   - `SUPPORT_USERNAME`
6. Deploy.

### Важно про бесплатный план Render
Бесплатные Web Service на Render «засыпают» после ~15 минут без входящих
HTTP-запросов. Наш бот шлёт исходящие сообщения (heartbeat), но это не
считается входящим запросом и не помешает сервису уснуть.

Чтобы бот не засыпал, добавьте бесплатный внешний пинг на его URL (Render выдаёт
адрес вида `https://standoff2-shop-bot.onrender.com`) через сервис вроде
[UptimeRobot](https://uptimerobot.com/) с интервалом 5 минут — он будет дергать
`/` (health-check), и Render не будет усыплять сервис. Либо используйте платный
план Render, где сервис не засыпает.

## 5. Редактирование текстов и фото

Откройте `content.py` — там 5 блоков (`MAIN_MENU`, `GOLD`, `SUBSCRIPTION`, `BOOST`,
`SUPPORT`) и текст заглушки оплаты `PAYMENT_STUB`. У каждого блока два поля:

- `"photo"` — прямая ссылка на изображение
- `"text"` — HTML-текст описания (поддерживаются теги `<b>`, `<i>`, и т.д.)

После правки закоммитьте и запушьте изменения — Render передеплоит бота автоматически.

## 6. Подключение реальной оплаты

Кнопка «Оплатить» сейчас вызывает заглушку — всплывающее окно с текстом из
`PAYMENT_STUB` в `content.py`. Логика находится в `handlers/menu.py`,
функция `cb_pay`. Когда будете готовы подключить платёжную систему (ЮKassa,
CryptoBot, Telegram Payments и т.п.), замените тело этой функции на реальный
вызов API платёжного провайдера.
