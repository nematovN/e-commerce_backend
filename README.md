# E-Commerce Backend

🚀 **Django REST Framework (DRF) asosida qurilgan e-commerce backend**

Bu loyiha **[Figma eCommerce UI Kit](https://www.figma.com/design/My44GoSUIQMJHZEtlDZdXJ/Figma-ecommerce-UI-Kit-(web-%26-mobile)-(Community)?node-id=0-1&p=f&t=1tiJd543foBMZurO-0)** dizayni asosida ishlab chiqildi va to'liq DRF orqali API yaratildi.

## 📌 Xususiyatlar

- 🔐 **Autentifikatsiya & Avtorizatsiya** (Login, Register, JWT Token)
- 🏷️ **Mahsulotlar** (Ro'yxat, Tafsilotlar, Izlash, Filtrlash, Saralash)
- 🛍️ **Brendlar & Kategoriyalar**
- ⭐ **Foydalanuvchi fikrlari** (Comment qo'shish, o'chirish, ko'rish)
- ❤️ **Like tizimi** (Mahsulotlarni yoqtirish va yoqtirishdan chiqarish)
- 📷 **Rasmlar bilan ishlash**
- ⚡ **Maxsus takliflar (Deals)**

## 🛠 Texnologiyalar

- **Backend**: Django, Django REST Framework (DRF)
- **Ma'lumotlar bazasi**: PostgreSQL
- **Autentifikatsiya**: JWT
- **Versiya nazorati**: Git & GitHub

## 🔧 O'rnatish

### 1️⃣. Repository'ni klonlash
```bash
  git clone https://github.com/nematovN/e-commerce_backend.git
  cd e-commerce_backend
```

### 2️⃣. Virtual muhit yaratish va faollashtirish
```bash
  python -m venv .venv  # Virtual environment yaratish
  source .venv/bin/activate  # Linux & Mac
  .venv\Scripts\activate  # Windows
```

### 3️⃣. Kerakli kutubxonalarni o‘rnatish
```bash
  pip install -r requirements.txt
```

### 4️⃣. Ma'lumotlar bazasini sozlash
```bash
  python manage.py migrate
  python manage.py createsuperuser  # Admin yaratish
```

### 5️⃣. Serverni ishga tushirish
```bash
  python manage.py runserver
```

## 📡 API Endpointlar

| Endpoint | Method | Tavsif |
|----------|--------|---------|
| `/api/register/` | `POST` | Foydalanuvchi ro'yxatdan o'tkazish |
| `/api/login/` | `POST` | Login qilish (JWT Token) |
| `/api/user/` | `GET` | Foydalanuvchi profili |
| `/api/products/` | `GET` | Mahsulotlar ro'yxati |
| `/api/products/{id}/` | `GET` | Mahsulot tafsilotlari |
| `/api/products/{id}/comments/` | `GET` | Mahsulotga yozilgan izohlar |
| `/api/products/{id}/comments/add/` | `POST` | Izoh qo‘shish |
| `/api/comments/{id}/delete/` | `DELETE` | Izohni o‘chirish |
| `/api/products/{id}/like/` | `POST` | Like bosish |
| `/api/products/{id}/unlike/` | `DELETE` | Likeni olib tashlash |

👉 **Barcha endpointlar uchun batafsil dokumentatsiya:** `http://127.0.0.1:8000/swagger/`

## 🎯 Muallif

👨‍💻 **Nematov** - Backend Developer

📌 **GitHub**: [nematovN](https://github.com/nematovN)
