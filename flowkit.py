#!/usr/bin/env python3
"""
flowkit — linear process-flow diagrams for the portfolio's automation case studies.

One vertical spine, one step per row, one sentence per step. Light background so the
diagram reads as part of the document rather than as a separate piece of art, which is
what a process artefact should do. Replaces the earlier dark swimlane system: that one
was denser and prettier, and worse to actually read at Notion's column width.

Render:  rsvg-convert -w 2080 diagram.svg -o diagram.png
"""

from xml.sax.saxutils import escape

# ─────────────────────────────────────────────────────────── design tokens ──
PAPER   = "#FFFFFF"
INK     = "#0F172A"   # step titles
INK_2   = "#475569"   # step body
INK_3   = "#94A3B8"   # eyebrow, captions
LINE    = "#E2E8F0"   # card borders
SPINE   = "#CBD5E1"   # the process spine

FONT = "Inter, Helvetica Neue, Arial, sans-serif"

# One role per step. The tag on each card names it, so no legend is needed.
ROLES = {
    "input":    {"tag": "INPUT",          "dot": "#94A3B8", "fg": "#475569", "bg": "#F1F5F9"},
    "system":   {"tag": "AUTOMATED",      "dot": "#2563EB", "fg": "#1D4ED8", "bg": "#EFF6FF"},
    "ai":       {"tag": "AI SERVICE",     "dot": "#7C3AED", "fg": "#6D28D9", "bg": "#F5F3FF"},
    "human":    {"tag": "HUMAN DECISION", "dot": "#D97706", "fg": "#B45309", "bg": "#FFFBEB"},
    "decision": {"tag": "DECISION",       "dot": "#2563EB", "fg": "#1D4ED8", "bg": "#EFF6FF"},
    "output":   {"tag": "DELIVERABLE",    "dot": "#059669", "fg": "#047857", "bg": "#ECFDF5"},
}

_W_REG, _W_SEMI = 0.545, 0.575


def tw(s, size, weight=400, tracking=0.0):
    f = _W_SEMI if weight >= 600 else _W_REG
    return len(s) * size * f + max(0, len(s) - 1) * tracking


# ──────────────────────────────────────────────────────────────── geometry ──
W = 980
M = 44
MARK_X = M + 26          # centre of the step marker
CARD_X = M + 74
CARD_W = W - CARD_X - M

HEAD_TOP = 54
STEP_GAP = 20


