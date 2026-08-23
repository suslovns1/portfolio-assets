#!/usr/bin/env python3
"""
svgkit — a tiny layout/rendering toolkit for the portfolio's architecture diagrams.

Design goals: one consistent visual language across all five case studies, at a
*capability* level of detail (named modules and integrations, decision gates and
human touchpoints — no implementation trivia). Everything is hand-placed on an
explicit grid so the output is deterministic and reviewable, unlike an
auto-routed graph.

Render:  rsvg-convert -w 2800 diagram.svg -o diagram.png
"""

from xml.sax.saxutils import escape

# ─────────────────────────────────────────────────────────── design tokens ──
BG          = "#080C16"
BG_SOFT     = "#0C1220"
LANE_FILL   = "#0D1424"
LANE_STROKE = "#182238"
RAIL        = "#5A6B8C"

INK         = "#E9EEF9"   # primary text
INK_2       = "#95A4C0"   # secondary text
INK_3       = "#6A7A99"   # tertiary / labels

WIRE        = "#33425E"   # default connector
WIRE_MAIN   = "#3F72C4"   # happy-path connector
WIRE_SOFT   = "#2C4266"   # merge / fan-in bus

# semantic roles — kept deliberately few, each explained in the legend
ROLES = {
    "source":  {"line": "#5C6E90", "glow": "#5C6E90", "fill": "#111A2B"},  # system of record / input
    "system":  {"line": "#3F72C4", "glow": "#4F8DF7", "fill": "#101B32"},  # automated module we built
    "ai":      {"line": "#7C5CD6", "glow": "#A78BFA", "fill": "#171331"},  # AI / model service
    "human":   {"line": "#C08A2E", "glow": "#F0B44A", "fill": "#221A0E"},  # human decision / control
    "output":  {"line": "#2C9E77", "glow": "#3FD9A0", "fill": "#0C221B"},  # delivered artefact
}

FONT   = "Inter, Helvetica Neue, Arial, sans-serif"
MONO   = "Menlo, SF Mono, Consolas, monospace"

# rough advance-width factors, good enough for pill sizing and centring
_W_REG, _W_SEMI, _W_MONO = 0.545, 0.575, 0.601


def tw(s, size, weight=400, mono=False, tracking=0.0):
    """Estimated text width in px."""
    f = _W_MONO if mono else (_W_SEMI if weight >= 600 else _W_REG)
    return len(s) * size * f + max(0, len(s) - 1) * tracking


def esc(s):
    return escape(str(s))


# ────────────────────────────────────────────────────────────────── nodes ──
class Box:
    """A placed rectangle exposing edge ports."""

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    def top(self, f=0.5):
        return (self.x + self.w * f, self.y)

    def bottom(self, f=0.5):
        return (self.x + self.w * f, self.y + self.h)

    def left(self, f=0.5):
        return (self.x, self.y + self.h * f)

    def right(self, f=0.5):
        return (self.x + self.w, self.y + self.h * f)


