#!/usr/bin/env python3
"""Case 4 - Multi-Language Localisation Engine (background dubbing service)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flowkit import Flow

f = Flow("CASE 04 · COMPANY 2 · GLOBAL SCALING",
         "Multi-Language Localisation Engine",
         "Turns one winning creative into twenty market-ready versions as a background job.")

f.step(1, "Winning creative and target markets",
       "The approved master cut, the edit decisions behind it, and the market list.",
       role="input",
       note="A creative enters the queue the moment it wins the auction.")

f.step(2, "Speech map",
       "Segments the master read into phrases with hard boundaries.",
       role="system", chips=["Voice activity detection", "Forced alignment"])

f.step(3, "Routing decision",
       "Is this a re-cut of a master that has already been dubbed?",
       role="decision",
       branches=[
           ("Yes", "Base reuse. The editor's trim already defines the mapping, 1:1.", "output"),
           ("No", "Send the read down the adaptive re-timing ladder.", "system"),
       ],
       note="Five hard checks. All five must pass.")

f.step(4, "Adaptive re-timing ladder",
       "Each rung runs only when the previous one runs out of room.",
       role="system",
       chips=["1 · Micro-pacing", "2 · Picture remap", "3 · Semantic condensation"])

f.step(5, "Voice cast and stem-aware mix",
       "The voice is separated out first, so the original music bed survives.",
       role="ai", chips=["Multilingual voice", "Stem separation"])

f.step(6, "Shippability check",
       "A read that no longer fits the picture goes to a person.",
       role="human")

f.step(7, "Localised pack",
       "20+ markets, with burned subtitles where the platform requires them.",
       role="output")

f.outcome([
    ("5 → 20+", "markets per creative"),
    ("160", "dubs per pack, unattended"),
    ("1.5 h → 0 min", "designer time per release"),
    ("1:1", "fidelity on a re-cut"),
])
f.footnote("Later folded into Case 03. Figures are relative deltas under NDA.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case4_localization_engine.svg")
print(*f.save(out))
