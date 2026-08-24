#!/usr/bin/env python3
"""Case 5 - Semantic Archive Search & Timeline Drafter."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flowkit import Flow

f = Flow("CASE 05 · COMPANY 3 · DOCUMENTARY PRODUCTION",
         "Semantic Archive Search & Timeline Drafter",
         "Makes a terabyte footage archive answerable in plain language, and returns a first cut.")

f.step(1, "Source libraries",
       "The YouTube and stock footage every project in the series is cut from.",
       role="input")

f.step(2, "Shot segmentation",
       "Every file is split into discrete shots with representative frames.",
       role="system", chips=["Scene detection"])

f.step(3, "Description and indexing",
       "A vision model describes each shot, speech is transcribed, both land in one searchable index.",
       role="ai", chips=["Vision model", "Transcription", "Vector index"],
       note="Indexed once per archive, reused by every project after.")

f.step(4, "Script-driven retrieval",
       "The approved script, split into segments, becomes the query. Each segment gets scored candidates.",
       role="ai", chips=["Semantic retrieval", "Confidence score"])

f.step(5, "Rule-based assembly",
       "Pacing, no-repeat, b-roll ratio and licence constraints are applied to the draft timeline.",
       role="system", chips=["Editorial rules"])

f.step(6, "Editor review",
       "Low-confidence cuts are flagged on the timeline for the editor.",
       role="human")

f.step(7, "Handoff to the editor",
       "An editable sequence that opens straight in Premiere Pro.",
       role="output", chips=["EDL / FCPXML"])

f.outcome([
    ("80% → 10%", "of project time spent searching"),
    ("$100 → $35", "cost per finished video"),
    ("< 1 s", "query across terabytes"),
])
f.footnote("Performance figures are presented as relative deltas under NDA.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case5_semantic_dam.svg")
print(*f.save(out))
