# Fynity Backend

## Prerequisites

Before running the project, install:

- Python 3.10+
- PostgreSQL
- Git

---

## Clone Repository

```bash
git clone https://github.com/narendra-eng/fynity-backend.git
cd fynity-backend
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Activate (Windows)

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create PostgreSQL Database

Create a database named:

```text
fynity_backend_db
```

---

## Create .env file

Create a file named `.env` in the project root.

Example:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/fynity_backend_db
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
```

---

## Run Database Migration

```bash
flask db upgrade
```

---

## Run Backend

```bash
python run.py
```

Backend runs at:

```
http://localhost:5000
```