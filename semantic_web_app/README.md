# Semantic Music Explorer 🎵

Explore, search, and visualize music data semantically! Built with FastAPI, RDF, MySQL, and a modern responsive frontend. Fetches 500+ songs from iTunes, stores in DB, and lets you search by song, artist, album, or genre.

## 🚀 Setup & Run

### 1. MySQL Setup

1. Install MySQL server (kalau belum ada)
2. Buat database:
   ```sql
   CREATE DATABASE semantic_web_app;
   ```
3. (Optional) Edit user/password MySQL di `backend/db.py` kalau beda

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

### 4. Open Frontend (langsung buka di browser)

Buka file `frontend/index.html` di browser (tidak perlu build, no server needed).

Halaman:

- Home & search: `index.html`
- Song detail & semantic: `detail.html?id=...`
- Knowledge graph: `graph.html`
- SPARQL: `sparql.html`

---

## 🔌 API Endpoints

- `GET /api/songs` — List all songs
- `GET /api/songs/{id}` — Song info, RDF triples, related songs (artist, album, genre)
- `GET /api/sparql?q=...` — Run SPARQL query

---

## 🧠 Ontology

Lihat: `backend/ontology/ontology.owl`
Namespace: `http://example.org/music#`
Classes: Song, Artist, Album, Genre
Properties: performedBy, partOfAlbum, hasGenre, year, title

---

## 🔥 Fitur Utama

- Search lagu, artist, album, genre (autocomplete & flexible)
- Klik lagu → lihat detail, RDF triples, relasi semantik
- Visualisasi knowledge graph (vis-network)
- Semua data & relasi diambil dari RDF graph, bukan hardcode
- Responsive & modern UI (Tailwind, Inter font)
- Data di-cache di MySQL, fetch iTunes API cuma sekali

---

## 🧪 Contoh SPARQL Query

Semua lagu & judul:

```sparql
PREFIX : <http://example.org/music#>
SELECT ?song ?title WHERE {
  ?song a :Song .
  ?song :title ?title .
}
```

Lagu lain dengan artist sama:

```sparql
PREFIX : <http://example.org/music#>
SELECT ?song ?title WHERE {
  :Song_123 :performedBy ?artist .
  ?song :performedBy ?artist .
  ?song :title ?title .
  FILTER(?song != :Song_123)
}
```

---

## ⚠️ Notes

<<<<<<< HEAD
=======
- Pastikan MySQL running & config di `backend/db.py` sudah benar
- Kalau ganti user/password, update juga di `backend/db.py`
- Data di-cache di MySQL (biar nggak spam API)
- Semua RDF digenerate dari data asli, bukan dummy
- Semua file frontend ada watermark & prompt anti-clone (lihat comment di atas file HTML)

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

>>>>>>> 490de2f46803ad705fd840015dd50e8891b46523
- Make sure MySQL is running and DB config in `backend/db.py` is correct.
- If you change DB user/password, update `backend/db.py`.
- Data is cached in MySQL for speed (no API spam).
- All RDF is generated dynamically from real API data.
```
