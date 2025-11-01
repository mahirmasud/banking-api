# 🏦 FastAPI In-Memory Banking System

A complete **Banking REST API** built with **FastAPI**, using an **in-memory architecture** (Python dictionary as storage).  
No external databases — data persists only during runtime.

---

## 🚀 Features

✅ **User Authentication**
- Register & Login with JWT tokens

✅ **Account Management**
- Create unique bank accounts
- View balances and transaction history

✅ **Transactions**
- Deposit, Withdraw, Transfer funds
- Real-time balance updates
- Persistent in-memory data during runtime

✅ **Architecture**
- Singleton in-memory store with thread-safe access
- Modular folder structure
- Auto-generated Swagger Docs at `/docs`

---

## ⚙️ Tech Stack
- **FastAPI**
- **Pydantic**
- **PyJWT / fastapi-jwt-auth**
- **Uvicorn**
- **Docker / Docker Compose**

---

## 📁 Project Structure
```
banking-api/
├── app/
│   ├── main.py
│   ├── models/
│   │   └── schemas.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── accounts.py
│   │   └── transactions.py
│   ├── core/
│   │   ├── memory.py
│   │   └── security.py
│   └── utils/
│       └── helpers.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 🐳 Run with Docker (Recommended)

Make sure Docker is installed, then run:

```bash
docker-compose up --build
```

Access API docs:
```
http://localhost:8000/docs
```

Stop the service:
```bash
docker-compose down
```

---

## 💻 Run Locally (Without Docker)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open browser at:
```
http://127.0.0.1:8000/docs
```

---

## 🧠 In-Memory Store

```python
{
    "users": {},
    "accounts": {},
    "transactions": []
}
```

Data is stored in-memory (no DB). It resets when the app stops.

---

## 🔒 Example API Flow

1. **Register** → `/register`
2. **Login** → `/login` → Get JWT Token
3. **Create Account** → `/account/create`
4. **Deposit/Withdraw/Transfer** → respective endpoints
5. **View History** → `/transactions/{account_id}`

---

## 🧰 Optional Enhancements
- Add middleware logging (request/response time)
- Add unit tests with `pytest`
- Load example data on startup

---

## 🧑‍💻 Author
Developed by **mahirmasud**  
