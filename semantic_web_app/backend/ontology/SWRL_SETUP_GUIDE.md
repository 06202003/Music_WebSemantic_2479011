# Protege SWRL Import Setup Guide

## **Method 1: Auto-Enable SWRL (Recommended)**

### Step 1: Update Protege Configuration

```
Go to: C:\Users\[YourUsername]\AppData\Roaming\Protege\
Create file: protege.properties

Add these lines:
---
# Enable SWRL Tab
swrl.enabled=true
swrl.tab.visible=true
org.protege.editor.owl.ui.view.SWRLRulesView.enabled=true
```

### Step 2: Restart Protege

```
Close Protege completely
Reopen it
SWRL tab should now appear automatically
```

---

## **Method 2: Manual Import via File**

### Step 1: Open Protege

```
File > Open > d:\S2\WS\semantic_web_app\backend\ontology\music_runtime.ttl
```

### Step 2: Import Layout

```
Protege > Preferences > Manage Ontology Layouts
Click "Import"
Select: protege-layout-swrl.xml
Apply
Restart Protege
```

---

## **Method 3: Quick Install SWRL Plugin**

### Step 1: Check for Updates

```
Protege > Help > Check for updates
Search: "SWRL"
Install: "SWRL Editor Tab"
Restart Protege
```

### Step 2: Enable in Plugin Manager

```
Protege > Preferences > Plugins
Find: "SWRL Rules Editor"
Check ✓ to enable
Restart Protege
```

### Step 3: Verify SWRL Tab Appears

```
After restart, SWRL tab should show next to Ontology
```

---

## **Method 4: Command Line Launch**

```powershell
# Navigate to Protege installation
cd "C:\Program Files\Protege"

# Launch with ontology and layout
protege.exe -layout D:\S2\WS\semantic_web_app\backend\ontology\protege-layout-swrl.xml D:\S2\WS\semantic_web_app\backend\ontology\music_runtime.ttl
```

---

## **Troubleshoot: SWRL Tab Still Missing?**

### Check 1: Verify Plugin Installed

```
Tools > Preferences > Plugins
Scroll to find "SWRL"
If not listed: Install from Help > Check for updates
```

### Check 2: Verify Protege Version

```
Help > About Protege
Must be Protege 5.3+ for full SWRL support
```

### Check 3: Clear Protege Cache

```
Close Protege
Delete: C:\Users\[YourUsername]\AppData\Roaming\Protege\cache\
Restart Protege
```

### Check 4: Manual Tab Addition

```
1. Open music_runtime.ttl
2. Go to "Window" menu
3. Look for "SWRL" option
4. Click to show SWRL tab
```

---

## **Once SWRL Tab is Visible**

✅ Click SWRL tab to see all 12 inference rules:

- rule_classicSongByYear
- rule_trendingSongByPopularity
- rule_hitSongByPopularityAndDuration
- rule_recommendationByMood
- rule_artistCollaborationFromDuet
- rule_collaborativeArtistClass
- rule_multiGenreAlbumClass
- rule_albumByArtistFromSongs
- rule_albumPrimaryGenreFromSongs
- rule_propagateGenreForRelatedSongs
- rule_relatedBySharedArtist
- rule_eventCountryFromArtistOrigin

✅ Start reasoner: Tools > Reasoner > HermiT > Start Reasoner

✅ Test SPARQL: Tools > SPARQL Query > Run sample queries

---

## **File Locations**

- Ontology: `d:\S2\WS\semantic_web_app\backend\ontology\music_runtime.ttl`
- Plugin Config: `d:\S2\WS\semantic_web_app\backend\ontology\swrl-plugin-config.xml`
- Layout File: `d:\S2\WS\semantic_web_app\backend\ontology\protege-layout-swrl.xml`

---

## **Quick Test After Setup**

```
1. SWRL tab visible ✓
2. Click on rule (e.g., rule_classicSongByYear)
3. Should show rule definition with swrl:body and swrl:head
4. Go to SPARQL Query
5. Run: ASK { music:Song_demo_timeless_echo a music:ClassicSong . }
6. Result: TRUE (because 1999 <= 2005)
```

✅ If TRUE appears = Everything working perfectly!
