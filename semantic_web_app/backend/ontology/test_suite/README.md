# Music Ontology Test Suite

Complete testing framework for `music_runtime.ttl` SWRL inference rules and SPARQL queries.

## 📁 Test Structure

```
test_suite/
├── README.md (this file)
├── sparql_queries/
│   ├── 01_classic_song_tests.sparql
│   ├── 02_trending_song_tests.sparql
│   ├── 03_hit_song_tests.sparql
│   ├── 04_recommendations_tests.sparql
│   ├── 05_collaborations_tests.sparql
│   ├── 06_album_inference_tests.sparql
│   └── 07_comprehensive_tests.sparql
├── test_results.md
├── test_runner.py
├── quick_test_guide.md
└── example_test_data.ttl
```

## 🧪 How to Run Tests

### Method 1: Protege Manual Testing

1. Open Protege with `music_runtime.ttl`
2. Enable Reasoner: **Tools > Reasoner > HermiT > Start Reasoner**
3. Go to **SPARQL Query** tab
4. Copy-paste queries from `sparql_queries/` files
5. Click **Execute**
6. Record results in `test_results.md`

### Method 2: Python Test Runner (Automated)

```bash
cd d:\S2\WS\semantic_web_app\backend\ontology\test_suite
python test_runner.py
```

Results automatically saved to `test_results.md`

### Method 3: RDF4J REST API

```bash
# If using RDF4J server
curl -X POST http://localhost:8080/rdf4j-server/repositories/music/query \
  -H "Content-Type: application/sparql-query" \
  -d @sparql_queries/01_classic_song_tests.sparql
```

---

## ✅ Test Categories

| Category            | File                              | Tests | Expected Results                                                             |
| ------------------- | --------------------------------- | ----- | ---------------------------------------------------------------------------- |
| **ClassicSong**     | `01_classic_song_tests.sparql`    | 3     | ASK=TRUE, SELECT has 4 songs, DESCRIBE shows ClassicSong class               |
| **TrendingSong**    | `02_trending_song_tests.sparql`   | 3     | ASK=TRUE for multi-songs, SELECT lists 9+ trending songs                     |
| **HitSong**         | `03_hit_song_tests.sparql`        | 3     | ASK=TRUE, DESCRIBE shows HitSong class, SELECT returns 2+ hits               |
| **Recommendations** | `04_recommendations_tests.sparql` | 4     | ASK=TRUE for mood-based links, CONSTRUCT builds graph                        |
| **Collaborations**  | `05_collaborations_tests.sparql`  | 4     | ASK=TRUE for CollaborativeArtist, SELECT lists all collaborations            |
| **Album Inference** | `06_album_inference_tests.sparql` | 4     | albumByArtist inferred, albumPrimaryGenre inferred, MultiGenreAlbum detected |
| **Comprehensive**   | `07_comprehensive_tests.sparql`   | 5     | Aggregate counts, chain visualization, edge cases                            |

---

## 🎯 Key Test Scenarios

### Scenario 1: ClassicSong Classification

**Trigger:** releaseYear ≤ 2005  
**Test Song:** `Song_demo_timeless_echo` (1999)  
**Expected:** ClassicSong class inferred  
**Confidence:** ⭐⭐⭐⭐⭐ High (numeric comparison reliable)

### Scenario 2: TrendingSong Classification

**Trigger:** popularityScore > 80  
**Test Songs:** `Song_modern_hit` (89.5), `Song_chart_topper` (87.2)  
**Expected:** TrendingSong class inferred  
**Confidence:** ⭐⭐⭐⭐⭐ High

### Scenario 3: HitSong Classification

**Trigger:** TrendingSong + durationSeconds > 180  
**Test Song:** `Song_blockbuster_epic` (92.1 pop, 295s)  
**Expected:** Both TrendingSong + HitSong inferred  
**Confidence:** ⭐⭐⭐⭐⭐ High (chained inference)

### Scenario 4: Collaborative Artist Detection

**Trigger:** 2 artists on same song  
**Test Song:** `Song_demo_collab_bridge` (Aruna + North Tide)  
**Expected:** collaboratesWith property + CollaborativeArtist class  
**Confidence:** ⭐⭐⭐⭐⭐ High

### Scenario 5: Album-Artist Inference

