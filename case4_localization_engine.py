#!/usr/bin/env python3
"""Case 4 — Multi-Language Localisation Engine (background dubbing service)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flowkit import Flow

f = Flow("CASE 04 · STORYBY · GLOBAL SCALING",
         "Multi-Language Localisation Engine",
         "Turns one winning creative into twenty market-ready versions as a background job.")

f.step(1, "Winning creative and target markets",
       "The approved master cut, the edit decisions behind it, and the market list.",
       role="input",
       note="A creative enters the queue the moment it wins the auction — no hand-off meeting, no ticket.")

f.step(2, "Speech map",
       "Segments the master read into phrases with hard boundaries.",
       role="system", chips=["Voice activity detection", "Forced alignment"])

f.step(3, "Routing decision",
       "Is this a re-cut of a master that has already been dubbed?",
       role="decision",
       branches=[
           ("Yes", "Base reuse — the editor's own trim already defines the mapping. 1:1, no re-timing.", "output"),
           ("No", "Send the read down the adaptive re-timing ladder.", "system"),
       ],
       note="Five categorical checks, never a statistical guess. This one decision removes the costliest class of dubbing error.")

f.step(4, "Adaptive re-timing ladder",
       "Each rung is tried only when the previous one runs out of room — the cheapest fix wins.",
       role="system",
       chips=["1 · Micro-pacing", "2 · Picture remap", "3 · Semantic condensation"])

f.step(5, "Voice cast and stem-aware mix",
       "The original music bed survives, because the voice is separated out before the dub goes in.",
       role="ai", chips=["Multilingual voice", "Stem separation"])

f.step(6, "Shippability check",
       "A read that no longer fits the picture is escalated, never shipped quietly.",
       role="human")

f.step(7, "Localised pack",
       "20+ markets, with burned subtitles where the platform requires them.",
       role="output")

f.outcome([
    ("1.5 h → minutes", "5 markets by hand vs 20 automated"),
    ("0", "designer hours per release"),
    ("20+", "markets live on the day of the win"),
    ("1:1", "audio fidelity on a re-cut"),
])
f.footnote("Later folded into Case 03, where the same engine runs inside the application. "
           "Performance figures are presented as relative deltas under NDA.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case4_localization_engine.svg")
print(*f.save(out))