# ───────────────────────────────────────────────────────────────── canvas ──
class Diagram:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.bg = []       # lane bands, drawn first
        self.wires = []    # connectors, drawn under the cards
        self.fg = []       # cards and labels

    # ---------------------------------------------------------- primitives
    def _rect(self, layer, x, y, w, h, r=0, fill="none", stroke="none", sw=1, dash=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op is not None else ""
        layer.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>'
        )

    def _text(self, layer, x, y, s, size=13, weight=400, fill=INK, anchor="start",
              mono=False, tracking=None, op=None):
        fam = MONO if mono else FONT
        t = f' letter-spacing="{tracking}"' if tracking else ""
        o = f' opacity="{op}"' if op is not None else ""
        layer.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{t}{o}>{esc(s)}</text>'
        )

    def text(self, x, y, s, **kw):
        self._text(self.fg, x, y, s, **kw)

    # ------------------------------------------------------------- chrome
    def frame(self):
        self.bg.insert(0, f'<rect width="{self.w}" height="{self.h}" fill="{BG}"/>')
        self.bg.insert(1,
            f'<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="url(#vign)"/>')

    def header(self, x, y, eyebrow, title, subtitle, status=None, status_role="system"):
        """Case eyebrow + title + one-line purpose, with an optional status chip."""
        self._text(self.fg, x, y, eyebrow, size=12.5, weight=600, fill=INK_3, tracking=2.4)
        self._text(self.fg, x, y + 34, title, size=27, weight=700, fill=INK)
        self._text(self.fg, x, y + 61, subtitle, size=14.5, weight=400, fill=INK_2)
        if status:
            r = ROLES[status_role]
            pw = tw(status, 11.5, 600, tracking=1.6) + 26
            px = self.w - 56 - pw
            self._rect(self.fg, px, y - 13, pw, 25, r=12.5, fill=r["fill"], stroke=r["line"], sw=1.2)
            self._text(self.fg, px + pw / 2, y + 4, status, size=11.5, weight=600,
                       fill=r["glow"], anchor="middle", tracking=1.6)
        # rule under the header
        self._rect(self.fg, x, y + 82, self.w - 2 * x, 1, fill="#1A2438")

    def lane(self, x, y, w, h, label, index=None, tint=None):
        """A horizontal phase band with a left rail label."""
        self._rect(self.bg, x, y, w, h, r=14, fill=LANE_FILL, stroke=LANE_STROKE, sw=1)
        if tint:
            self._rect(self.bg, x, y, 3, h, r=1.5, fill=tint)
        lx = x + 22
        plate_w = 22 + (32 if index is not None else 0) + \
            tw(label.upper(), 11.5, 600, tracking=2.2) + 16
        self._rect(self.fg, x + 8, y + 12, plate_w, 29, r=7, fill=LANE_FILL)
        if index is not None:
            self._rect(self.fg, lx, y + 16, 21, 21, r=6, fill="#162034", stroke="#26334D", sw=1)
            self._text(self.fg, lx + 10.5, y + 31, str(index), size=12, weight=700,
                       fill=RAIL, anchor="middle")
            lx += 32
        self._text(self.fg, lx, y + 31, label.upper(), size=11.5, weight=600,
                   fill=RAIL, tracking=2.2)
        return Box(x, y, w, h)

    def note(self, x, y, s, size=12, fill=INK_3, anchor="start", plate=False):
        """A short annotation. `plate` paints the band colour behind it so a
        connector crossing underneath reads as passing behind, not through."""
        if plate:
            w = tw(s, size) + 16
            px = {"start": x - 8, "end": x - w + 8, "middle": x - w / 2}[anchor]
            self._rect(self.fg, px, y - size - 3, w, size + 12, r=5, fill=LANE_FILL)
        self._text(self.fg, x, y, s, size=size, weight=400, fill=fill, anchor=anchor)

    # -------------------------------------------------------------- cards
    def card(self, x, y, w, h, title, lines=(), role="system", chips=(), tag=None,
             title_size=16, shape="rect"):
        """The workhorse node: accent bar + title + up to three muted detail lines."""
        r = ROLES[role]
        if shape == "store":
            self._store(x, y, w, h, r)
        else:
            self._rect(self.fg, x, y, w, h, r=11, fill=r["fill"], stroke=r["line"], sw=1.4)
            self._rect(self.fg, x, y + 11, 3, h - 22, r=1.5, fill=r["glow"], op=0.9)

        tx = x + 18
        ty = y + (38 if shape == "store" else 26)
        if tag:
            self._text(self.fg, tx, ty - 3, tag.upper(), size=10, weight=600,
                       fill=r["glow"], tracking=1.7, op=0.85)
            ty += 17
        self._text(self.fg, tx, ty, title, size=title_size, weight=600, fill=INK)
        ly = ty + 20
        for ln in lines:
            self._text(self.fg, tx, ly, ln, size=12.6, weight=400, fill=INK_2)
            ly += 17
        if chips:
            self._chiprow(tx, y + h - (26 if shape == "store" else 15), chips, r["glow"])
        return Box(x, y, w, h)

    def _store(self, x, y, w, h, r):
        """Cylinder — a system of record."""
        ry = 11
        self.fg.append(
            f'<path d="M{x:.1f} {y+ry:.1f} A {w/2:.1f} {ry} 0 0 1 {x+w:.1f} {y+ry:.1f} '
            f'L {x+w:.1f} {y+h-ry:.1f} A {w/2:.1f} {ry} 0 0 1 {x:.1f} {y+h-ry:.1f} Z" '
            f'fill="{r["fill"]}" stroke="{r["line"]}" stroke-width="1.4"/>'
        )
        self.fg.append(
            f'<path d="M{x:.1f} {y+ry:.1f} A {w/2:.1f} {ry} 0 0 0 {x+w:.1f} {y+ry:.1f}" '
            f'fill="none" stroke="{r["line"]}" stroke-width="1.4" opacity="0.75"/>'
        )

    def _chiprow(self, x, y, chips, color):
        cx = x
        for c in chips:
            cw = tw(c, 10.4, mono=True) + 17
            self._rect(self.fg, cx, y - 12, cw, 18, r=5, fill="#0A1424", stroke="#22314C", sw=1)
            self._text(self.fg, cx + cw / 2, y + 1.5, c, size=10.4, weight=400,
                       fill=color, anchor="middle", mono=True, op=0.92)
            cx += cw + 7

    def gate(self, x, y, w, h, title, lines=(), tag="DECISION", role="human"):
        """A decision point. Amber when a person decides, blue when the system does."""
        r = ROLES[role]
        cut = 16
        self.fg.append(
            f'<path d="M{x+cut:.1f} {y:.1f} L {x+w-cut:.1f} {y:.1f} L {x+w:.1f} {y+h/2:.1f} '
            f'L {x+w-cut:.1f} {y+h:.1f} L {x+cut:.1f} {y+h:.1f} L {x:.1f} {y+h/2:.1f} Z" '
            f'fill="{r["fill"]}" stroke="{r["line"]}" stroke-width="1.4"/>'
        )
        ty = y + 26
        if tag:
            self._text(self.fg, x + w / 2, ty - 3, tag.upper(), size=10, weight=600,
                       fill=r["glow"], anchor="middle", tracking=1.7, op=0.85)
            ty += 17
        self._text(self.fg, x + w / 2, ty, title, size=15, weight=600, fill=INK, anchor="middle")
        ly = ty + 19
        for ln in lines:
            self._text(self.fg, x + w / 2, ly, ln, size=12.4, weight=400, fill=INK_2, anchor="middle")
            ly += 16
        return Box(x, y, w, h)

    def group(self, x, y, w, h, label):
        """A dashed grouping frame for a set of sibling modules."""
        self._rect(self.bg, x, y, w, h, r=10, fill="#0A1120", stroke="#1E2A42", sw=1, dash="5 5")
        if label:
            self._text(self.bg, x + 14, y + 19, label.upper(), size=10.5, weight=600,
                       fill=INK_3, tracking=1.8)
        return Box(x, y, w, h)

    def outcome(self, x, y, w, items, title="BUSINESS OUTCOME"):
        """The closing metrics band — the reason the system exists."""
        h = 92
        self._rect(self.fg, x, y, w, h, r=12, fill="#0A1D18", stroke="#1E4B3C", sw=1.2)
        self._rect(self.fg, x, y + 14, 3, h - 28, r=1.5, fill=ROLES["output"]["glow"])
        self._text(self.fg, x + 20, y + 26, title, size=10.5, weight=600,
                   fill="#3FD9A0", tracking=2.0)
        cw = (w - 40) / len(items)
        for i, (big, small) in enumerate(items):
            ix = x + 20 + cw * i
            self._text(self.fg, ix, y + 58, big, size=21, weight=700, fill="#EAFBF4")
            self._text(self.fg, ix, y + 78, small, size=12, weight=400, fill="#7FB8A4")
            if i:
                self._rect(self.fg, ix - 18, y + 32, 1, 42, fill="#1E4B3C")
        return Box(x, y, w, h)

    def legend(self, x, y, entries, extra=None):
        cx = x
        for label, role in entries:
            r = ROLES[role]
            self._rect(self.fg, cx, y - 9, 13, 13, r=4, fill=r["fill"], stroke=r["line"], sw=1.3)
            self._rect(self.fg, cx + 2.5, y - 6.5, 2.5, 8, r=1.2, fill=r["glow"])
            self._text(self.fg, cx + 21, y + 1.5, label, size=11.8, weight=400, fill=INK_3)
            cx += 21 + tw(label, 11.8) + 30
        if extra:
            self._text(self.fg, self.w - 56, y + 1.5, extra, size=11.8, weight=400,
                       fill="#4A5872", anchor="end")

    # --------------------------------------------------------- connectors
    def wire(self, pts, color=WIRE, sw=1.6, dash=None, arrow=True, label=None,
             label_at=None, label_side="above"):
        """Orthogonal polyline with rounded corners and an optional end arrow."""
        d = _round_path(pts, 9)
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        self.wires.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"{dd}/>'
        )
        if arrow:
            self.wires.append(_arrow(pts[-2], pts[-1], color))
        if label:
            lx, ly = label_at if label_at else _midpoint(pts)
            w = tw(label, 11) + 16
            self.wires.append(
                f'<rect x="{lx-w/2:.1f}" y="{ly-10:.1f}" width="{w:.1f}" height="19" rx="5" '
                f'fill="{BG}" stroke="#22314C" stroke-width="1"/>'
            )
            self._text(self.wires, lx, ly + 4, label, size=11, weight=500,
                       fill=INK_2, anchor="middle")

    def down(self, a, b, fa=0.5, fb=0.5, **kw):
        """a.bottom → b.top, elbowed at the midpoint when the columns differ."""
        p0, p1 = a.bottom(fa), b.top(fb)
        if abs(p0[0] - p1[0]) < 0.6:
            pts = [p0, p1]
        else:
            my = (p0[1] + p1[1]) / 2
            pts = [p0, (p0[0], my), (p1[0], my), p1]
        self.wire(pts, **kw)

    def via(self, a, b, ybus, fa=0.5, fb=0.5, **kw):
        """a.bottom(fa) → down to the bus line → across → into b.top(fb)."""
        p0, p1 = a.bottom(fa), b.top(fb)
        pts = [p0] if abs(p0[0] - p1[0]) < 0.6 else [p0, (p0[0], ybus), (p1[0], ybus)]
        self.wire(pts + [p1], **kw)

    def across(self, a, b, fa=0.5, fb=0.5, **kw):
        """a.right → b.left, elbowed at the midpoint when the rows differ."""
        p0, p1 = a.right(fa), b.left(fb)
        if abs(p0[1] - p1[1]) < 0.6:
            pts = [p0, p1]
        else:
            mx = (p0[0] + p1[0]) / 2
            pts = [p0, (mx, p0[1]), (mx, p1[1]), p1]
        self.wire(pts, **kw)

    # ------------------------------------------------------------- output
    def save(self, path):
        defs = (
            '<defs>'
            f'<radialGradient id="vign" cx="50%" cy="0%" r="105%">'
            f'<stop offset="0%" stop-color="{BG_SOFT}"/>'
            f'<stop offset="100%" stop-color="{BG}"/>'
            '</radialGradient>'
            '</defs>'
        )
        body = "\n".join(self.bg + self.wires + self.fg)
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}">\n{defs}\n{body}\n</svg>\n'
        )
        with open(path, "w") as fh:
            fh.write(svg)
        return path


