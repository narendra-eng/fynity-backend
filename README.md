# Backend Setup

Clone backend

```bash
git clone https://github.com/narendra-eng/fynity-backend.git
```

Go to backend

```bash
cd backend
```

Create venv

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install

```bash
pip install -r requirements.txt
```

Create `.env`

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/fynity_backend_db
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
```

Run migration

```bash
flask db upgrade
```

Start backend

```bash
python run.py
```