# Exp.md - Penjelasan Semantic Music Explorer dan TTL

## 1. Ringkasan Proyek

**Semantic Music Explorer** adalah web aplikasi yang menggabungkan:

- **Frontend statis** untuk pencarian, detail lagu, graph, dan SPARQL
- **Backend FastAPI** untuk API dan penyajian data semantik
- **RDF graph / ontology** untuk merepresentasikan data musik secara semantik
- **TTL (Turtle)** sebagai format utama ontologi dan aturan inferensi
- **SPARQL** untuk query data semantik

Tujuan utama aplikasi ini adalah membuat data musik tidak hanya tampil sebagai daftar biasa, tetapi sebagai **knowledge graph** yang bisa dipahami relasinya antar lagu, artis, album, genre, negara, dan mood.

---

## 2. Gambaran Web

Web ini terdiri dari beberapa halaman utama:

### `frontend/index.html`

Halaman utama untuk:

- mencari lagu, artis, album, dan genre
- melihat daftar lagu
- membuka detail semantic per lagu
- menuju halaman graph dan SPARQL

### `frontend/detail.html`

Halaman detail lagu, berisi:

- info dasar lagu
- RDF triples dari lagu tersebut
- lagu lain yang berelasi lewat artis, album, atau genre
- penjelasan semantic/semantic explanation

### `frontend/graph.html`

Halaman visualisasi knowledge graph yang menampilkan:

- node lagu, artis, album, dan genre
- relasi explicit dari RDF
- relasi inferred dari reasoning
- provenance data seperti source dan fetchedAt

### `frontend/sparql.html`

Halaman untuk menjalankan query SPARQL, termasuk template query seperti:

- SELECT
- ASK
- DESCRIBE
- CONSTRUCT

Halaman ini dibuat agar user bisa langsung menguji inferensi dari ontology.

### `frontend/streamlit_app.py`

Versi Python frontend yang memberikan tampilan tambahan, termasuk ringkasan SWRL.

---

## 3. Backend dan Alur Data

Backend utama ada di `backend/main.py` dan service pendukungnya:

- `backend/rdf_service.py`
- `backend/db.py`
- `backend/swrl_service.py`

Alurnya seperti ini:

1. Aplikasi start
2. Backend menginisialisasi database
3. RDF graph dibangun dari data lagu
4. Data diperkaya dengan relasi semantik
5. Frontend mengambil data melalui API FastAPI
6. User bisa mencari, membuka detail, menjalankan SPARQL, dan melihat graph

### Endpoint utama

- `GET /api/songs`
- `GET /api/songs/{id}`
- `GET /api/sparql?q=...`
- `GET /api/semantic/search?q=...&limit=30`
- `GET /api/semantic/health`
- `GET /api/swrl/summary`
- `GET /api/swrl/rules`

---

## 4. Sumber Data

Data lagu diambil dari:

- database cache MySQL `songs_cache`
- fallback fetch dari iTunes API jika cache belum tersedia

Setiap lagu diperkaya dengan atribut seperti:

- `id`
- `title`
- `artist`
- `album`
- `genre`
- `year`
- `country`
- `source`
- `fetched_at`

Ini penting karena TTL yang dibentuk bukan hanya menyimpan data statis, tetapi juga metadata provenance.

---

## 5. TTL yang Dibentuk

File ontology utama ada di:

- `backend/ontology/music_runtime.ttl`

File ini adalah definisi **Turtle RDF** yang menjadi basis semantik aplikasi. Di dalamnya ada:

- ontology declaration
- annotation properties
- object properties
- datatype properties
- class definitions
- SWRL rules
- named individuals

### Namespace utama

```turtle
@prefix : <http://example.org/music#> .
@prefix music: <http://example.org/music#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix swrl: <http://www.w3.org/2003/11/swrl#> .
@prefix swrlb: <http://www.w3.org/2003/11/swrlb#> .
```

### Struktur besar TTL

