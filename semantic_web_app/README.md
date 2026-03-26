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

- Make sure MySQL is running and DB config in `backend/db.py` is correct.
- If you change DB user/password, update `backend/db.py`.
- Data is cached in MySQL for speed (no API spam).
- All RDF is generated dynamically from real API data.
```
