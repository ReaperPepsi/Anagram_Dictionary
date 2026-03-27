# 🔤 Anagram Dictionary API

A backend API built with FastAPI that allows users to create and manage their own anagram dictionaries, with authentication and structured grouping of words.

---

## 🚀 Features

* User authentication (JWT-based)
* Create and manage personal anagram dictionaries
* Group words by sorted key (anagram logic)
* Prevent duplicate entries per user
* Logging system (auth + DB operations)
* Clean and scalable architecture

---

## 🧠 How it works

Each word is transformed into a **key_word** by sorting its characters.

Example:

```
listen → eilnst
silent → eilnst
enlist → eilnst
```

All words sharing the same `key_word` belong to the same anagram group.

---

## 🔐 Authentication

The API uses JWT tokens.

### Login

```
POST /login
```

**Response:**

```json
{
  "access_token": "your_token_here",
  "token_type": "bearer"
}
```

Use the token in requests:

```
Authorization: Bearer <token>
```

---

## 📦 Endpoints

### ➕ Add words

```
POST /words/
```

**Request:**

```json
{
  "words": ["listen", "silent", "hello"]
}
```

**Response:**

```json
{
  "added": ["listen", "silent", "hello"],
  "skipped": []
}
```

---

### 📚 Get all anagram groups

```
GET /words/
```

**Response:**

```json
[
  {
    "key_word": "eilnst",
    "words": ["listen", "silent"]
  }
]
```

---

### 🔍 Get specific anagram group

```
GET /list/{word}
```

**Example:**

```
GET /list/listen
```

**Response:**

```json
[
  {
    "key_word": "eilnst",
    "words": ["listen", "silent"]
  }
]
```

---

## 🗄️ Database Design

* Built using **SQLModel**
* Each entry contains:

  * `word`
  * `key_word`
  * `user_id`

### Constraints:

* Unique `(user_id, word)`
* Ensures no duplicate words per user

---

## 🪵 Logging System

The application includes a basic logging system:

* `auth.log` → authentication events (login, errors)
* `db.log` → database operations (insert, read, errors)

Logs include:

* timestamp
* level
* source
* message

---

## ⚙️ Tech Stack

* FastAPI
* SQLModel
* PostgreSQL
* JWT Authentication
* Python Logging

---

## ▶️ Run the project

```bash
git clone <repo>
cd Anagram_Dictionary
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 📌 API Docs

After running the app:

👉 http://127.0.0.1:8000/docs

---

## 🧩 Future Improvements

* Pagination for large datasets
* Rate limiting
* Better error handling
* Unit & integration testing
* Docker support

---

## 🧠 What I learned

* Designing REST APIs with FastAPI
* Working with SQLModel and database constraints
* JWT authentication flow
* Logging architecture
* Structuring a backend project

---

## ⭐ Project Status

Active development 🚀