1. **Ontology header**
   - mendefinisikan ontology `music:MusicOntology`
   - menyimpan catatan query SPARQL internal dan eksternal

2. **Annotation properties**
   - `externalSparqlExample`
   - `internalSparqlExample`
   - `sparqlQueryPackage`

3. **Object properties**
   - relasi antar entity, misalnya `performedBy`, `hasGenre`, `recommendedWith`

4. **Datatype properties**
   - atribut literal, misalnya `title`, `releaseYear`, `popularityScore`

5. **Classes**
   - jenis-jenis entity seperti `Song`, `Artist`, `Album`, `Genre`, `Mood`, `Event`

6. **SWRL rules**
   - aturan inferensi untuk menghasilkan kelas dan relasi baru

7. **Individuals**
   - contoh data nyata/demonstration data untuk testing reasoning

---

## 6. Kelas Utama pada TTL

TTL ini memiliki kelas inti berikut:

- `Song`
- `Artist`
- `Album`
- `Genre`
- `Mood`
- `Country`
- `Language`
- `Era`
- `Event`
- `Playlist`

### Kelas turunan penting

- `ClassicSong`
- `TrendingSong`
- `HitSong`
- `MultiGenreAlbum`
- `CollaborativeArtist`
- `SoloArtist`
- `BandArtist`
- `LiveEvent`
- `FestivalEvent`

Kelas-kelas ini tidak hanya dideklarasikan, tetapi juga digunakan dalam reasoning dan query.

---

## 7. Object Properties

Object property dipakai untuk menghubungkan satu entity dengan entity lain.

### Contoh relasi penting

- `performedBy` dan `performsSong`
- `partOfAlbum` dan `containsSong`
- `hasGenre`
- `hasMood`
- `collaboratesWith`
- `recommendedWith`
- `relatedByArtist`
- `fromCountry`
- `belongsToEra`
- `featuredInEvent`

### Fungsi relasi ini

Relasi tersebut dipakai untuk:

- navigasi graph
- pencarian lagu terkait
- inferensi kolaborasi artis
- penelusuran lagu berdasarkan genre/mood
- pembentukan rekomendasi otomatis

---

## 8. Datatype Properties

Datatype property menyimpan nilai literal seperti string, integer, atau boolean.

### Contoh data property

- `title`
- `artistName`
- `releaseYear`
- `durationSeconds`
- `popularityScore`
- `bpm`
- `explicitFlag`
- `countryName`
- `source`
- `fetchedAt`

### Kenapa penting

Atribut literal ini dipakai untuk:

- klasifikasi lagu berdasarkan tahun rilis
- klasifikasi trending berdasarkan popularitas
- audit provenance data
- filter query SPARQL

---

## 9. SWRL Rules dan Inferensi

Bagian paling penting dari TTL ini adalah **SWRL rules**. Rules dipakai agar ontology bisa menghasilkan pengetahuan baru secara otomatis.

### Aturan yang dibentuk

#### 1. ClassicSong

Jika `releaseYear <= 2005`, maka lagu menjadi `ClassicSong`.

#### 2. TrendingSong

Jika `popularityScore > 80`, maka lagu menjadi `TrendingSong`.

#### 3. HitSong

Jika lagu sudah `TrendingSong` dan `durationSeconds > 180`, maka lagu menjadi `HitSong`.

#### 4. recommendedWith

Jika dua lagu punya mood yang sama, maka keduanya direkomendasikan satu sama lain.

#### 5. collaboratesWith

Jika dua artis tampil di lagu yang sama, maka mereka dianggap kolaborasi.

#### 6. CollaborativeArtist

Jika artis punya relasi kolaborasi, maka dia dikategorikan sebagai `CollaborativeArtist`.

#### 7. MultiGenreAlbum

Jika album punya dua genre atau lebih, maka menjadi `MultiGenreAlbum`.

#### 8. relatedByArtist

Jika dua lagu berasal dari artis yang sama, maka lagu-lagu itu saling terkait.

### Dampak inferensi

