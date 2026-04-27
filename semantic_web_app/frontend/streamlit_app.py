"""Streamlit frontend for the Semantic Music Explorer."""

from __future__ import annotations

from typing import Any

import requests
import streamlit as st


DEFAULT_API_BASE = "http://localhost:8000"


def api_get(api_base: str, path: str, params: dict[str, Any] | None = None) -> Any:
    response = requests.get(f"{api_base}{path}", params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def render_home(api_base: str) -> None:
    st.subheader("Browse Songs")
    songs = api_get(api_base, "/api/songs")

    search = st.text_input("Search songs, artists, albums, or genres", value="")
    if search:
        needle = search.strip().lower()
        songs = [
            song
            for song in songs
            if needle in str(song.get("title", "")).lower()
            or needle in str(song.get("artist", "")).lower()
            or needle in str(song.get("album", "")).lower()
            or needle in str(song.get("genre", "")).lower()
        ]

    st.caption(f"{len(songs)} song(s) matched")

    if not songs:
        st.info("No songs found.")
        return

    for song in songs[:50]:
        with st.container(border=True):
            st.markdown(f"### {song.get('title', 'Unknown')}")
            st.write(f"Artist: {song.get('artist', '-')}")
            st.write(f"Album: {song.get('album', '-')}")
            st.write(f"Genre: {song.get('genre', '-')}")
            st.write(f"Year: {song.get('year', '-')}")


def render_detail(api_base: str) -> None:
    st.subheader("Semantic Song Detail")
    songs = api_get(api_base, "/api/songs")

    if not songs:
        st.info("No songs available from the backend yet.")
        return

    song_options = {f"{song.get('title', 'Unknown')} — {song.get('artist', '-')}": song.get("id") for song in songs}

    selected_label = st.selectbox("Choose a song", list(song_options.keys()))
    song_id = song_options[selected_label]
    if not song_id:
        st.warning("No song selected")
        return

    data = api_get(api_base, f"/api/songs/{song_id}")
    info = data.get("info", {})

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {info.get('title', 'Unknown')}")
        st.write(f"Artist: {info.get('artist', '-')}")
        st.write(f"Album: {info.get('album', '-')}")
        st.write(f"Genre: {info.get('genre', '-')}")
        st.write(f"Year: {info.get('year', '-')}")
        st.write(f"Country: {info.get('country', '-')}")

    with col2:
        explanation = data.get("semantic_explanation", {})
        st.markdown("### Semantic Summary")
        st.write(explanation.get("human_summary", "No semantic explanation available."))
        provenance = explanation.get("provenance", {})
        st.caption(f"source={provenance.get('source', '-')}, fetchedAt={provenance.get('fetched_at', '-')}")

    relations = [
        ("Songs by same artist", data.get("related_artist", [])),
        ("Songs in same album", data.get("related_album", [])),
        ("Songs in same genre", data.get("related_genre", [])),
        ("Inferred related by artist", data.get("inferred_related_artist", [])),
    ]

    for title, items in relations:
        st.markdown(f"#### {title}")
        if not items:
            st.write("No related songs found.")
        else:
            st.dataframe(items, use_container_width=True, hide_index=True)

    st.markdown("#### Artist Collaborations")
    collaborations = data.get("artist_collaborations", [])
    if collaborations:
        st.dataframe(collaborations, use_container_width=True, hide_index=True)
    else:
        st.write("No collaborations detected for this song.")

    st.markdown("#### RDF Triples")
    triples = data.get("triples", [])
    if triples:
        st.dataframe(triples, use_container_width=True, hide_index=True)
    else:
        st.write("No triples returned.")


def render_sparql(api_base: str) -> None:
    st.subheader("SPARQL Query Runner")
    query = st.text_area(
        "Write a read-only SPARQL query",
        value="""PREFIX music: <http://example.org/music#>\nSELECT ?song ?title WHERE {\n  ?song a music:Song .\n  ?song music:title ?title .\n}\nORDER BY ?title\nLIMIT 20""",
        height=200,
    )

    if st.button("Run query", type="primary"):
        try:
            result = api_get(api_base, "/api/sparql", params={"q": query})
        except requests.RequestException as exc:
            st.error(f"SPARQL request failed: {exc}")
            return

        result_type = str(result.get("type", "")).upper()
        if result_type == "ASK":
            st.success(f"ASK result: {result.get('boolean', False)}")
            return

        if result_type in {"DESCRIBE", "CONSTRUCT"}:
            triples = result.get("triples", [])
            st.write(f"{len(triples)} triple(s) returned")
            if triples:
                st.dataframe(triples, use_container_width=True, hide_index=True)
            return

        rows = result.get("results", [])
        if rows:
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.info("No rows returned.")


def render_health(api_base: str) -> None:
    st.subheader("Backend Health")
    data = api_get(api_base, "/api/semantic/health")
    validation = data.get("validation", {})

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Songs", data.get("song_count", 0))
    with col2:
        st.metric("Validation issues", validation.get("issue_count", 0))

    st.markdown("#### Validation Report")
    st.json(validation)


def render_swrl(api_base: str) -> None:
    st.subheader("SWRL Rules")
    st.caption("This view reads SWRL definitions from the ontology file through the Python backend. Execution still happens in Protege / an OWL reasoner, not inside Streamlit.")

    summary = api_get(api_base, "/api/swrl/summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rules", summary.get("rule_count", 0))
    with col2:
        st.metric("Variables", summary.get("variable_count", 0))
    with col3:
        st.metric("Numeric rules", len(summary.get("numeric_rules", [])))

    st.markdown("#### Rule Names")
    st.write(", ".join(summary.get("class_inference_rules", []) + summary.get("property_inference_rules", []) + summary.get("numeric_rules", [])))

    st.markdown("#### Variables")
    variables = summary.get("variables", [])
    if variables:
        st.code("\n".join(f"- {variable}" for variable in variables), language="text")
    else:
        st.info("No SWRL variables found.")

    st.markdown("#### Full Rule List")
    rules = summary.get("rules", [])
    for rule in rules:
        with st.expander(rule.get("name", "SWRL rule"), expanded=False):
            if rule.get("label"):
                st.write(rule["label"])
            st.markdown("**Body**")
            st.code(rule.get("body", ""), language="turtle")
            st.markdown("**Head**")
            st.code(rule.get("head", ""), language="turtle")


def main() -> None:
    st.set_page_config(page_title="Semantic Music Explorer", page_icon="🎵", layout="wide")
    st.title("Semantic Music Explorer")
    st.caption("Python frontend for the existing FastAPI + RDF backend")

    api_base = st.sidebar.text_input("API base URL", value=DEFAULT_API_BASE)
    tab_name = st.sidebar.radio("Go to", ["Home", "Detail", "SPARQL", "SWRL", "Health"], index=0)

    try:
        if tab_name == "Home":
            render_home(api_base)
        elif tab_name == "Detail":
            render_detail(api_base)
        elif tab_name == "SPARQL":
            render_sparql(api_base)
        elif tab_name == "SWRL":
            render_swrl(api_base)
        else:
            render_health(api_base)
    except requests.RequestException as exc:
        st.error(f"Unable to reach the backend at {api_base}: {exc}")


if __name__ == "__main__":
    main()