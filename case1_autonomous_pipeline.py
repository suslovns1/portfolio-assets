#!/usr/bin/env python3
"""Case 1 — Autonomous AI Creative Engine (Bini Games)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flowkit import Flow

f = Flow("CASE 01 · BINI GAMES · CREATIVE AUTOMATION",
         "Autonomous AI Creative Engine",
         "From a campaign brief to a review-ready video pack. The designer directs; the pipeline produces.")

f.step(1, "Campaign brief",
       "Written by the art director: product, angle, target market, format and the winners to beat.",
       role="input")

f.step(2, "Creative direction",
       "An LLM turns the brief into concept angles, a script and a shot-by-shot manifest.",
       role="ai", chips=["LLM Orchestration", "Storyboard Manifest"],
       note="The manifest is the contract: every step downstream executes it, nothing is improvised.")

f.step(3, "Concept sign-off",
       "The motion designer judges the angle before a single generation credit is spent.",
       role="human",
       branches=[
           ("Approve", "The generation queues start.", "system"),
           ("Needs context", "Back to the art director — a thin brief is answered, not generated around.", "input"),
       ])

f.step(4, "Parallel asset generation",
       "Four independent queues run off one manifest, each under a hard cost ceiling.",
       role="ai", chips=["Voice cast", "Score & SFX", "Key visuals", "Motion shots"])

f.step(5, "Automated assembly and render",
       "Forced alignment turns the voiceover into a timing grid; shots snap to narration beats.",
       role="system", chips=["Forced Alignment", "Captions", "Auto-ducked music", "Batch render"],
       note="The whole variant matrix renders unattended — no designer present.")

f.step(6, "Side-by-side review",
       "Brief next to the rendered cut: approve in one click, or send it back with notes.",
       role="human", note="Revisions re-enter at step 2, so the manifest stays the single source of truth.")

f.step(7, "Creative pack",
       "Approved variants — plus an open, layered project file, never a black box.",
       role="output")

f.outcome([
    ("4 h → < 3 min", "brief to first draft"),
    ("−80%", "unit cost per concept"),
    ("Hundreds", "hypotheses per designer, per week"),
])
f.footnote("Performance figures are presented as relative deltas under NDA.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case1_autonomous_pipeline.svg")
print(*f.save(out))