class Flow:
    def __init__(self, eyebrow, title, subtitle):
        self.el = []
        self.y = 0
        self.marks = []          # marker centres, for drawing the spine underneath
        self._header(eyebrow, title, subtitle)

    # ---------------------------------------------------------- primitives
    def _rect(self, x, y, w, h, r=0, fill="none", stroke="none", sw=1):
        self.el.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def _text(self, x, y, s, size=14.5, weight=400, fill=INK_2, anchor="start", tracking=None):
        t = f' letter-spacing="{tracking}"' if tracking else ""
        self.el.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{t}>{escape(s)}</text>')

    # ------------------------------------------------------------- header
    def _header(self, eyebrow, title, subtitle):
        self._text(M, HEAD_TOP, eyebrow, 11, 600, INK_3, tracking=2.2)
        self._text(M, HEAD_TOP + 34, title, 27, 700, INK)
        self._text(M, HEAD_TOP + 60, subtitle, 14.5, 400, INK_2)
        self._rect(M, HEAD_TOP + 80, W - 2 * M, 1, fill=LINE)
        self.y = HEAD_TOP + 116

    # --------------------------------------------------------------- step
    def step(self, n, title, body, role="system", chips=(), branches=(), note=None):
        r = ROLES[role]
        h = 80 + (24 if chips else 0) + (26 * len(branches)) + (26 if note else 0)
        y = self.y

        self._rect(CARD_X, y, CARD_W, h, r=10, fill=PAPER, stroke=LINE, sw=1.2)
        self._rect(CARD_X, y + 12, 3.5, h - 24, r=2, fill=r["dot"])

        # role tag, top right
        tag = r["tag"]
        pw = tw(tag, 10.5, 600, 1.4) + 22
        self._rect(CARD_X + CARD_W - 18 - pw, y + 17, pw, 21, r=10.5, fill=r["bg"])
        self._text(CARD_X + CARD_W - 18 - pw / 2, y + 31.5, tag, 10.5, 600, r["fg"],
                   anchor="middle", tracking=1.4)

        self._text(CARD_X + 22, y + 35, title, 19, 600, INK)
        self._text(CARD_X + 22, y + 62, body, 14.5, 400, INK_2)

        ly = y + 62
        for label, text, brole in branches:
            ly += 26
            br = ROLES[brole]
            lw = tw(label, 11, 600) + 20
            self._rect(CARD_X + 22, ly - 12, lw, 18, r=9, fill=br["bg"])
            self._text(CARD_X + 22 + lw / 2, ly + 1.5, label, 11, 600, br["fg"], anchor="middle")
            self._text(CARD_X + 22 + lw + 12, ly + 2, text, 13.5, 400, INK_2)

        if chips:
            cy = ly + (22 if branches else 24)
            cx = CARD_X + 22
            for c in chips:
                cw = tw(c, 11) + 20
                self._rect(cx, cy - 13, cw, 20, r=5, fill="#F8FAFC", stroke=LINE, sw=1)
                self._text(cx + cw / 2, cy + 1.5, c, 11, 500, "#64748B", anchor="middle")
                cx += cw + 8
            ly = cy

        if note:
            self._text(CARD_X + 22, ly + 24, note, 12.5, 400, INK_3)

        self.marks.append((y + 30, role, n))
        self.y = y + h + STEP_GAP
        return y

    # ------------------------------------------------------------ outcome
    def outcome(self, items, title="BUSINESS OUTCOME"):
        y = self.y + 10
        h = 96
        self._rect(M, y, W - 2 * M, h, r=10, fill="#F6FBF8", stroke="#CBE8DA", sw=1.2)
        self._text(M + 24, y + 27, title, 10.5, 600, "#047857", tracking=1.8)

        avail = W - 2 * M - 48
        need = [max(tw(b, 21, 700), tw(s_, 12)) for b, s_ in items]
        gutter = 36
        slack = avail - sum(need) - gutter * (len(items) - 1)
        size = 21
        if slack < 0:                       # shrink the figures until the row fits
            size = max(15, 21 * (avail - gutter * (len(items) - 1)) / sum(need))
            need = [max(tw(b, size, 700), tw(s_, 12)) for b, s_ in items]
            slack = avail - sum(need) - gutter * (len(items) - 1)
        pad = slack / len(items)

        x = M + 24
        for i, (big, small) in enumerate(items):
            if i:
                self._rect(x - gutter / 2 - pad / 2, y + 34, 1, 46, fill="#CBE8DA")
            self._text(x, y + 62, big, size, 700, "#0B3D2E")
            self._text(x, y + 82, small, 12, 400, "#5B8474")
            x += need[i] + pad + gutter
        self.y = y + h + 12

    def footnote(self, s):
        self._text(M, self.y + 20, s, 11.5, 400, INK_3)
        self.y += 32

    # ------------------------------------------------------------- output
    def save(self, path):
        height = self.y + 20
        spine = []
        if len(self.marks) > 1:
            spine.append(f'<path d="M{MARK_X} {self.marks[0][0]} L{MARK_X} {self.marks[-1][0]}" '
                         f'stroke="{SPINE}" stroke-width="2" fill="none"/>')
            # one arrowhead per gap, so direction of travel is unambiguous
            for a, b in zip(self.marks, self.marks[1:]):
                my = (a[0] + b[0]) / 2
                spine.append(f'<path d="M{MARK_X - 5} {my - 4} L{MARK_X} {my + 3} '
                             f'L{MARK_X + 5} {my - 4}" fill="none" stroke="{SPINE}" '
                             f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')

        markers = []
        for cy, role, n in self.marks:
            r = ROLES[role]
            if role == "decision":
                markers.append(f'<path d="M{MARK_X} {cy - 17} L{MARK_X + 17} {cy} '
                               f'L{MARK_X} {cy + 17} L{MARK_X - 17} {cy} Z" '
                               f'fill="{PAPER}" stroke="{r["dot"]}" stroke-width="2"/>')
            else:
                markers.append(f'<circle cx="{MARK_X}" cy="{cy}" r="15" fill="{PAPER}" '
                               f'stroke="{r["dot"]}" stroke-width="2"/>')
            markers.append(
                f'<text x="{MARK_X}" y="{cy + 5}" font-family="{FONT}" font-size="13" '
                f'font-weight="700" fill="{r["dot"]}" text-anchor="middle">{n}</text>')

        body = "\n".join([f'<rect width="{W}" height="{height:.0f}" fill="{PAPER}"/>']
                         + spine + markers + self.el)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height:.0f}" '
               f'viewBox="0 0 {W} {height:.0f}">\n{body}\n</svg>\n')
        with open(path, "w") as fh:
            fh.write(svg)
        return path, height
