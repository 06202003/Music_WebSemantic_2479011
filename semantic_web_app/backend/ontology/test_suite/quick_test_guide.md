# Quick Test Guide

**Fast 5-minute test to verify ontology working correctly**

## ⚡ Quick Test Steps

### Step 1: Load Ontology (30 seconds)

```
Protege > File > Open
Navigate to: d:\S2\WS\semantic_web_app\backend\ontology\music_runtime.ttl
Click Open
```

Wait for file to load (should show "Ontology loaded" status)

### Step 2: Enable Reasoner (1 minute)

```
Tools > Reasoner > HermiT
Wait for "Starting reasoner..." message
Should show: "Reasoner: Consistent" ✓
```

### Step 3: Run Quick Test Query (2 minutes)

```
Click: SPARQL Query tab
Paste this query:
```

```sparql
PREFIX music: <http://example.org/music#>
SELECT
  (COUNT(DISTINCT ?cs) as ?classicSongs)
  (COUNT(DISTINCT ?ts) as ?trendingSongs)
  (COUNT(DISTINCT ?hs) as ?hitSongs)
  (COUNT(DISTINCT ?ca) as ?collaborativeArtists)
WHERE {
  OPTIONAL { ?cs a music:ClassicSong . }
  OPTIONAL { ?ts a music:TrendingSong . }
  OPTIONAL { ?hs a music:HitSong . }
  OPTIONAL { ?ca a music:CollaborativeArtist . }
}
```

```
Click: Execute
```

### Expected Result:

```
classicSongs: 4
trendingSongs: 9+
hitSongs: 2+
collaborativeArtists: 6+
```

✅ **If you see numbers = Everything is working!**

---

## 🧪 Specific Quick Tests (2 min each)

### Test 1: ClassicSong Rule

```sparql
PREFIX music: <http://example.org/music#>
ASK { music:Song_demo_timeless_echo a music:ClassicSong . }
```

**Expected:** TRUE

### Test 2: TrendingSong Rule

```sparql
PREFIX music: <http://example.org/music#>
ASK { music:Song_viral_current a music:TrendingSong . }
```

**Expected:** TRUE

### Test 3: HitSong Rule (Chained)

```sparql
PREFIX music: <http://example.org/music#>
ASK { music:Song_blockbuster_epic a music:HitSong . }
```

**Expected:** TRUE

### Test 4: Recommendations

```sparql
PREFIX music: <http://example.org/music#>
ASK { music:Song_demo_reflection music:recommendedWith music:Song_demo_reflection_live . }
```

**Expected:** TRUE

### Test 5: Collaborations

```sparql
PREFIX music: <http://example.org/music#>
ASK { music:Artist_demo_solo music:collaboratesWith music:Artist_demo_band . }
```

**Expected:** TRUE

### Test 6: Album Inference

```sparql
PREFIX music: <http://example.org/music#>
ASK { music:Album_demo_semantic_reflections music:albumByArtist music:Artist_demo_solo . }
```

**Expected:** TRUE

---

## 🚨 Troubleshooting

| Issue                    | Fix                                                   |
| ------------------------ | ----------------------------------------------------- |
| All queries return empty | Reasoner not started. Go to Tools > Reasoner > HermiT |
| Parser error on query    | Check SPARQL syntax, verify PREFIX                    |
| Timeout                  | Try with LIMIT clause or simpler query                |
| Ontology won't load      | Check file path is correct                            |

---

## ✅ Success Indicators

If ALL quick tests return TRUE/correct counts:
✅ ClassicSong rule working
✅ TrendingSong rule working  
✅ HitSong chained inference working
✅ Recommendations working
✅ Collaborations working
✅ Album inference working
✅ **ONTOLOGY IS FULLY FUNCTIONAL!**

---

## 📋 Full Test Suite

For comprehensive testing, see:

- `README.md` - Full test framework
- `sparql_queries/` - 40+ organized queries
- `test_results.md` - Results tracking

Run all tests:

```bash
cd test_suite
python test_runner.py
```