Karena rules ini, data yang awalnya hanya explicit triples bisa menghasilkan:

- kelas baru
- relasi baru
- graph yang lebih kaya
- hasil SPARQL yang lebih informatif

---

## 10. Individuals / Instance di TTL

TTL ini juga berisi banyak instance demonstrasi untuk menguji reasoning.

### Contoh instance

#### Genre

- `Genre_pop`
- `Genre_rock`
- `Genre_jazz`
- `Genre_folk`
- `Genre_electronic`

#### Mood

- `Mood_reflective`
- `Mood_energetic`
- `Mood_melancholic`
- `Mood_uplifting`

#### Artist

- `Artist_demo_solo`
- `Artist_demo_band`
- `Artist_indie_legend`
- `Artist_rock_band`

#### Song

- `Song_vintage_groove`
- `Song_golden_era`
- `Song_modern_hit`
- `Song_blockbuster_epic`
- `Song_melancholic_blues`
- `Song_uplifting_sunrise`

#### Album

- `Album_demo_semantic_reflections`
- `Album_demo_timeless_waves`

#### Event

- `Event_Jakarta_Night_2026`
- `Event_Tokyo_Festival_2026`
- `Event_Seoul_Concert_2026`

Instance-instance ini dipakai sebagai data uji untuk memastikan reasoning berjalan.

---

## 11. Cara TTL Dipakai di Web

TTL ini tidak berdiri sendiri. TTL dipakai oleh backend untuk:

- menjadi base graph ontology yang diload langsung dari `backend/ontology/music_runtime.ttl`
- membangun RDF graph gabungan antara ontology + data runtime
- menjawab query SPARQL
- menampilkan relasi lagu di halaman detail
- membentuk graph visual di halaman graph
- menyediakan ringkasan SWRL

### Contoh penggunaan di backend

- `/api/songs/{id}` mengembalikan info lagu, triples, relasi artist/album/genre, dan semantic explanation
- `/api/sparql` mengeksekusi query SPARQL terhadap graph
- `/api/swrl/summary` membaca ringkasan rule dari ontology

---

## 12. Contoh Query SPARQL

### Ambil semua lagu

```sparql
PREFIX music: <http://example.org/music#>
SELECT ?song ?title WHERE {
  ?song a music:Song .
  ?song music:title ?title .
}
```

### Ambil lagu klasik

```sparql
PREFIX music: <http://example.org/music#>
SELECT ?song ?year WHERE {
  ?song a music:ClassicSong ;
        music:releaseYear ?year .
}
```

### Ambil lagu trending

```sparql
PREFIX music: <http://example.org/music#>
SELECT ?song ?popularity WHERE {
  ?song a music:TrendingSong ;
        music:popularityScore ?popularity .
}
ORDER BY DESC(?popularity)
```

### Ambil relasi rekomendasi

```sparql
PREFIX music: <http://example.org/music#>
SELECT ?song1 ?song2 WHERE {
  ?song1 music:recommendedWith ?song2 .
}
```

---

## 13. Inti Arsitektur Semantik

Sederhananya, alur logikanya adalah:

**music_runtime.ttl -> RDF base graph -> data runtime dari DB/iTunes -> merged semantic catalog -> SWRL inference -> SPARQL query -> Frontend visualization**

Jadi web ini bukan sekadar katalog lagu. Ia adalah sistem semantik yang membuat data musik bisa:

- dihubungkan
- diperdalam maknanya
- dianalisis dengan rule
- divisualisasikan sebagai knowledge graph

---

## 14. Kesimpulan

`music_runtime.ttl` adalah fondasi semantik dari aplikasi ini. TTL tersebut mendefinisikan kelas, properti, aturan inferensi, dan data contoh untuk membentuk knowledge graph musik yang dapat dipakai oleh frontend dan backend.

Dokumen ini menjelaskan bagaimana seluruh web bekerja, bagaimana data mengalir, dan bagaimana ontology TTL membentuk logika semantiknya.
