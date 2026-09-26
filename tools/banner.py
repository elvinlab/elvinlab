#!/usr/bin/env python3
"""Generate animated AI-themed header/divider SVGs for the GitHub profile (dark + light)."""
import math, random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

THEMES = {
    "dark": dict(bg1="#07070f", bg2="#0f0b1f", text="#e6edf3", muted="#8b949e", line="#30284d", node="#a78bfa"),
    "light": dict(bg1="#fbfbff", bg2="#eef0ff", text="#0d1117", muted="#57606a", line="#c9c3ee", node="#7c3aed"),
}
VIOLET, CYAN, PINK = "#8b5cf6", "#06b6d4", "#ec4899"
FONT = "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "'Space Grotesk', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
ROLES = ["Full-Stack Engineering", "AI Agents &amp; Workflows", "Software Architecture", "Performance &amp; Optimization"]


def network(w, h, t):
    """Layered neural net on the right side with animated signal pulses."""
    random.seed(7)
    layers = [3, 5, 5, 3]
    x0, x1 = w * 0.60, w * 0.94
    nodes = []
    for i, n in enumerate(layers):
        x = x0 + (x1 - x0) * i / (len(layers) - 1)
        nodes.append([(x, h * (0.5 + (j - (n - 1) / 2) * 0.16)) for j in range(n)])
    lines, pulses, circles = [], [], []
    k = 0
    for a, b in zip(nodes, nodes[1:]):
        for (xa, ya) in a:
            for (xb, yb) in b:
                d = f"M{xa:.1f} {ya:.1f} L{xb:.1f} {yb:.1f}"
                lines.append(f'<path d="{d}" stroke="{t["line"]}" stroke-width="1"/>')
                if random.random() < 0.45:
                    length = math.hypot(xb - xa, yb - ya)
                    delay = random.uniform(0, 4)
                    color = random.choice([VIOLET, CYAN, PINK])
                    pulses.append(
                        f'<path d="{d}" class="pulse" stroke="{color}" stroke-width="2" '
                        f'stroke-dasharray="14 {length:.0f}" stroke-dashoffset="14" '
                        f'style="--len:{length + 14:.0f};animation-delay:{delay:.2f}s"/>')
                k += 1
    for li, layer in enumerate(nodes):
        for j, (x, y) in enumerate(layer):
            delay = (li * 0.5 + j * 0.3) % 3
            circles.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{t["bg2"]}" stroke="{t["node"]}" stroke-width="2"/>'
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" class="core" fill="url(#g)" style="animation-delay:{delay:.1f}s"/>')
    return "\n".join(lines + pulses + circles)


def header(name, t):
    w, h = 1200, 340
    step = 3.0
    total = step * len(ROLES)
    roles = "\n".join(
        f'<text x="72" y="236" class="role" style="animation-delay:{i * step}s">{r}<tspan class="cursor"> ▍</tspan></text>'
        for i, r in enumerate(ROLES))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Elvin González — Full-stack Software Engineer: AI agents and workflows, clean architecture, performance and cloud">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VIOLET}"/><stop offset=".55" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}"/>
  </linearGradient>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/>
  </linearGradient>
  <radialGradient id="glow1" cx=".78" cy=".35" r=".45"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".28"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
  <radialGradient id="glow2" cx=".15" cy=".95" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".18"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{t["line"]}" stroke-width=".5" opacity=".35"/></pattern>
  <clipPath id="r"><rect width="{w}" height="{h}" rx="18"/></clipPath>
</defs>
<style>
  .hi {{ font: 500 20px {FONT}; fill: {t["muted"]}; }}
  .name {{ font: 800 64px {SANS}; letter-spacing: -1.5px; }}
  .prompt {{ font: 600 26px {FONT}; fill: {CYAN}; }}
  .role {{ font: 600 26px {FONT}; fill: {t["text"]}; opacity: 0; animation: role {total}s infinite; }}
  .tag {{ font: 500 15px {FONT}; fill: {t["muted"]}; letter-spacing: 1px; }}
  .cursor {{ fill: {PINK}; animation: blink 1s steps(1) infinite; }}
  .pulse {{ fill: none; animation: flow 4s linear infinite; }}
  .core {{ animation: beat 3s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
  @keyframes role {{ 0% {{ opacity: 0; transform: translateY(8px); }} 3%, {100 / len(ROLES) - 3:.1f}% {{ opacity: 1; transform: none; }} {100 / len(ROLES):.1f}%, 100% {{ opacity: 0; transform: translateY(-8px); }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @keyframes flow {{ from {{ stroke-dashoffset: 14; }} to {{ stroke-dashoffset: calc(var(--len) * -1); }} }}
  @keyframes beat {{ 0%, 100% {{ transform: scale(1); opacity: .9; }} 50% {{ transform: scale(1.5); opacity: 1; }} }}
  @media (prefers-reduced-motion: reduce) {{ .role, .pulse, .core, .cursor {{ animation: none; }} .role:first-of-type {{ opacity: 1; }} }}
</style>
<g clip-path="url(#r)">
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>
  <rect width="{w}" height="{h}" fill="url(#glow1)"/>
  <rect width="{w}" height="{h}" fill="url(#glow2)"/>
  {network(w, h, t)}
  <text x="72" y="104" class="hi">// hey, I'm</text>
  <text x="68" y="172" class="name" fill="url(#g)">{name}</text>
  <text x="72" y="236" class="prompt" dx="-2">&gt;</text>
  <g transform="translate(26 0)">{roles}</g>
  <text x="72" y="292" class="tag">FULL-STACK SOFTWARE ENGINEER · COSTA RICA · ELVINLAB.DEV</text>
  <rect x="0" y="{h - 4}" width="{w}" height="4" fill="url(#g)"/>
</g>
</svg>'''
    return svg


def divider(t):
    w, h = 1200, 24
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{VIOLET}" stop-opacity="0"/><stop offset=".2" stop-color="{VIOLET}"/>
  <stop offset=".5" stop-color="{CYAN}"/><stop offset=".8" stop-color="{PINK}"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/>
</linearGradient></defs>
<style>.dot {{ animation: move 6s ease-in-out infinite alternate; }} @keyframes move {{ to {{ transform: translateX(1000px); }} }}
@media (prefers-reduced-motion: reduce) {{ .dot {{ animation: none; }} }}</style>
<rect x="0" y="11" width="{w}" height="2" fill="url(#g)" opacity=".7"/>
<circle class="dot" cx="100" cy="12" r="4" fill="{CYAN}"/>
</svg>'''


for mode, t in THEMES.items():
    (OUT / f"banner-{mode}.svg").write_text(header("Elvin González", t))
    (OUT / f"divider-{mode}.svg").write_text(divider(t))
print("ok")
