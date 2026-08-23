#!/usr/bin/env python3
"""Case 5 — Semantic Archive Search & Timeline Drafter."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flowkit import Flow

f = Flow("CASE 05 · DOCUMENTARY & EXPLAINER PRODUCTION",
         "Semantic Archive Search & Timeline Drafter",
         "Makes a terabyte footage archive answerable in plain language — and returns a first cut, not a search result.")

f.step(1, "Footage archive",
       "Terabytes of licensed archive, b-roll and interview rushes.",
       role="input")

f.step(2, "Shot segmentation",
       "Every file is split into discrete shots with representative frames.",
       role="system", chips=["Scene detection"])

f.step(3, "Description and indexing",
       "A vision model describes each shot, speech is transcribed, both land in one searchable index.",
       role="ai", chips=["Vision model", "Transcription", "Vector index"],
       note="Indexing runs once per archive; every project after that queries it for free.")

f.step(4, "Script-driven retrieval",
       "The approved script, broken into narrative beats, becomes the query — each beat gets scored candidates.",
       role="ai", chips=["Semantic retrieval", "Confidence score"])

f.step(5, "Rule-based assembly",
       "Pacing, no-repeat, b-roll ratio and licence constraints are applied to the draft timeline.",
       role="system", chips=["Editorial rules"])

f.step(6, "Editor review",
       "Low-confidence cuts are flagged on the timeline, not hidden. The system drafts; the editor decides.",
       role="human")

f.step(7, "Handoff to the editor's NLE",
       "An editable sequence, delivered in the tool the editor already works in.",
       role="output", chips=["EDL / FCPXML"])

f.outcome([
    ("40% → 6%", "of edit time spent searching"),
    ("$100 → $35", "cost per finished video"),
    ("−85%", "shot-hunting time"),
    ("< 1 s", "query across terabytes"),
])
f.footnote("Performance figures are presented as relative deltas under NDA.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case5_semantic_dam.svg")
print(*f.save(out))
