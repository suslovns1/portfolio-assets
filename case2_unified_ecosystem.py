#!/usr/bin/env python3
"""Case 2 — Unified Creative Production Application (standalone desktop editor)."""
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
    "CASE 02 · STORYBY · PRODUCTION TOOLING",
    "Unified Creative Production Application",
    "A purpose-built desktop editor that assembles whole creative packs from the studio's own production data.",
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


# ── 1 · systems of record ───────────────────────────────────────────────────
c1, y1 = lane("Systems of Record", 1, 118,
              "The studio's existing sources stay the single source of truth — the app never forks them.")
sc = row(X0, X1, 3, 44)
lib = d.card(sc[0][0], c1, sc[0][1], 118, "Shared Asset Library",
             ["Films, hooks, music, overlay elements", "and watermarks on the studio drive."],
             role="source", shape="store")
db = d.card(sc[1][0], c1, sc[1][1], 118, "Production Database",
            ["Creative briefs, approved on-screen copy,", "hook specifications and delivery status."],
            role="source", shape="store")
src = d.card(sc[2][0], c1, sc[2][1], 118, "External References",
             ["Source links named in a brief are pulled", "and normalised on demand."],
             role="source", shape="store")

# ── 2 · the application ─────────────────────────────────────────────────────
c2, y2 = lane("Desktop Application · The Designer's Single Workspace", 2, 118,
              "Cross-platform Electron build — no After Effects licence anywhere in the chain.")
ac = row(X0, X1, 4, 26)
plan = d.card(ac[0][0], c2, ac[0][1], 118, "Batch Build Planner",
              ["Decodes a creative code into a", "full build plan and asset list."],
              tag="Preflight", chips=["Naming Grammar"])
gate = d.gate(ac[1][0], c2, ac[1][1], 118, "Missing-Asset Review",
              ["The designer closes real gaps", "before the batch runs."], tag="Human gate")
work = d.card(ac[2][0], c2, ac[2][1], 118, "Editing Workspace",
              ["Multi-track timeline: ripple,", "blade, rate stretch, snapping."],
              tag="Designer-operated", chips=["Custom NLE Core"])
capt = d.card(ac[3][0], c2, ac[3][1], 118, "Caption & Style System",
              ["Word-level captions on a", "governed brand style set."],
              tag="Brand consistency", chips=["Style Registry"])
b1 = y2 - GAP / 2 - 5
for s_ in (lib, db, src):
    d.wire([s_.bottom(), (s_.cx, b1)], color=WIRE_SOFT, arrow=False)
d.wire([(min(lib.cx, plan.cx), b1), (src.cx, b1)], color=WIRE_SOFT, arrow=False)
d.wire([(plan.cx, b1), plan.top()], color=WIRE_MAIN)
d.across(plan, gate, color=WIRE_MAIN)
d.across(gate, work, color=WIRE_MAIN)
d.across(work, capt, color=WIRE_MAIN)

# ── 3 · local media services ────────────────────────────────────────────────
c3, y3 = lane("Local Media Services · Invoked by the App", 3, 118,
              "Every model runs on the designer's machine — no upload, no per-minute cloud bill, no NDA exposure.")
mc = row(X0, X1, 4, 26)
align = d.card(mc[0][0], c3, mc[0][1], 118, "Forced Alignment",
               ["Word-level timings that drive both", "captions and every later dub."],
               role="ai", chips=["Speech Alignment"])
stems = d.card(mc[1][0], c3, mc[1][1], 118, "Stem Separation",
               ["Splits voice from music so a dub", "keeps the original bed intact."],
               role="ai", chips=["UVR5 / MDX23C"])
scene = d.card(mc[2][0], c3, mc[2][1], 118, "Shot & Hook Analysis",
               ["Detects cuts and builds new hooks", "out of already-approved masters."],
               role="ai", chips=["Scene Detection"])
genai = d.card(mc[3][0], c3, mc[3][1], 118, "Generative Shots",
               ["Fills the gap when the library has", "no footage for a briefed hook."],
               role="ai", chips=["Seedance"])
b2 = y3 - GAP / 2 - 5
d.wire([work.bottom(0.35), (work.x + work.w * 0.35, b2), (align.cx, b2)], color=WIRE_MAIN, arrow=False,
       label="Invoked on demand", label_at=(work.x + work.w * 0.35, (c2 + 118 + b2) / 2))
d.wire([(align.cx, b2), (genai.cx, b2)], color=WIRE_MAIN, arrow=False)
for s_ in (align, stems, scene, genai):
    d.wire([(s_.cx, b2), s_.top()], color=WIRE_MAIN)

# ── 4 · localisation, render and delivery ───────────────────────────────────
c4, y4 = lane("Localisation, Render & Delivery", 4, 118,
              "One unattended run produces the whole matrix: every creative, in every market.")
dc = row(X0, X1, 3, 44)
loc = d.card(dc[0][0], c4, dc[0][1], 118, "Localisation Engine",
             ["20+ markets: voice cast, translated", "on-screen copy, re-timed captions."],
             chips=["ElevenLabs", "Base Reuse"])
rend = d.card(dc[1][0], c4, dc[1][1], 118, "Render Planner",
              ["Picks the cheapest correct route —", "stream copy, or full frame pipeline."],
              chips=["FFmpeg", "WebCodecs"])
out = d.card(dc[2][0], c4, dc[2][1], 118, "Creative Pack",
             ["8+ creatives × 20+ languages,", "delivered straight to the shared drive."],
             role="output", chips=["Batch Delivery"])
b3 = y4 - GAP / 2 - 5
for s_ in (align, stems):
    d.wire([s_.bottom(), (s_.cx, b3)], color=WIRE_SOFT, arrow=False)
d.wire([(align.cx, b3), (stems.cx, b3)], color=WIRE_SOFT, arrow=False)
d.wire([(loc.cx, b3), loc.top()], color=WIRE_MAIN)
for s_ in (scene, genai):
    d.wire([s_.bottom(), (s_.cx, b3)], color=WIRE_SOFT, arrow=False)
d.wire([(rend.cx, b3), (genai.cx, b3)], color=WIRE_SOFT, arrow=False)
d.wire([(rend.cx, b3), rend.top()], color=WIRE_SOFT)
d.across(loc, rend, color=WIRE_MAIN)
d.across(rend, out, color=WIRE_MAIN)

# ── outcome + legend ────────────────────────────────────────────────────────
d.outcome(LX, cur, LW, [
    ("−80%", "of a designer's day given back"),
    ("20+", "markets built in one pass"),
    ("0", "After Effects licences required"),
    ("8+ × 20", "creatives × GEO per batch"),
])
d.legend(LX, cur + 92 + 48, [
    ("System of record", "source"),
    ("Automated module", "system"),
    ("AI service", "ai"),
    ("Human control point", "human"),
    ("Delivered artefact", "output"),
], extra="Performance figures are relative deltas, presented under NDA.")

d.h = cur + 92 + 48 + 44
d.frame()
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case2_unified_ecosystem.svg")
d.save(p)
print(p, d.h)
