#!/usr/bin/env python3
"""Case 4 — Multi-Language Localisation Engine (background dubbing service)."""
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
    "CASE 04 · STORYBY · GLOBAL SCALING",
    "Multi-Language Localisation Engine",
    "Turns one winning creative into twenty market-ready versions as a background job — zero designer hours.",
    status="SHIPPED · FOLDED INTO CASE 02", status_role="output",
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


# ── 1 · input ───────────────────────────────────────────────────────────────
c1, y1 = lane("Input & Speech Map", 1, 118,
              "A creative enters the queue the moment it wins the auction — no hand-off meeting, no ticket.")
ic = row(X0, X1, 3, 44)
master = d.card(ic[0][0], c1, ic[0][1], 118, "Winning Creative",
                ["The approved master cut and the", "edit decisions behind it."],
                role="source", shape="store")
smap = d.card(ic[1][0], c1, ic[1][1], 118, "Speech Map",
              ["Segments the master read into", "phrases with hard boundaries."],
              chips=["Voice Activity", "Alignment"])
geos = d.card(ic[2][0], c1, ic[2][1], 118, "Target Markets",
              ["The GEO list marketing wants live", "within hours of the win."],
              role="source", shape="store")
d.across(master, smap, color=WIRE_MAIN)
d.wire([geos.left(), smap.right()], color=WIRE_MAIN)

# ── 2 · routing decision ────────────────────────────────────────────────────
c2, y2 = lane("Automated Routing", 2, 118,
              "Recognising an already-dubbed master is the single highest-value decision in the engine.")
route = d.gate(X0, c2, 470, 118, "Re-cut of a Dubbed Master?",
               ["Five categorical checks —", "never a statistical guess."],
               tag="Routing decision", role="system")
reuse = d.card(X0 + 550, c2, 470, 118, "Base Reuse",
               ["The editor's own trim already defines", "the mapping — reuse 1:1, no re-timing."],
               chips=["Exact by construction"])
b1 = y2 - GAP / 2 - 5
d.wire([smap.bottom(), (smap.cx, b1), (route.cx, b1), route.top()], color=WIRE_MAIN)
d.across(route, reuse, color=WIRE_MAIN, label="Match")
ax = X0 + 1130
d.wire([reuse.right(), (ax - 16, reuse.cy)], color=WIRE_MAIN)
d.conn(ax, reuse.cy, "A", role="output")
d.note(ax, reuse.cy + 40, "Skips the ladder", size=11.6, fill=INK_3, anchor="middle")

# ── 3 · escalation ladder ───────────────────────────────────────────────────
c3, y3 = lane("Adaptive Re-timing Ladder", 3, 118,
              "Each rung is tried only when the previous one runs out of room — the cheapest fix always wins.")
tc = row(X0, X1, 3, 96)
t1 = d.card(tc[0][0], c3, tc[0][1], 118, "Tier 1 · Micro-pacing",
            ["Stretch the phrase inside a threshold", "the ear cannot detect."],
            chips=["Default path"])
t2 = d.card(tc[1][0], c3, tc[1][1], 118, "Tier 2 · Bidirectional Fit",
            ["Move picture and audio together when", "the phrase still overruns its window."],
            chips=["Picture remap"])
t3 = d.card(tc[2][0], c3, tc[2][1], 118, "Tier 3 · Semantic Condensation",
            ["An LLM rewrites the line to fit the", "window with the marketing hook intact."],
            role="ai", chips=["Meaning preserved"])
b2 = y3 - GAP / 2 - 5
d.wire([route.bottom(), (route.cx, b2), (t1.cx, b2), t1.top()], color=WIRE_MAIN,
       label="No match", label_at=(route.cx, (c2 + 118 + b2) / 2))
d.across(t1, t2, color=ROLES["human"]["line"], label="Overruns")
d.across(t2, t3, color=ROLES["human"]["line"], label="At the cap")

# ── 4 · voice, mix and QA ───────────────────────────────────────────────────
c4, y4 = lane("Voice, Mix & QA", 4, 118,
              "The engine escalates a read it cannot place instead of shipping a version nobody checked.")
vc = row(X0, X1, 4, 26)
voice = d.card(vc[0][0], c4, vc[0][1], 118, "Multilingual Voice Cast",
               ["One casting decision reused across", "every market and every creative."],
               role="ai", chips=["ElevenLabs"])
mix = d.card(vc[1][0], c4, vc[1][1], 118, "Stem-Aware Mix",
             ["The original music bed survives", "because the voice is separated out."],
             chips=["UVR5 / MDX23C"])
qa = d.gate(vc[2][0], c4, vc[2][1], 118, "Shippability Check",
            ["A read that no longer fits is", "escalated, never shipped quietly."], tag="Human gate")
outp = d.card(vc[3][0], c4, vc[3][1], 118, "Localised Pack",
              ["20+ markets, burned subtitles", "where the platform requires them."],
              role="output", chips=["Ready to launch"])
b3 = y4 - GAP / 2 - 5
d.wire([t3.bottom(), (t3.cx, b3), (voice.x + voice.w * 0.35, b3),
        (voice.x + voice.w * 0.35, c4)], color=WIRE_MAIN)
d.conn(voice.x + voice.w * 0.86, c4 - 26, "A", role="output")
d.wire([(voice.x + voice.w * 0.86, c4 - 11), (voice.x + voice.w * 0.86, c4)],
       color=ROLES["output"]["line"], dash="4 4")
d.across(voice, mix, color=WIRE_MAIN)
d.across(mix, qa, color=WIRE_MAIN)
d.across(qa, outp, color=WIRE_MAIN)

# ── outcome + legend ────────────────────────────────────────────────────────
d.outcome(LX, cur, LW, [
    ("1.5 h → minutes", "5 markets by hand vs 20 automated"),
    ("0", "designer hours per release"),
    ("20+", "markets live the same day"),
    ("1:1", "audio fidelity on a re-cut"),
])
d.legend(LX, cur + 92 + 48, [
    ("Input", "source"),
    ("Automated module", "system"),
    ("AI service", "ai"),
    ("Human control point", "human"),
    ("Delivered artefact", "output"),
], extra="Hexagon = decision point. Performance figures are relative deltas, under NDA.")

d.h = cur + 92 + 48 + 44
d.frame()
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case4_localization_engine.svg")
d.save(p)
print(p, d.h)
