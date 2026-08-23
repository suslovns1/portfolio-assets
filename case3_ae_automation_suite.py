#!/usr/bin/env python3
"""Case 3 — After Effects Creative Automation Suite (custom CEP panel)."""
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
    "CASE 03 · STORYBY · IN-TOOL AUTOMATION",
    "After Effects Creative Automation Suite",
    "A custom panel that removes the routine 80% of composition assembly — without taking the designer out of After Effects.",
    status="IN PRODUCTION", status_role="output",
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


# ── 1 · trigger and asset resolution ────────────────────────────────────────
c1, y1 = lane("Trigger & Asset Resolution", 1, 118,
              "Automation starts from the naming convention the studio already had — nothing new for the team to learn.")
rc = row(X0, X1, 3, 44)
code = d.card(rc[0][0], c1, rc[0][1], 118, "Creative Code",
              ["The composition name is the spec:", "film, scene, hook, copy, music."],
              role="source", tag="Input", chips=["Studio Convention"])
parse = d.card(rc[1][0], c1, rc[1][1], 118, "Grammar Parser",
               ["Decodes the code into a precise", "request list for every asset role."],
               tag="Deterministic", chips=["No guesswork"])
heal = d.card(rc[2][0], c1, rc[2][1], 118, "Resolver & Auto-Heal",
              ["Finds each file, repairs unreadable", "media, reports the real gaps up front."],
              tag="Preflight", chips=["Zero mid-render failures"])
d.across(code, parse, color=WIRE_MAIN)
d.across(parse, heal, color=WIRE_MAIN)

# ── 2 · automated composition build ─────────────────────────────────────────
c2, y2 = lane("Automated Composition Build", 2, 118,
              "Four assembly tracks run off one resolved plan — the part of the job that never needed a senior designer.")
bc = row(X0, X1, 4, 26)
foot = d.card(bc[0][0], c2, bc[0][1], 118, "Footage & Hook Layout",
              ["Scene and hook video with linked", "audio, on the studio template."],
              chips=["Frame-accurate"])
keyed = d.card(bc[1][0], c2, bc[1][1], 118, "Overlay & Keying",
               ["Overlay backgrounds removed", "automatically — no manual roto."],
               chips=["Auto Color Key"])
copyd = d.card(bc[2][0], c2, bc[2][1], 118, "Approved Copy",
               ["On-screen text pulled from the", "production database and typeset."],
               chips=["Text DB Presync"])
caps = d.card(bc[3][0], c2, bc[3][1], 118, "Caption Track",
              ["Voice isolated, aligned, then", "animated word by word."],
              role="ai", chips=["UVR5", "Alignment"])
b1 = y2 - GAP / 2 - 5
d.wire([heal.bottom(), (heal.cx, b1), (foot.cx, b1)], color=WIRE_MAIN, arrow=False,
       label="Resolved build plan", label_at=(heal.cx, (c1 + 118 + b1) / 2))
d.wire([(foot.cx, b1), (caps.cx, b1)], color=WIRE_MAIN, arrow=False)
for m in (foot, keyed, copyd, caps):
    d.wire([(m.cx, b1), m.top()], color=WIRE_MAIN)

# ── 3 · variations, localisation, handoff ───────────────────────────────────
c3, y3 = lane("Variations, Localisation & Handoff", 3, 118,
              "The panel hands back native, fully editable compositions — automation never becomes a black box.")
vc = row(X0, X1, 4, 26)
matrix = d.card(vc[0][0], c3, vc[0][1], 118, "Variation Matrix",
                ["Hook × copy × music combinations", "built in a single pass."],
                chips=["Split-test ready"])
lang = d.card(vc[1][0], c3, vc[1][1], 118, "In-Panel Localisation",
              ["Offline translation of copy and", "captions against a locked glossary."],
              role="ai", chips=["Local Model"])
review = d.gate(vc[2][0], c3, vc[2][1], 118, "Designer Review",
                ["Every comp stays native", "and fully editable."], tag="Human gate")
pack = d.card(vc[3][0], c3, vc[3][1], 118, "Variation Pack",
              ["Batch render with first-frame", "thumbnails and a session log."],
              role="output", chips=["Ready to test"])
b2 = y3 - GAP / 2 - 5
for m in (foot, keyed, copyd, caps):
    d.wire([m.bottom(), (m.cx, b2)], color=WIRE_SOFT, arrow=False)
d.wire([(foot.cx, b2), (caps.cx, b2)], color=WIRE_SOFT, arrow=False)
d.wire([(matrix.cx, b2), matrix.top()], color=WIRE_MAIN)
d.across(matrix, lang, color=WIRE_MAIN)
d.across(lang, review, color=WIRE_MAIN)
d.across(review, pack, color=WIRE_MAIN)

# ── outcome + legend ────────────────────────────────────────────────────────
d.outcome(LX, cur, LW, [
    ("5–7×", "faster composition assembly"),
    ("20+", "variations in ~15 seconds"),
    ("0", "renders lost to missing assets"),
    ("100%", "editable native output"),
])
d.legend(LX, cur + 92 + 48, [
    ("Input", "source"),
    ("Automated module", "system"),
    ("AI service", "ai"),
    ("Human control point", "human"),
    ("Delivered artefact", "output"),
], extra="Performance figures are relative deltas, presented under NDA.")

d.h = cur + 92 + 48 + 44
d.frame()
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case3_ae_automation_suite.svg")
d.save(p)
print(p, d.h)
