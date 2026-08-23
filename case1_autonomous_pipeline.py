#!/usr/bin/env python3
"""Case 1 — Autonomous AI Creative Engine (target-state architecture)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Diagram, row, WIRE, WIRE_MAIN, WIRE_SOFT, ROLES, INK_3

W = 1440
M = 56
LX, LW = M, W - 2 * M
PAD, HEAD, GAP = 30, 52, 26
X0, X1 = LX + PAD, LX + LW - PAD

d = Diagram(W, 10)          # height is patched in once the layout is known
d.header(
    M, 62,
    "CASE 01 · BINI GAMES · CREATIVE AUTOMATION",
    "Autonomous AI Creative Engine",
    "From a campaign brief to a review-ready video pack — the designer directs, the pipeline produces.",
    status="TARGET-STATE ARCHITECTURE", status_role="source",
)

cur = 178


def lane(label, index, card_h, note=None):
    """Open a phase band sized to one row of cards; returns the card baseline y."""
    global cur
    h = HEAD + card_h + 26
    y = cur
    d.lane(LX, y, LW, h, label, index=index)
    if note:
        d.note(X1, y + 31, note, anchor="end", plate=True)
    cur = y + h + GAP
    return y + HEAD, y


# ── 1 · brief and creative direction ────────────────────────────────────────
c1, y1 = lane("Brief & Creative Direction", 1, 124,
              "The one phase that spends human judgement instead of GPU credits.")
brief = d.card(X0, c1, 250, 124, "Campaign Brief",
               ["Product, angle, target GEO,", "format, reference winners."],
               role="source", shape="store")
agent = d.card(X0 + 292, c1, 336, 124, "Creative Director Agent",
               ["Reads the brief and returns concept", "angles, script and a shot-by-shot plan."],
               role="ai", tag="Orchestration", chips=["LLM Routing", "Prompt Library"])
manif = d.card(X0 + 670, c1, 300, 124, "Storyboard Manifest",
               ["The machine-readable contract:", "shots, durations, prompts, voice cast."],
               role="system", tag="System contract", chips=["Schema-validated"])
gate1 = d.gate(X0 + 1012, c1, 256, 124, "Concept Sign-off",
               ["Approve the angle before", "any credits are spent."], tag="Human gate")
d.across(brief, agent, color=WIRE_MAIN)
d.across(agent, manif, color=WIRE_MAIN)
d.across(manif, gate1, color=WIRE_MAIN)

# the revision loop re-enters here — closes the connector placed in phase 4
d.conn(agent.x + agent.w - 40, c1 - 26, "1")
d.wire([(agent.x + agent.w - 40, c1 - 11), (agent.x + agent.w - 40, c1)],
       color=ROLES["human"]["line"], dash="4 4")

# ── 2 · parallel generation ─────────────────────────────────────────────────
c2, y2 = lane("Parallel Asset Generation", 2, 112,
              "One manifest fans out into four independent queues, each under a hard cost ceiling.")
gc = row(X0, X1, 4, 26)
gen = [
    d.card(gc[0][0], c2, gc[0][1], 112, "Voice Cast",
           ["Per-character narration in the", "target language, paced to the cut."],
           role="ai", chips=["ElevenLabs"]),
    d.card(gc[1][0], c2, gc[1][1], 112, "Score & SFX",
           ["Licensed bed or generated score,", "entry locked to the first musical beat."],
           role="ai", chips=["Music Library", "Suno"]),
    d.card(gc[2][0], c2, gc[2][1], 112, "Key Visuals",
           ["Style-locked frames built from", "cached character and location refs."],
           role="ai", chips=["Image Model"]),
    d.card(gc[3][0], c2, gc[3][1], 112, "Motion Shots",
           ["Image-to-video per shot at the exact", "duration — nothing trimmed in post."],
           role="ai", chips=["Kling", "Seedance"]),
]
b1 = y2 - GAP / 2 - 5
d.wire([gate1.bottom(), (gate1.cx, b1)], color=WIRE_MAIN, arrow=False,
       label="Approved concept", label_at=(gate1.cx, (gate1.y + gate1.h + b1) / 2))
d.wire([(gate1.cx, b1), (gen[0].cx, b1)], color=WIRE_MAIN, arrow=False)
for g in gen:
    d.wire([(g.cx, b1), g.top()], color=WIRE_MAIN)

# ── 3 · assembly ────────────────────────────────────────────────────────────
c3, y3 = lane("Automated Assembly", 3, 112,
              "Every timing decision is derived from the narration — logged and reproducible.")
ac = row(X0, X1, 3, 44)
clock = d.card(ac[0][0], c3, ac[0][1], 112, "Narration Clock",
               ["Forced alignment turns the voiceover", "into a word-level timing grid."],
               chips=["Forced Alignment"])
comp = d.card(ac[1][0], c3, ac[1][1], 112, "Timeline Compositor",
              ["Shots snap to narration beats; captions,", "ducked music and end-card are laid in."],
              chips=["Scripted Build"])
fleet = d.card(ac[2][0], c3, ac[2][1], 112, "Render Fleet",
               ["Unattended batch render of the whole", "variant matrix — language × ratio."],
               chips=["Render Queue"])
b2 = y3 - GAP / 2 - 5
d.via(gen[0], clock, b2, fb=0.72, color=WIRE_MAIN)
for g in gen[1:]:
    d.wire([g.bottom(), (g.cx, b2)], color=WIRE_SOFT, arrow=False)
d.wire([(gen[1].cx, b2), (gen[3].cx, b2)], color=WIRE_SOFT, arrow=False)
d.wire([(comp.cx, b2), comp.top()], color=WIRE_SOFT)
d.across(clock, comp, color=WIRE_MAIN)
d.across(comp, fleet, color=WIRE_MAIN)

# ── 4 · review and delivery ─────────────────────────────────────────────────
c4, y4 = lane("Review & Delivery", 4, 152,
              "The designer returns as a reviewer — and always receives an editable project, not only a file.")
gate2 = d.gate(X0 + 40, c4, 320, 112, "Side-by-Side Review",
               ["Brief next to the rendered cut:", "approve, or send back with notes."], tag="Human gate")
master = d.card(X0 + 448, c4, 356, 112, "Editable Master Project",
                ["Every draft also lands as an open", "layered project for manual finishing."],
                role="output", chips=["No black box"])
pack = d.card(X0 + 852, c4, 356, 112, "Creative Pack",
              ["Approved variants packaged per", "GEO, placement and ad platform."],
              role="output", chips=["Ready to launch"])
b3 = y4 - GAP / 2 - 5
d.wire([fleet.bottom(), (fleet.cx, b3), (gate2.cx, b3), gate2.top()], color=WIRE_MAIN)
d.across(gate2, master, color=WIRE_MAIN)
d.across(master, pack, color=WIRE_MAIN)

d.wire([gate2.bottom(), (gate2.cx, c4 + 112 + 12)], color=ROLES["human"]["line"], dash="5 4", arrow=False)
d.conn(gate2.cx, c4 + 112 + 27, "1")
d.note(gate2.cx + 28, c4 + 112 + 32, "Revision notes re-enter at the Creative Director Agent",
       size=11.6, fill=INK_3)

# ── outcome + legend ────────────────────────────────────────────────────────
d.outcome(LX, cur, LW, [
    ("4 h → < 3 min", "brief to first draft"),
    ("−80%", "unit cost per concept"),
    ("2 000+", "concepts through the pipeline"),
    ("20+", "GEO variants per approved cut"),
], title="TARGET OUTCOME · MODELLED ON CURRENT PRODUCTION RATES")

d.legend(LX, cur + 92 + 48, [
    ("System of record", "source"),
    ("Automated module", "system"),
    ("AI service", "ai"),
    ("Human control point", "human"),
    ("Delivered artefact", "output"),
], extra="Performance figures are relative deltas, presented under NDA.")

d.h = cur + 92 + 48 + 44
d.frame()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case1_autonomous_pipeline.svg")
d.save(out)
print(out, d.h)
