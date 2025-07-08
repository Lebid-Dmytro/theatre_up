# 🎭 Cinema Up API

**Cinema Up** is a RESTful API for a stage performance booking website.  
Despite the name, this platform is not for movies, but for **live plays and theater performances**.  
Users can browse upcoming shows, view detailed information, and make reservations.  
Administrators can manage performances, plays, and seating.

---

## 🔧 Features

- JWT authentication
- User registration and profile management
- Performance and play management
- Reservation system with ticket handling
- Upload images for plays
- Admin panel
- Interactive API documentation via Swagger and Redoc

---

## 📂 Endpoints Overview

### 🔐 Authentication

- `POST /api/user/register/` — Register a new user  
- `POST /api/user/login/` — Obtain JWT token  
- `GET /api/user/me/` — Get current user info  
- `PUT/PATCH /api/user/me/` — Update user profile  
- `POST /api/user/token/` — Get access and refresh tokens  
- `POST /api/user/token/refresh/` — Refresh access token  
- `POST /api/user/token/verify/` — Verify JWT token  

---

### 🎭 Plays

- `GET /api/plays/` — List all plays  
- `POST /api/plays/` — Create a new play  
- `GET /api/plays/{id}/` — Retrieve play details  
- `PUT/PATCH /api/plays/{id}/` — Update play  
- `DELETE /api/plays/{id}/` — Delete play  
- `POST /api/plays/{id}/upload_image/` — Upload play image  

---

### ⏰ Performances

- `GET /api/performances/` — List all performances  
- `GET /api/performances/{id}/` — Performance details  

---

### 🎟️ Reservations

- `GET /api/reservations/` — View all reservations  
- `POST /api/reservations/` — Create a new reservation  
- `GET /api/reservations/{id}/` — Get reservation details  
- `PUT/PATCH /api/reservations/{id}/` — Update reservation  
- `DELETE /api/reservations/{id}/` — Delete reservation  

---

## 🛠️ Installation with Docker

1. **Clone the repository**

```bash
git clone https://github.com/your-username/cinema_up.git
cd cinema_up
docker-compose up --build
