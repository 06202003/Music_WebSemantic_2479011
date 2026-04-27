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

### 5. Python Frontend Option

Kalau mau FE juga jalan dari Python, pakai Streamlit frontend:

```bash
streamlit run frontend/streamlit_app.py
```

Atau jalankan backend + frontend sekaligus dari satu launcher:

```bash
python run_python_stack.py
```

Python frontend ini tetap memakai backend FastAPI yang sama di `backend/main.py`, jadi data, RDF, dan SPARQL tetap terpusat.

### 6. SWRL View di Python

Di Streamlit frontend sekarang ada tab **SWRL** untuk melihat rule dari ontology:

- `GET /api/swrl/summary` — ringkasan rule, variabel, dan daftar rule
- `GET /api/swrl/rules` — daftar rule SWRL dalam bentuk structured data

Catatan: view ini menampilkan definisi SWRL dari file ontology. Eksekusi reasoning tetap dilakukan lewat Protege / reasoner OWL, bukan di Streamlit.

---

## 🔌 API Endpoints

- `GET /api/songs` — List all songs
- `GET /api/songs/{id}` — Song info, RDF triples, related songs (artist, album, genre)
- `GET /api/sparql?q=...` — Run SPARQL query
- `GET /api/semantic/search?q=...&limit=30` — Semantic search (natural-language-like keyword query)
- `GET /api/semantic/health` — RDF semantic validation summary and graph readiness status
- `GET /api/swrl/summary` — SWRL rule summary from `backend/ontology/music_runtime.ttl`
- `GET /api/swrl/rules` — SWRL rule list from `backend/ontology/music_runtime.ttl`

---

## 🧠 Ontology

Lihat: `backend/ontology/ontology.owl`
Namespace: `http://example.org/music#`
Classes: Song, Artist, Album, Genre, Country
Properties: performedBy, partOfAlbum, hasGenre, releaseYear, title, collaborationType, collaboratesWith, fromCountry, relatedByArtist, frequentCollaborator, source, fetchedAt

---

## ✨ Semantic Upgrade (v2)

- Stable entity URI strategy with external IDs (when available)
- Provenance metadata in RDF (`source`, `fetchedAt`)
- Artist collaboration modeling (`feat`, `duo`, `trio`, `quartet`, `group`)
- Lightweight semantic inference:
  - `relatedByArtist` for songs sharing artist
  - `frequentCollaborator` for repeated artist collaboration pairs
- SPARQL safety guardrails:
  - Read-only query restriction
  - Default `LIMIT` injection (for `SELECT` without `LIMIT`)
  - Query timeout protection

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

```
