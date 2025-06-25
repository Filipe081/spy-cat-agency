# 🐾 Spy Cat Agency - Management System

Gerenciamento de gatos espiões, suas missões e alvos.

---

## 🇬🇧 ENGLISH VERSION

### 📋 Project Overview

This project was developed as part of a technical assessment. It includes a FastAPI backend and a Next.js frontend to manage spy cats, their missions, and assigned targets.

### 🧠 Technologies

- ✅ Backend: FastAPI + SQLite  
- ✅ Frontend: Next.js (TypeScript)  
- ✅ External API: [TheCatAPI](https://api.thecatapi.com/v1/breeds)

---

### ⚙️ How to Run

#### ▶️ Backend (FastAPI)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn main:app --reload
