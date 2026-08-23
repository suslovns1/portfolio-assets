#!/usr/bin/env python3
"""Case 5 — Semantic Archive Search & Timeline Drafter."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Diagram, row, WIRE, WIRE_MAIN, WIRE_SOFT, ROLES, INK_3

W, M = 1440, 56
LX, LW = M, W - 2 * M
PAD, HEAD, GAP = 30, 52, 26
X0, X1 = LX + PAD, LX + LW - PAD

d = Diagram(W, 10)
d.header(
    M, 62,
    "CASE 05 · DOCUMENTARY & EXPLAINER PRODUCTION",
    "Semantic Archive Search & Timeline Drafter",
    "Makes a terabyte footage archive answerable in plain language — and returns a first cut, not a search result.",
)

cur = 178


def lane(label, index, card_h, note=None):
    global cur
    h = HEAD + card_h + 26
    y = cur
    d.lane(LX, y, LW, h, label, index=index)
    if note:
        d.note(X1, y + 31, note, anchor="end", plate=True)
    cur = y + h + GAP
    return y + HEAD, y


# ── 1 · indexing ────────────────────────────────────────────────────────────
c1, y1 = lane("Archive Indexing", 1, 118,
              "Indexing runs once per archive; every project afterwards queries it for free.")
ic = row(X0, X1, 4, 26)
arch = d.card(ic[0][0], c1, ic[0][1], 118, "Footage Archive",
              ["Terabytes of licensed archive,", "b-roll and interview rushes."],
              role="source", shape="store")
shots = d.card(ic[1][0], c1, ic[1][1], 118, "Shot Segmentation",
               ["Every file split into discrete", "shots with representative frames."],
               chips=["Scene Detection"])
descr = d.card(ic[2][0], c1, ic[2][1], 118, "Shot Description",
               ["A vision model describes what is", "on screen; speech is transcribed."],
               role="ai", chips=["Vision Model"])
index = d.card(ic[3][0], c1, ic[3][1], 118, "Searchable Index",
               ["Embeddings and metadata, queried", "in plain language in under a second."],
               role="source", shape="store")
d.across(arch, shots, color=WIRE_MAIN)
d.across(shots, descr, color=WIRE_MAIN)
d.across(descr, index, color=WIRE_MAIN)

# ── 2 · script to footage ───────────────────────────────────────────────────
c2, y2 = lane("Script to Footage", 2, 118,
              "The script — not a folder tree — becomes the way an editor navigates the archive.")
sc = row(X0, X1, 3, 44)
script = d.card(sc[0][0], c2, sc[0][1], 118, "Narrative Script",
                ["The approved voiceover, broken", "into narrative beats."],
                role="source", tag="Input", chips=["Beat structure"])
match = d.card(sc[1][0], c2, sc[1][1], 118, "Beat-to-Shot Matcher",
               ["Retrieves candidate shots for each", "beat and scores how well each fits."],
               role="ai", tag="Semantic retrieval", chips=["Confidence score"])
rules = d.card(sc[2][0], c2, sc[2][1], 118, "Editorial Rules",
               ["Pacing, no-repeat, b-roll ratio and", "licence constraints are enforced."],
               tag="Craft, encoded", chips=["Assembly Rules"])
b1 = y2 - GAP / 2 - 5
d.wire([index.bottom(), (index.cx, b1), (match.cx, b1), match.top()], color=WIRE_MAIN,
       label="Indexed shots", label_at=(index.cx, (c1 + 118 + b1) / 2))
d.across(script, match, color=WIRE_MAIN)
d.across(match, rules, color=WIRE_MAIN)

# ── 3 · draft and handoff ───────────────────────────────────────────────────
c3, y3 = lane("Draft & Handoff", 3, 118,
              "The system drafts; the editor still decides. Uncertainty is surfaced, never hidden.")
dc = row(X0, X1, 3, 44)
draft = d.card(dc[0][0], c3, dc[0][1], 118, "Timeline Draft",
               ["A first assembly with b-roll, lower", "thirds and titles already in place."],
               chips=["Minutes, not days"])
gate = d.gate(dc[1][0], c3, dc[1][1], 118, "Editor Review",
              ["Low-confidence cuts are flagged", "on the timeline, not hidden."], tag="Human gate")
hand = d.card(dc[2][0], c3, dc[2][1], 118, "NLE Handoff",
              ["Delivered as an editable sequence", "in the editor's own tool."],
              role="output", chips=["EDL / FCPXML"])
b2 = y3 - GAP / 2 - 5
d.wire([rules.bottom(), (rules.cx, b2), (draft.cx, b2), draft.top()], color=WIRE_MAIN)
d.across(draft, gate, color=WIRE_MAIN)
d.across(gate, hand, color=WIRE_MAIN)

# ── outcome + legend ────────────────────────────────────────────────────────
d.outcome(LX, cur, LW, [
    ("−85%", "time spent hunting for a shot"),
    ("−65%", "unit cost per finished video"),
    ("< 1 s", "plain-language archive query"),
])
d.legend(LX, cur + 92 + 48, [
    ("Input / index", "source"),
    ("Automated module", "system"),
    ("AI service", "ai"),
    ("Human control point", "human"),
    ("Delivered artefact", "output"),
], extra="Performance figures are relative deltas, presented under NDA.")

d.h = cur + 92 + 48 + 44
d.frame()
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case5_semantic_dam.svg")
d.save(p)
print(p, d.h)
