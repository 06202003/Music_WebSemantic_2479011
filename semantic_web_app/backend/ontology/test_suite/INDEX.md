# Test Suite Index

Complete testing framework for `music_runtime.ttl` ontology

## 📁 Files Overview

### Documentation

- **README.md** - Full test suite documentation with setup instructions
- **quick_test_guide.md** - 5-minute quick validation guide
- **test_results.md** - Results tracking template (fill after running tests)
- **.gitignore** - Exclude test results from version control

### SPARQL Query Files

Organized test queries by inference rule category:

1. **01_classic_song_tests.sparql** (4 tests)
   - ASK: ClassicSong detection
   - SELECT: List all classic songs
   - DESCRIBE: Show song properties with inferred class
   - CONSTRUCT: Build ClassicSong graph

2. **02_trending_song_tests.sparql** (4 tests)
   - ASK: Multiple trending songs
   - SELECT: Trending songs ranked by popularity
   - DESCRIBE: Trending song details
   - CONSTRUCT: Trending songs network

3. **03_hit_song_tests.sparql** (6 tests)
   - ASK: HitSong detection
   - ASK: Prerequisites verification
   - SELECT: List all hit songs
   - DESCRIBE: Show inference chain
   - CONSTRUCT: Class hierarchy visualization
   - Edge case: Trending but not hit

4. **04_recommendations_tests.sparql** (6 tests)
   - ASK: Reflective mood linking
   - SELECT: Recommendation pairs by mood
   - CONSTRUCT: Recommendation graph
   - SELECT: Mood-based aggregation
   - ASK: Verify symmetric property
   - SELECT: Transitive paths

5. **05_collaborations_tests.sparql** (8 tests)
   - ASK: Artist collaboration inference
   - ASK: CollaborativeArtist class
   - SELECT: All collaboration pairs
   - SELECT: Duet songs
   - DESCRIBE: Collaborative artist details
   - CONSTRUCT: Collaboration network
   - SELECT: Collaboration frequency
   - ASK: Symmetric property verification

6. **06_album_inference_tests.sparql** (9 tests)
   - ASK: Album-artist inference
   - ASK: Multi-genre detection
   - ASK: MultiGenreAlbum class
   - SELECT: Albums with artists
   - SELECT: Genre count aggregation
   - DESCRIBE: Complete album metadata
   - CONSTRUCT: Album graph
   - SELECT: Verification basis
   - Edge case: Single-genre albums

7. **07_comprehensive_tests.sparql** (10 tests)
   - SELECT: Aggregate inference counts
   - CONSTRUCT: Complete inference chain
   - SELECT: Multi-classification detection
   - SELECT: Collaboration-to-album paths
   - SELECT: Recommendation chains with genres
   - ASK: Consistency validation
   - SELECT: Complex multi-pattern query
   - SELECT: Performance test
   - ASK: Ontology consistency
   - SELECT: Rule execution trace

### Testing Tools

- **test_runner.py** - Automated test execution script
  - Loads ontology
  - Executes all SPARQL queries
  - Generates JSON results
  - Produces summary statistics

## 🚀 Quick Start

### 1. Manual Testing (Protege GUI)

```bash
# Open Protege
1. File > Open > music_runtime.ttl
2. Tools > Reasoner > HermiT > Start Reasoner
3. Click SPARQL Query tab
4. Copy-paste queries from sparql_queries/ files
5. Click Execute
6. Record results in test_results.md
```

### 2. Automated Testing (Python)

```bash
# Navigate to test suite
cd d:\S2\WS\semantic_web_app\backend\ontology\test_suite

# Install requirements
pip install rdflib

# Run all tests
python test_runner.py

# Check results
cat test_results.json
```

### 3. Quick Validation (5 min)

```bash
# Follow quick_test_guide.md
# Run 6 key tests to verify ontology works
```

## 📊 Test Statistics

