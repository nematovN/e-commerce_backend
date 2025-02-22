# E-Commerce Backend

![GitHub repo size](https://img.shields.io/github/repo-size/nematovN/e-commerce_backend)
![GitHub contributors](https://img.shields.io/github/contributors/nematovN/e-commerce_backend)
![GitHub last commit](https://img.shields.io/github/last-commit/nematovN/e-commerce_backend)
![GitHub stars](https://img.shields.io/github/stars/nematovN/e-commerce_backend?style=social)
![GitHub forks](https://img.shields.io/github/forks/nematovN/e-commerce_backend?style=social)
![GitHub license](https://img.shields.io/github/license/nematovN/e-commerce_backend)


## 📌 Overview
This is a backend service for an e-commerce platform built using Django and Django REST Framework (DRF). The API provides user authentication, product management, pagination, filtering, and admin functionalities.

## 🛠️ Features
- **User Authentication**: JWT-based authentication with login and registration.
- **Role Management**: Admin and regular users.
- **Product Management**: CRUD operations for products.
- **Pagination & Filtering**: Optimized data retrieval.
- **Comment & Likes**: Users can comment on and like products.
- **Admin Panel**: Secure admin functionalities.

## 🚀 Technologies Used
- **Python** - Main programming language
- **Django** - Web framework
- **Django REST Framework (DRF)** - API development
- **PostgreSQL** - Database
- **JWT (SimpleJWT)** - Authentication
- **Docker** - Containerization

## 📂 Project Structure
```
ecommerce_backend/
│── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│── shop/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│── manage.py
│── requirements.txt
```

## 🔧 Installation & Setup

### Prerequisites
Make sure you have the following installed:
- Python 3.9+
- PostgreSQL
- Docker (Optional, for containerization)

### Clone the Repository
```bash
git clone https://github.com/nematovN/ecommerce_backend.git
cd ecommerce_backend
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Up Environment Variables
Copy the `.env.example` file and rename it to `.env`. Then, configure your database credentials inside `.env`.

### Run Migrations
```bash
python manage.py migrate
```

### Create a Superuser
```bash
python manage.py createsuperuser
```

### Start the Development Server
```bash
python manage.py runserver
```

## 🐳 Run with Docker
```bash
docker-compose up --build
```

## 📌 API Endpoints
| Method | Endpoint             | Description         |
|--------|----------------------|---------------------|
| POST   | `/api/auth/register/` | User registration  |
| POST   | `/api/auth/login/`    | User login         |
| GET    | `/api/products/`      | List all products  |
| GET    | `/api/products/{id}/` | Retrieve a product |
| POST   | `/api/products/`      | Create a product   |
| PUT    | `/api/products/{id}/` | Update a product   |
| DELETE | `/api/products/{id}/` | Delete a product   |
| POST   | `/api/products/{id}/like/` | Like a product |
| POST   | `/api/products/{id}/comment/` | Comment on a product |

## 🛠 Contribution
1. Fork the repository
2. Create a new branch (`feature/new-feature`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to GitHub (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## ✉️ Contact
For any inquiries or issues, please contact [Nematov Nemat](nemat8954@gmail.com).

