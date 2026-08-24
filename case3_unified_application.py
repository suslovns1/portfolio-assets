#!/usr/bin/env python3
"""Case 3 - Unified Creative Production Application (standalone desktop editor)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flowkit import Flow

f = Flow("CASE 03 · COMPANY 2 · PRODUCTION TOOLING",
         "Unified Creative Production Application",
         "A purpose-built desktop editor that assembles whole creative packs from the studio's own production data.")

f.step(1, "Systems of record",
       "The shared asset library and the production database stay the single source of truth.",
       role="input", chips=["Google Drive", "Airtable"])

f.step(2, "Batch build planner",
       "Decodes a creative code into a full build plan and flags every missing asset up front.",
       role="system", chips=["Preflight report"])

f.step(3, "Missing-asset review",
       "The designer closes the gaps, then the batch runs unattended.",
       role="human")

f.step(4, "Unique asset creation",
       "Subscenes and hooks are cut automatically from approved masters; generative shots fill what the library lacks.",
       role="ai", chips=["Shot detection", "Hook re-cut", "Generative video"])

f.step(5, "Assembly and captions",
       "A full multi-track timeline - ripple, blade, rate stretch, snapping, live preview - with word-level captions.",
       role="system", chips=["Custom NLE core", "FFmpeg", "WebCodecs"],
       note="No After Effects in the chain. Every model runs locally.")

f.step(6, "Localisation",
       "20+ markets in one pass: voice cast, translated on-screen copy, re-timed captions.",
       role="ai", chips=["Multilingual voice", "Stem separation", "Base reuse"])

f.step(7, "Batch render and delivery",
       "8 creatives × 20 markets = 160 finished videos, dropped straight into the delivery folder.",
       role="output")

f.outcome([
    ("160", "localised videos per batch"),
    ("480-1 600", "per day, at 3-10 batches"),
    ("~100%", "of routine automated"),
    ("-80%", "unique asset creation"),
])
f.footnote("Evolved out of Case 02, rebuilt as a standalone application. Figures are relative deltas under NDA.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case3_unified_application.svg")
print(*f.save(out))
