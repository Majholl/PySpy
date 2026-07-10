

# Spy Game

این پروژه یک پروژه بکندی برای بازی اسپای با استفاده از 
- FastAPI
- WebSocket

است 

این پروژه امکان ایجاد اتاق بازی، ورود مالک، ورود کاربران، تنظیم تعداد جاسوس‌ها، شروع بازی و ارسال پیام‌های لحظه‌ای به کاربران را فراهم می‌کند.

## ویژگی‌ها

- ورود مالک بازی
- ورود کاربران به بازی
- تنظیم تعداد جاسوس‌ها
- تنظیم اینکه مالک در بازی شرکت کند یا نه
- ارتباط زنده با WebSocket
- شروع بازی و توزیع نقش‌ها
- نمایش کلمه برای بازیکنان عادی و پیام "You are spy" برای جاسوس‌ها

## تکنولوژی‌های استفاده‌شده

- Python
- FastAPI
- Uvicorn
- WebSocket
- JSON

## ساختار پروژه

```text
spy/
├── src/
│   ├── main.py
│   ├── utils.py
│   └── words.json
└── README.md


```

## پیش‌نیازها

- Python 3.9 یا بالاتر
- pip

## نصب
```

1- python -m venv .venv 
2- .venv\Scripts\activate
3- pip install fastapi uvicorn
```


## اجرای پروژه
```
bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

پس از اجرا، می‌توانید از این آدرس‌ها استفاده کنید:

- Swagger UI: http://localhost:8000/docs


## جریان استفاده

1. مالک با اطلاعات زیر وارد می‌شود:
   - username: `admin`
   - password: `admin`

2. پس از لاگین، یک توکن برای مالک ایجاد می‌شود.

3. کاربران با `POST /join/user` وارد می‌شوند.

4. مالک با WebSocket به اتاق متصل می‌شود.

5. پس از شروع بازی، نقش‌ها به کاربران داده می‌شود.

## Endpointها

### احراز هویت مالک
- `POST /auth/owner`

### دریافت داده‌های بازی
- `GET /data`

### تنظیم تعداد جاسوس‌ها
- `POST /setting/spys/`

### تنظیم حضور مالک در بازی
- `POST /setting/ownerin/`

### ورود کاربر
- `POST /join/user`

### شروع بازی
- `POST /game/start`

### پایان بازی
- `POST /game/end`

### WebSocket
- `WS /ws/owner/{token}`
- `WS /ws/user/{token}`

## Postman collection
برای استفاده از اندپوینت ها به  

Spy-kms.postman_collection.json

مراجعه کنید

## نکته

این پروژه در حال حاضر یک نسخه‌ی ساده و اولیه از بازی Spy است و برای توسعه‌ی بیشتر مناسب می‌باشد.

## مجوز

این پروژه برای استفاده‌ی شخصی و آموزشی مناسب است.