| Category        | Tests  | Focus                                             |
| --------------- | ------ | ------------------------------------------------- |
| ClassicSong     | 4      | releaseYear ≤ 2005                                |
| TrendingSong    | 4      | popularity > 80                                   |
| HitSong         | 6      | TrendingSong + duration > 180s (chained)          |
| Recommendations | 6      | Mood-based linking                                |
| Collaborations  | 8      | Artist duets detection                            |
| Album Inference | 9      | albumByArtist, albumPrimaryGenre, MultiGenreAlbum |
| Comprehensive   | 10     | Aggregates, edge cases, performance               |
| **TOTAL**       | **47** | **Complete coverage**                             |

## ✅ Expected Results

### Passing Criteria

- ASK queries: TRUE (for existing inferences)
- SELECT queries: Row counts match expected ranges
- DESCRIBE queries: Show inferred classes
- CONSTRUCT queries: Return valid RDF triples
- No parser errors or timeouts
- Reasoner shows "Consistent"

### Key Test Entities

**Example Songs Triggering Inference:**

- `Song_demo_timeless_echo` (1999, 84.7 pop) → ClassicSong + TrendingSong
- `Song_blockbuster_epic` (92.1 pop, 295s) → TrendingSong + HitSong
- `Song_demo_reflection` (mood: reflective) → recommendedWith relationships
- `Song_demo_collab_bridge` (duet) → collaboratesWith inference
- `Album_demo_semantic_reflections` → albumByArtist + albumPrimaryGenre

## 🔄 Test Workflow

```
1. Load Ontology
    ↓
2. Enable Reasoner (HermiT)
    ↓
3. Run Quick Tests (5 min)
    ├─ All pass? → GO TO FULL SUITE
    └─ Some fail? → Check troubleshooting
    ↓
4. Run Full Test Suite (30 min)
    ├─ Manual in Protege OR
    └─ Automated via test_runner.py
    ↓
5. Record Results
    └─ Fill test_results.md with findings
```

## 🐛 Troubleshooting

| Issue                 | Solution                       |
| --------------------- | ------------------------------ |
| Queries return empty  | Reasoner not running           |
| Parser errors         | Check SPARQL syntax and PREFIX |
| Timeout               | Add LIMIT or try simpler query |
| Inconsistent ontology | Check domain/range constraints |

See README.md for detailed troubleshooting.

## 📈 Performance Benchmarks

Expected performance with HermiT reasoner:

- Simple ASK queries: < 100ms
- SELECT with 5-10 results: < 500ms
- Large CONSTRUCT (1000+ triples): 1-2 seconds
- Full reasoner initialization: 2-5 seconds

## 📝 Files Checklist

- [x] README.md - Full documentation
- [x] quick_test_guide.md - 5-minute guide
- [x] test_results.md - Results template
- [x] 01_classic_song_tests.sparql
- [x] 02_trending_song_tests.sparql
- [x] 03_hit_song_tests.sparql
- [x] 04_recommendations_tests.sparql
- [x] 05_collaborations_tests.sparql
- [x] 06_album_inference_tests.sparql
- [x] 07_comprehensive_tests.sparql
- [x] test_runner.py - Automation script
- [x] .gitignore - Repository cleanup
- [x] INDEX.md (this file)

## 🎯 Success Indicators

✅ **All tests pass** when:

1. Music ontology loads without errors
2. HermiT reasoner initializes successfully
3. All 47 test queries execute without timeout
4. Inferred class counts match expected values
5. No ontology inconsistencies reported
6. Query execution times are reasonable

**Example Success Output:**

```
Total Tests:    47
Passed:         47 ✓
Failed:         0 ✗
Errors:         0 ⚠
Pass Rate:      100.0%

✓✓✓ ALL TESTS PASSED ✓✓✓
```

---

**Last Updated:** April 27, 2026  
**Test Suite Version:** 1.0  
**Ontology Version:** music_runtime.ttl (complete)
