# Smart Library – Semantic Search Engine

## 🚀 Setup & Run

### 1. MySQL Setup

- Install MySQL server (jika belum ada)
- Buat database:

```sql
CREATE DATABASE semantic_web_app;
```

- (Optional) Edit user/password MySQL di `backend/db.py` jika perlu

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Backend

```bash
uvicorn backend.main:app --reload
```

### 4. Open Frontend

Buka file `frontend/index.html` di browser (tidak perlu build).

- Book list: `index.html`
- Book detail & semantic: `detail.html?id=...`
- SPARQL: `sparql.html`

---

## 🔌 API Endpoints

- `GET /api/books` — List all books
- `GET /api/books/{id}` — Book info, RDF triples, related books (author & subject)
- `GET /api/sparql?q=...` — Run SPARQL query

---

## 🧠 Ontology

Lihat: `backend/ontology/ontology.owl`

Namespace: `http://example.org/smart-library#`

Classes: Book, Author, Subject
Properties: writtenBy, hasSubject, publishedYear, title

---

## 🔥 Semantic Features

- Klik buku → lihat info, RDF triples, buku lain dengan author/subject sama
- Semua relasi diambil dari RDF graph (bukan hardcode)

---

## 🧪 Example SPARQL Queries

# Semua buku dan judul

```
PREFIX : <http://example.org/smart-library#>
SELECT ?book ?title WHERE {
  ?book a :Book .
  ?book :title ?title .
}
```

# Buku lain dengan author sama

```
PREFIX : <http://example.org/smart-library#>
SELECT ?book ?title WHERE {
  :Book_OL1234567W :writtenBy ?author .
  ?book :writtenBy ?author .
  ?book :title ?title .
  FILTER(?book != :Book_OL1234567W)
}
```

# Buku lain dengan subject sama

```
PREFIX : <http://example.org/smart-library#>
SELECT ?book ?title WHERE {
  :Book_OL1234567W :hasSubject ?subject .
  ?book :hasSubject ?subject .
  ?book :title ?title .
  FILTER(?book != :Book_OL1234567W)
}
```

```

Get all authors:

```

SELECT ?author ?name WHERE {
?author a <http://example.org/ontology#Author> .
?author <http://example.org/ontology#title> ?name .
}

```

Get books published after 2000:

```

SELECT ?book ?title ?year WHERE {
?book a <http://example.org/ontology#Book> .
?book <http://example.org/ontology#title> ?title .
?book <http://example.org/ontology#publishedYear> ?year .
FILTER(?year > 2000)
}

```

---

## ⚠️ Notes

- Make sure MySQL is running and DB config in `backend/db.py` is correct.
- If you change DB user/password, update `backend/db.py`.
- Data is cached in MySQL for speed (no API spam).
- All RDF is generated dynamically from real API data.
```