**Trigger:** Songs in album performed by artist  
**Test:** `Album_demo_semantic_reflections` contains `Song_demo_reflection` by `Artist_demo_solo`  
**Expected:** albumByArtist property inferred  
**Confidence:** ⭐⭐⭐⭐ High

### Scenario 6: Album-Genre Inference

**Trigger:** Multiple genres on songs in album  
**Test:** `Album_demo_semantic_reflections` contains songs with indie_pop + alternative  
**Expected:** albumPrimaryGenre inferred for both genres, MultiGenreAlbum class triggered  
**Confidence:** ⭐⭐⭐⭐⭐ High

### Scenario 7: Mood-Based Recommendations

**Trigger:** Songs share same mood  
**Test:** `Song_demo_reflection` + `Song_demo_reflection_live` (both reflective)  
**Expected:** recommendedWith property inferred (symmetric)  
**Confidence:** ⭐⭐⭐⭐ High

---

## 📊 Test Execution Checklist

### Pre-Test

- [ ] Protege version 5.3+ installed
- [ ] SWRL plugin enabled
- [ ] `music_runtime.ttl` loaded
- [ ] HermiT reasoner available
- [ ] Test suite folder downloaded

### Test Phase

- [ ] Run `01_classic_song_tests.sparql` → Record results
- [ ] Run `02_trending_song_tests.sparql` → Record results
- [ ] Run `03_hit_song_tests.sparql` → Record results
- [ ] Run `04_recommendations_tests.sparql` → Record results
- [ ] Run `05_collaborations_tests.sparql` → Record results
- [ ] Run `06_album_inference_tests.sparql` → Record results
- [ ] Run `07_comprehensive_tests.sparql` → Record results

### Post-Test

- [ ] Compare results with expected values in `test_results.md`
- [ ] Document any discrepancies
- [ ] Verify rule execution count
- [ ] Check console for warnings/errors

---

## 🔍 Troubleshooting Tests

| Issue                    | Cause                             | Solution                              |
| ------------------------ | --------------------------------- | ------------------------------------- |
| All queries return empty | Reasoner not running              | Tools > Reasoner > HermiT > Start     |
| ClassicSong not inferred | swrlb:lessThanOrEqual not working | Check swrlb namespace imported        |
| HitSong not showing      | TrendingSong prerequisite missing | Run Trending test first, verify chain |
| Collaborations empty     | Different namespace for artists   | Check prefix music: in query          |
| Timeout on queries       | Large dataset                     | Add LIMIT clause or use sample data   |

---

## 📈 Success Criteria

✅ **Test Passed If:**

- ClassicSong inferred for songs from 1999-2005
- TrendingSong inferred for songs with popularity > 80
- HitSong inferred for Trending songs > 180 seconds
- Recommendations created from shared moods
- Collaborations detected from duets
- Album metadata inferred from songs
- All queries return expected result types (ASK=bool, SELECT=rows, DESCRIBE=properties)

❌ **Test Failed If:**

- Reasoner indicates inconsistency
- Rule body conditions not met for song instances
- SPARQL syntax errors occur
- Expected classes/properties not inferred
- Timeout on query execution

---

## 🚀 Quick Start

```bash
# 1. Navigate to test suite
cd d:\S2\WS\semantic_web_app\backend\ontology\test_suite

# 2. View available tests
ls sparql_queries/

# 3. Run Python test runner
python test_runner.py

# 4. Check results
cat test_results.md
```

---

## 📝 Test Files Description

- **`01_classic_song_tests.sparql`**: Tests releaseYear ≤ 2005 classification
- **`02_trending_song_tests.sparql`**: Tests popularity > 80 classification
- **`03_hit_song_tests.sparql`**: Tests HitSong chain inference
- **`04_recommendations_tests.sparql`**: Tests mood-based recommendations
- **`05_collaborations_tests.sparql`**: Tests artist collaboration detection
- **`06_album_inference_tests.sparql`**: Tests album metadata inference
- **`07_comprehensive_tests.sparql`**: Aggregate and complex test scenarios
- **`test_runner.py`**: Automated test execution
- **`test_results.md`**: Results tracking and documentation
- **`example_test_data.ttl`**: Sample data for testing

---

## 📞 Support

For issues or questions:

1. Check **Troubleshooting** section above
2. Review `music_runtime.ttl` ontology header for query examples
3. Enable debug mode in Protege: **Preferences > Logging > SWRL = DEBUG**

Happy testing! 🎵
