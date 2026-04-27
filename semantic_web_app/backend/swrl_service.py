"""Utilities for reading SWRL rules from the music ontology file."""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


ONTOLOGY_FILE = Path(__file__).resolve().parent / "ontology" / "music_runtime.ttl"


@dataclass(slots=True)
class SwrlRule:
    name: str
    label: str | None
    body: str
    head: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SwrlService:
    """Parse SWRL rule definitions from the ontology Turtle file."""

    RULE_START_RE = re.compile(r"(?m)^(music:rule_[A-Za-z0-9_]+)\s+rdf:type\s+swrl:Imp\s*;")
    RULE_BLOCK_RE = re.compile(
        r"(?ms)^(music:rule_[A-Za-z0-9_]+)\s+rdf:type\s+swrl:Imp\s*;(?P<body>.*?)(?=^music:rule_[A-Za-z0-9_]+\s+rdf:type\s+swrl:Imp\s*;|\Z)"
    )
    LABEL_RE = re.compile(r'rdfs:label\s+"([^"]+)"')
    BODY_RE = re.compile(r"swrl:body\s*\((.*?)\)\s*;", re.DOTALL)
    HEAD_RE = re.compile(r"swrl:head\s*\((.*?)\)\s*\.\s*$", re.DOTALL)
    VARIABLE_RE = re.compile(r"music:var[A-Za-z0-9_]+\s+rdf:type\s+swrl:Variable\s*;\s*swrl:varName\s+\"([^\"]+)\"", re.DOTALL)

    def __init__(self, ontology_path: Path | None = None):
        self.ontology_path = ontology_path or ONTOLOGY_FILE

    def _read_text(self) -> str:
        return self.ontology_path.read_text(encoding="utf-8")

    def get_rules(self) -> list[SwrlRule]:
        text = self._read_text()
        rules: list[SwrlRule] = []

        for match in self.RULE_BLOCK_RE.finditer(text):
            name = match.group(1)
            block = match.group("body")
            label_match = self.LABEL_RE.search(block)
            body_match = self.BODY_RE.search(block)
            head_match = self.HEAD_RE.search(block)

            rules.append(
                SwrlRule(
                    name=name,
                    label=label_match.group(1) if label_match else None,
                    body=(body_match.group(1).strip() if body_match else ""),
                    head=(head_match.group(1).strip() if head_match else ""),
                )
            )

        return rules

    def get_summary(self) -> dict[str, Any]:
        rules = self.get_rules()
        text = self._read_text()
        variables = self.VARIABLE_RE.findall(text)

        class_rules = [rule for rule in rules if "ClassAtom" in rule.head]
        property_rules = [rule for rule in rules if "IndividualPropertyAtom" in rule.head]
        numeric_rules = [rule for rule in rules if "BuiltinAtom" in rule.body]

        return {
            "ontology_file": str(self.ontology_path),
            "rule_count": len(rules),
            "variable_count": len(variables),
            "variables": variables,
            "class_inference_rules": [rule.name for rule in class_rules],
            "property_inference_rules": [rule.name for rule in property_rules],
            "numeric_rules": [rule.name for rule in numeric_rules],
            "rules": [rule.to_dict() for rule in rules],
        }


_service: SwrlService | None = None


def get_swrl_service() -> SwrlService:
    global _service
    if _service is None:
        _service = SwrlService()
    return _service