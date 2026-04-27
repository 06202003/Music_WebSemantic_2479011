# Test Suite Structure

```
semantic_web_app/
└── backend/
    └── ontology/
        ├── music_runtime.ttl (Main ontology - 50+ instances, 12 SWRL rules)
        ├── swrl-plugin-config.xml (Protege SWRL plugin config)
        ├── protege-layout-swrl.xml (Protege layout with SWRL tab)
        ├── SWRL_SETUP_GUIDE.md (How to enable SWRL in Protege)
        │
        └── test_suite/
            ├── README.md (📖 Full test framework documentation)
            ├── INDEX.md (📋 This file - quick reference)
            ├── quick_test_guide.md (⚡ 5-minute validation)
            ├── test_results.md (📊 Results tracking template)
            ├── test_runner.py (🤖 Automated testing script)
            ├── .gitignore (Ignore generated results)
            │
            └── sparql_queries/
                ├── 01_classic_song_tests.sparql (4 tests)
                ├── 02_trending_song_tests.sparql (4 tests)
                ├── 03_hit_song_tests.sparql (6 tests)
                ├── 04_recommendations_tests.sparql (6 tests)
                ├── 05_collaborations_tests.sparql (8 tests)
                ├── 06_album_inference_tests.sparql (9 tests)
                └── 07_comprehensive_tests.sparql (10 tests)
                    [TOTAL: 47 SPARQL test queries]
```

## 📂 Quick Navigation

### Documentation

- 🏠 **Start here:** [README.md](README.md)
- ⚡ **Quick test:** [quick_test_guide.md](quick_test_guide.md)
- 📊 **Track results:** [test_results.md](test_results.md)
- 📋 **Reference:** [INDEX.md](INDEX.md) (this file)

### SPARQL Tests

- 📝 All test queries in: `sparql_queries/` folder
- 🔢 47 total test queries organized by category
- 📄 Each `.sparql` file has 4-10 test blocks

### Tools

- 🤖 **Automated:** `python test_runner.py`
- 🔧 **Manual:** Use Protege SPARQL tab
- 📖 **Config:** `SWRL_SETUP_GUIDE.md`

## 🎯 Choose Your Path

### Path A: Quick Validation (5 min)

```
1. Read: quick_test_guide.md
2. Follow 6 test steps
3. Verify TRUE results
4. Done! ✓
```

### Path B: Manual Full Testing (30 min)

```
1. Open: Protege with music_runtime.ttl
2. Enable: HermiT reasoner
3. Copy-paste: Queries from sparql_queries/ folder
4. Record: Results in test_results.md
5. Done! ✓
```

### Path C: Automated Testing (10 min)

```
1. Install: pip install rdflib
2. Run: python test_runner.py
3. Check: test_results.json
4. Done! ✓
```

## ✅ Test Summary

| Test File          | Tests | Focus Area                              |
| ------------------ | ----- | --------------------------------------- |
| 01_classic_song    | 4     | Song classification by release year     |
| 02_trending_song   | 4     | Song classification by popularity       |
| 03_hit_song        | 6     | Chained inference (Trending + Duration) |
| 04_recommendations | 6     | Mood-based song recommendations         |
| 05_collaborations  | 8     | Artist collaboration detection          |
| 06_album_inference | 9     | Album metadata inference                |
| 07_comprehensive   | 10    | Aggregate stats & edge cases            |

## 🚀 Getting Started

### Quickest Option (1 step)

```bash
cd test_suite
python test_runner.py
```

Results saved to: `test_results.json`

### Recommended Option (Manual verification)

1. Open Protege
2. File > Open > music_runtime.ttl
3. Tools > Reasoner > HermiT > Start
4. Follow `quick_test_guide.md` (6 queries, 5 min)

### Thorough Option (Complete coverage)

1. Follow Path B above (manual testing)
2. Run all 47 SPARQL queries
3. Document results in test_results.md
4. Time: ~30-45 minutes

## 📞 Need Help?

1. **Can't enable SWRL?** → Read `SWRL_SETUP_GUIDE.md`
2. **Query not working?** → Check `README.md` troubleshooting
3. **Don't know where to start?** → Read `quick_test_guide.md`
4. **Want to understand everything?** → Read `README.md` (comprehensive)

## 🎓 What Each Test Validates

### 01 - ClassicSong Tests

✓ Rule: `rule_classicSongByYear`  
✓ Validates: Songs from 1999-2005 get ClassicSong class  
✓ SWRL condition: `releaseYear <= 2005`

### 02 - TrendingSong Tests

✓ Rule: `rule_trendingSongByPopularity`  
✓ Validates: High-popularity songs get TrendingSong class  
✓ SWRL condition: `popularityScore > 80`

### 03 - HitSong Tests

✓ Rule: `rule_hitSongByPopularityAndDuration`  
✓ Validates: Long trending songs get HitSong class  
✓ SWRL condition: `TrendingSong AND duration > 180`  
✓ **Tests chained inference**

### 04 - Recommendations Tests

✓ Rule: `rule_recommendationByMood`  
✓ Validates: Songs with same mood linked  
✓ SWRL condition: `hasMood match → recommendedWith`

### 05 - Collaborations Tests

✓ Rules: `rule_artistCollaborationFromDuet`, `rule_collaborativeArtistClass`  
✓ Validates: Duet artists detected and classified  
✓ SWRL chain: Song with 2 artists → collaboratesWith → CollaborativeArtist

### 06 - Album Inference Tests

✓ Rules: `rule_albumByArtistFromSongs`, `rule_albumPrimaryGenreFromSongs`, `rule_multiGenreAlbumClass`  
✓ Validates: Album metadata inferred from songs  
✓ SWRL chain: Song data → Album properties → MultiGenreAlbum classification

### 07 - Comprehensive Tests

✓ Validates: All inference patterns working together  
✓ Tests: Aggregate counts, chains, edge cases  
✓ Ensures: Ontology consistency & performance

## 🏆 Success = All Green

```
✓ 01_classic_song_tests ............... PASS (4/4)
✓ 02_trending_song_tests .............. PASS (4/4)
✓ 03_hit_song_tests ................... PASS (6/6)
✓ 04_recommendations_tests ............ PASS (6/6)
✓ 05_collaborations_tests ............ PASS (8/8)
✓ 06_album_inference_tests ........... PASS (9/9)
✓ 07_comprehensive_tests ............. PASS (10/10)

TOTAL: 47/47 PASS ✓✓✓
```

---

**Test Suite Version:** 1.0  
**Created:** April 27, 2026  
**Status:** Ready for testing
