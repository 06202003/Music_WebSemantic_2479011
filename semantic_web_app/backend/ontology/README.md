# Music Ontology - Dokumentasi

## Daftar Isi

1. [Pengenalan](#pengenalan)
2. [Struktur Ontologi](#struktur-ontologi)
3. [Kelas Utama](#kelas-utama)
4. [Properti Object](#properti-object)
5. [Properti Data](#properti-data)
6. [SWRL Rules & Inference](#swrl-rules--inference)
7. [Individu/Instance](#individuinstance)
8. [Contoh Query SPARQL](#contoh-query-sparql)
9. [Cara Menggunakan](#cara-menggunakan)

---

## Pengenalan

`music_runtime.ttl` adalah sebuah ontologi **RDF (Resource Description Framework)** berbentuk Turtle yang dirancang untuk merepresentasikan data musik secara semantik. Ontologi ini memungkinkan:

- **Penyimpanan data musik** terstruktur (lagu, artis, album, genre, dll)
- **Inferensi otomatis** menggunakan SWRL (Semantic Web Rule Language) rules
- **Query semantik** dengan SPARQL
- **Klasifikasi dinamis** lagu berdasarkan atribut (ClassicSong, TrendingSong, HitSong)

**Format**: Turtle (TTL) - format RDF yang readable oleh manusia
**Namespace Utama**: `http://example.org/music#`

---

## Struktur Ontologi

Ontologi ini terdiri dari beberapa lapisan:

```
┌─────────────────────────────────┐
│   ANNOTATION PROPERTIES          │ (Metadata untuk ontologi)
├─────────────────────────────────┤
│   OBJECT PROPERTIES              │ (Relasi antar entity)
├─────────────────────────────────┤
│   DATA PROPERTIES                │ (Atribut dengan nilai literal)
├─────────────────────────────────┤
│   CLASSES                        │ (Kategori entity)
├─────────────────────────────────┤
│   SWRL RULES                     │ (Rule inferensi otomatis)
├─────────────────────────────────┤
│   INDIVIDUALS                    │ (Instance/data konkret)
└─────────────────────────────────┘
```

---

## Kelas Utama

### Core Classes

| Kelas      | Deskripsi                                                         |
| ---------- | ----------------------------------------------------------------- |
| `Song`     | Lagu/musik individual                                             |
| `Album`    | Kumpulan lagu yang dirilis bersama                                |
| `Artist`   | Musisi/pembuat musik                                              |
| `Genre`    | Jenis/kategori musik (Pop, Rock, Jazz, dll)                       |
| `Mood`     | Suasana hati yang ditimbulkan musik (Energetic, Melancholic, dll) |
| `Event`    | Acara musik (konser, festival)                                    |
| `Country`  | Negara asal artis/event                                           |
| `Language` | Bahasa dalam lagu                                                 |
| `Era`      | Periode waktu (1990s, 2000s, 2010s, 2020s)                        |
| `Playlist` | Koleksi lagu yang dikurasi                                        |

### Subclasses & Inferred Classes

#### Artist Classifications

```
Artist
├── SoloArtist (Artis solo)
├── BandArtist (Kelompok musik)
└── CollaborativeArtist (Artis yang sering kolaborasi)
```

#### Song Classifications (Inferred)

```
Song
├── ClassicSong (Lagu klasik: releaseYear ≤ 2005)
├── TrendingSong (Lagu trending: popularityScore > 80)
└── HitSong (Lagu hit: TrendingSong + durationSeconds > 180)
```

#### Event Classifications

```
Event
├── LiveEvent (Acara live performance)
└── FestivalEvent (Festival musik)
```

#### Album Classifications

```
Album
└── MultiGenreAlbum (Album dengan 2+ genre)
```

---

## Properti Object

### Relasi Artis-Lagu

| Properti       | Domain | Range  | Deskripsi                        |
| -------------- | ------ | ------ | -------------------------------- |
| `performsSong` | Artist | Song   | Artis melakukan/menyanyikan lagu |
| `performedBy`  | Song   | Artist | Lagu dinyanyikan oleh artis      |

### Relasi Lagu-Album

| Properti       | Domain | Range | Deskripsi                        |
| -------------- | ------ | ----- | -------------------------------- |
| `partOfAlbum`  | Song   | Album | Lagu merupakan bagian dari album |
| `containsSong` | Album  | Song  | Album berisi lagu                |

### Relasi Musik

| Properti            | Domain     | Range  | Deskripsi                      |
| ------------------- | ---------- | ------ | ------------------------------ |
| `hasGenre`          | Song/Album | Genre  | Memiliki genre musik           |
| `hasMood`           | Song       | Mood   | Memiliki suasana hati tertentu |
| `albumPrimaryGenre` | Album      | Genre  | Genre utama album              |
| `albumByArtist`     | Album      | Artist | Album dibuat oleh artis        |

### Relasi Kolaborasi & Rekomendasi

| Properti               | Domain | Range  | Deskripsi                             |
| ---------------------- | ------ | ------ | ------------------------------------- |
| `collaboratesWith`     | Artist | Artist | Artis berkolaborasi dengan artis lain |
| `frequentCollaborator` | Artist | Artist | Kolaborator yang sering               |
| `relatedByArtist`      | Song   | Song   | Lagu terkait melalui artis yang sama  |
| `recommendedWith`      | Song   | Song   | Lagu yang direkomendasikan bersama    |
| `similarGenreTo`       | Genre  | Genre  | Genre serupa                          |

### Relasi Konteks

| Properti          | Domain      | Range    | Deskripsi                 |
| ----------------- | ----------- | -------- | ------------------------- |
| `belongsToEra`    | Song/Artist | Era      | Milik periode tertentu    |
| `fromCountry`     | Artist      | Country  | Artis berasal dari negara |
| `hostCountry`     | Event       | Country  | Event diadakan di negara  |
| `hasLanguage`     | Song        | Language | Lagu menggunakan bahasa   |
| `featuredInEvent` | Song/Artist | Event    | Ditampilkan dalam event   |

### Relasi Pengaruh

| Properti       | Domain | Range  | Deskripsi                   |
| -------------- | ------ | ------ | --------------------------- |
| `influencedBy` | Artist | Artist | Terpengaruh oleh artis lain |
| `sampledFrom`  | Song   | Song   | Sampling dari lagu lain     |

---

## Properti Data

### Properti Artis

| Properti                 | Tipe        | Deskripsi            |
| ------------------------ | ----------- | -------------------- |
| `artistName`             | xsd:string  | Nama artis           |
| `collaborationFrequency` | xsd:integer | Frekuensi kolaborasi |
| `collaborationType`      | xsd:string  | Jenis kolaborasi     |

### Properti Lagu

| Properti          | Tipe        | Deskripsi                     |
| ----------------- | ----------- | ----------------------------- |
| `title`           | xsd:string  | Judul lagu                    |
| `releaseYear`     | xsd:integer | Tahun rilis                   |
| `durationSeconds` | xsd:integer | Durasi lagu dalam detik       |
| `popularityScore` | xsd:integer | Skor popularitas (0-100)      |
| `bpm`             | xsd:integer | Tempo musik (beat per minute) |
| `explicitFlag`    | xsd:boolean | Lagu eksplisit atau tidak     |

### Properti Lokasi

| Properti      | Tipe       | Deskripsi   |
| ------------- | ---------- | ----------- |
| `countryName` | xsd:string | Nama negara |

### Properti Teknis

| Properti    | Tipe         | Deskripsi          |
| ----------- | ------------ | ------------------ |
| `source`    | xsd:string   | Sumber data        |
| `fetchedAt` | xsd:dateTime | Waktu data diambil |

---

## SWRL Rules & Inference

SWRL Rules memungkinkan ontologi untuk membuat kesimpulan otomatis berdasarkan data yang ada.

### 1. **Klasifikasi Lagu Klasik**

```
IF Song.releaseYear ≤ 2005
THEN Song rdf:type ClassicSong
```

Lagu yang dirilis pada atau sebelum 2005 secara otomatis diklasifikasikan sebagai ClassicSong.

### 2. **Klasifikasi Lagu Trending**

```
IF Song.popularityScore > 80
THEN Song rdf:type TrendingSong
```

Lagu dengan skor popularitas di atas 80 diklasifikasikan sebagai TrendingSong.

### 3. **Klasifikasi Lagu Hit**

```
IF Song rdf:type TrendingSong AND Song.durationSeconds > 180
THEN Song rdf:type HitSong
```

Lagu yang trending DAN berdurasi lebih dari 180 detik adalah HitSong (lagu sukses).

### 4. **Rekomendasi Berdasarkan Mood**

```
IF Song1.hasMood = Mood AND Song2.hasMood = Mood
THEN Song1.recommendedWith = Song2
```

Lagu dengan suasana yang sama secara otomatis saling direkomendasikan.

### 5. **Kolaborasi Artis**

```
IF Song.performedBy = Artist1 AND Song.performedBy = Artist2
THEN Artist1.collaboratesWith = Artist2
```

Jika 2 artis tampil di lagu yang sama, mereka secara otomatis dianggap berkolaborasi.

### 6. **Klasifikasi Kolaboratif Artis**

```
IF Artist.collaboratesWith = ?otherArtist (count ≥ 1)
THEN Artist rdf:type CollaborativeArtist
```

Artis yang berkolaborasi diklasifikasikan sebagai CollaborativeArtist.

### 7. **Album Multi-Genre**

```
IF Album.hasGenre = Genre1 AND Album.hasGenre = Genre2 (Genre1 ≠ Genre2)
THEN Album rdf:type MultiGenreAlbum
```

Album dengan 2 atau lebih genre adalah MultiGenreAlbum.

### 8. **Propagasi Genre**

```
IF Song.hasGenre = Genre AND Song.relatedByArtist = Song2
THEN Song2.hasGenre = Genre
```

Genre dari satu lagu dipropagasi ke lagu terkait oleh artis yang sama.

---

## Individu/Instance

### Kategori Instance

#### Genre

- `Genre_indie_pop` - Indie Pop
- `Genre_alternative` - Alternatif
- `Genre_pop` - Pop
- `Genre_rock` - Rock
- `Genre_electronic` - Elektronik
- `Genre_folk` - Folk
- `Genre_jazz` - Jazz
- `Genre_hip_hop` - Hip Hop
- `Genre_classical` - Klasik
- `Genre_reggae` - Reggae
- `Genre_country` - Country

#### Mood

- `Mood_reflective` - Reflektif/merenung
- `Mood_energetic` - Energik
- `Mood_melancholic` - Melankolis
- `Mood_uplifting` - Penuh semangat
- `Mood_mysterious` - Misterius
- `Mood_dance` - Dance
- `Mood_romantic` - Romantis
- `Mood_aggressive` - Agresif

#### Artist

- `Artist_demo_solo` - Solo artist (contoh)
- `Artist_demo_band` - Band (contoh)
- `Artist_indie_legend` - Indie legend
- `Artist_electronic_master` - Master elektronik
- `Artist_rock_band` - Rock band
- `Artist_jazz_virtuoso` - Jazz virtuoso
- `Artist_folk_ensemble` - Folk ensemble
- `Artist_classical_composer` - Composer klasik

#### Song (Contoh dengan Klasifikasi)

```
ClassicSong (releaseYear ≤ 2005):
- Song_vintage_groove
- Song_golden_era
- Song_old_school_jam

TrendingSong (popularityScore > 80):
- Song_modern_hit
- Song_chart_topper
- Song_summer_anthem

HitSong (TrendingSong + duration > 180s):
- Song_blockbuster_epic
- Song_viral_masterpiece

Mood-based Recommendations:
- Song_melancholic_blues & Song_melancholic_soul (keduanya melancholic)
- Song_uplifting_sunrise & Song_uplifting_dawn (keduanya uplifting)
```

#### Album

- `Album_demo_semantic_reflections`
- `Album_demo_timeless_waves`
- Ratusan album lainnya dengan nama dari artis ternama

#### Event

- `Event_Jakarta_Night_2026` - Event di Jakarta 2026
- `Event_Tokyo_Festival_2026` - Festival di Tokyo 2026
- `Event_Seoul_Concert_2026` - Konser di Seoul 2026
- `Event_Berlin_Fest_2025` - Festival di Berlin 2025

---

## Contoh Query SPARQL

### Query 1: Temukan semua ClassicSong

```sparql
PREFIX music: <http://example.org/music#>

SELECT ?song ?year WHERE {
  ?song rdf:type music:ClassicSong ;
        music:releaseYear ?year .
}
ORDER BY ASC(?year)
```

### Query 2: Temukan TrendingSong

```sparql
PREFIX music: <http://example.org/music#>

SELECT ?song ?popularity WHERE {
  ?song rdf:type music:TrendingSong ;
        music:popularityScore ?popularity .
}
ORDER BY DESC(?popularity)
```

### Query 3: Rekomendasi Lagu Berdasarkan Mood

```sparql
PREFIX music: <http://example.org/music#>

SELECT ?song1 ?song2 ?mood WHERE {
  ?song1 music:recommendedWith ?song2 ;
         music:hasMood ?mood .
}
```

### Query 4: Kolaborasi Artis

```sparql
PREFIX music: <http://example.org/music#>

SELECT ?artist ?collaborators WHERE {
  ?artist rdf:type music:CollaborativeArtist ;
          music:collaboratesWith ?collaborators .
}
```

### Query 5: Album dengan Multiple Genre

```sparql
PREFIX music: <http://example.org/music#>

SELECT ?album ?genreCount ?genres WHERE {
  ?album rdf:type music:MultiGenreAlbum .
  {
    SELECT ?album (COUNT(DISTINCT ?genre) as ?genreCount)
                  (GROUP_CONCAT(?genre; separator=", ") as ?genres)
    WHERE {
      ?album music:hasGenre ?genre .
    }
    GROUP BY ?album
  }
}
```

### Query 6: Lagu Berkualitas Tinggi (HitSong)

```sparql
PREFIX music: <http://example.org/music#>

SELECT ?song ?popularity ?duration WHERE {
  ?song rdf:type music:HitSong ;
        music:popularityScore ?popularity ;
        music:durationSeconds ?duration .
}
```

### Query 7: Artis dari Negara Tertentu

```sparql
PREFIX music: <http://example.org/music#>

SELECT ?artist ?artistName ?country WHERE {
  ?artist music:fromCountry ?country ;
          music:artistName ?artistName ;
          rdf:type music:Artist .
  ?country music:countryName "Indonesia" .
}
```

---

## Cara Menggunakan

### 1. **Dengan Protégé (Desktop RDF/OWL Editor)**

```bash
# Download Protégé dari: https://protege.stanford.edu/
# Buka file: music_runtime.ttl
# Aktifkan reasoner untuk melihat inferensi
# Tools > SPARQL Query untuk menjalankan query
```

### 2. **Dengan Python (RDFLib)**

```python
from rdflib import Graph, Namespace, RDF, RDFS

# Load ontology
g = Graph()
g.parse("music_runtime.ttl", format="turtle")

# Query
MUSIC = Namespace("http://example.org/music#")
for song in g.subjects(RDF.type, MUSIC.ClassicSong):
    print(f"Classic Song: {song}")
```

### 3. **Dengan Flask/Backend (aplikasi ini)**

```python
# File: backend/rdf_service.py dan swrl_service.py
# Sudah terintegrasi untuk query dinamis
# API endpoint untuk query SPARQL
```

### 4. **Query di Frontend**

- Akses `http://localhost:8000/sparql.html`
- Tulis query SPARQL
- Lihat hasil dengan visualisasi interaktif

---

## File Terkait

| File                       | Deskripsi                      |
| -------------------------- | ------------------------------ |
| `music_runtime.ttl`        | Ontologi utama (format Turtle) |
| `music_runtime_v2.ttl`     | Versi extended ontologi        |
| `music_runtime.properties` | Konfigurasi properti           |
| `ontology.owl`             | Format OWL alternatif          |
| `SWRL_SETUP_GUIDE.md`      | Panduan setup SWRL             |
| `test_suite/`              | Suite test untuk inferensi     |

---

## Tips & Best Practices

✅ **DO:**

- Selalu aktifkan reasoner sebelum query SPARQL untuk melihat hasil inferensi
- Gunakan DESCRIBE untuk melihat semua properti suatu instance
- Batch multiple queries untuk performance lebih baik

❌ **DON'T:**

- Jangan modify ontologi tanpa backup
- Jangan skip reasoner jika mengharapkan inferensi bekerja
- Jangan lupa include PREFIX dalam query SPARQL

---

## Referensi

- [RDF Primer](https://www.w3.org/TR/rdf-primer/)
- [Turtle Format](https://www.w3.org/TR/turtle/)
- [SPARQL Query Language](https://www.w3.org/TR/sparql11-query/)
- [SWRL: A Semantic Web Rule Language](https://www.w3.org/Submission/SWRL/)
- [Protégé Documentation](https://protege.stanford.edu/)

---

**Dibuat**: April 2026  
**Format**: Markdown  
**Status**: Documentation untuk Music Ontology v2