# ─────────────────────────────────────────────────────────────── geometry ──
def _round_path(pts, r):
    if len(pts) == 2:
        return f"M{pts[0][0]:.1f} {pts[0][1]:.1f} L{pts[1][0]:.1f} {pts[1][1]:.1f}"
    d = [f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"]
    for i in range(1, len(pts) - 1):
        p, c, n = pts[i - 1], pts[i], pts[i + 1]
        r1 = min(r, _dist(p, c) / 2, _dist(c, n) / 2)
        a = _towards(c, p, r1)
        b = _towards(c, n, r1)
        d.append(f"L{a[0]:.1f} {a[1]:.1f}")
        d.append(f"Q{c[0]:.1f} {c[1]:.1f} {b[0]:.1f} {b[1]:.1f}")
    d.append(f"L{pts[-1][0]:.1f} {pts[-1][1]:.1f}")
    return " ".join(d)


def _dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def _towards(frm, to, dist):
    d = _dist(frm, to) or 1
    return (frm[0] + (to[0] - frm[0]) * dist / d, frm[1] + (to[1] - frm[1]) * dist / d)


def _arrow(frm, to, color, size=7.5):
    d = _dist(frm, to) or 1
    ux, uy = (to[0] - frm[0]) / d, (to[1] - frm[1]) / d
    px, py = -uy, ux
    b = (to[0] - ux * size, to[1] - uy * size)
    p1 = (b[0] + px * size * 0.5, b[1] + py * size * 0.5)
    p2 = (b[0] - px * size * 0.5, b[1] - py * size * 0.5)
    return (f'<path d="M{to[0]:.1f} {to[1]:.1f} L{p1[0]:.1f} {p1[1]:.1f} '
            f'L{p2[0]:.1f} {p2[1]:.1f} Z" fill="{color}"/>')


def _midpoint(pts):
    i = len(pts) // 2
    a, b = pts[i - 1], pts[i]
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


# ─────────────────────────────────────────────────────────── layout helpers ──
def row(x0, x1, n, gap):
    """n equal columns filling [x0, x1] with a fixed gap. Returns [(x, w), …]."""
    w = (x1 - x0 - gap * (n - 1)) / n
    return [(x0 + i * (w + gap), w) for i in range(n)]


def _conn(self, x, y, label, role="human", r=15):
    """On-page connector — the BA way to close a loop without a spaghetti wire."""
    c = ROLES[role]
    self.fg.append(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c["fill"]}" '
        f'stroke="{c["line"]}" stroke-width="1.4"/>'
    )
    self._text(self.fg, x, y + 5, label, size=13, weight=700, fill=c["glow"], anchor="middle")
    return Box(x - r, y - r, r * 2, r * 2)


Diagram.conn = _conn
