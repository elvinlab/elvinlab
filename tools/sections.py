#!/usr/bin/env python3
"""Generate profile section SVGs (cards, timeline, stats strip) matching the banner's visual system."""
import textwrap
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

VIOLET, CYAN, PINK = "#8b5cf6", "#06b6d4", "#ec4899"
FONT = "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "'Space Grotesk', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
THEMES = {
    "dark": dict(bg="#0d1117", card1="#0f0b1f", card2="#0a1220", text="#e6edf3", muted="#8b949e", line="#30284d", grid="#1c1830"),
    "light": dict(bg="#ffffff", card1="#faf8ff", card2="#f2fbfe", text="#0d1117", muted="#57606a", line="#d8d0f5", grid="#ece8fb"),
}

# Minimal line icons drawn on a 40x40 box.
ICONS = {
    "agents": '<circle cx="8" cy="20" r="4"/><circle cx="32" cy="8" r="4"/><circle cx="32" cy="32" r="4"/><circle cx="20" cy="20" r="3"/>'
              '<path d="M12 20h5M22.5 18.5 29 10.5M22.5 21.5 29 29.5"/>',
    "architecture": '<path d="M20 4 34 12v16L20 36 6 28V12z"/><path d="M6 12l14 8 14-8M20 20v16"/>',
    "fullstack": '<path d="M14 10 4 20l10 10M26 10l10 10-10 10M23 6l-6 28"/>',
    "performance": '<path d="M23 3 8 23h11l-3 14 16-21H21z"/>',
}

CARDS = [
    ("agents", "AI Agents & Workflows", VIOLET,
     "Multi-agent orchestration, model routing across providers, persistent memory and spec-driven development."),
    ("architecture", "Software Architecture", CYAN,
     "Clear boundaries, decoupled domains and predictable code — systems that stay easy to change as they grow."),
    ("fullstack", "Full-Stack Engineering", PINK,
     "End to end and framework-agnostic: interfaces, APIs, data and infrastructure. The right tool for each problem."),
    ("performance", "Performance & Optimization", VIOLET,
     "Profiling, bottleneck hunting and optimization — fast, cost-efficient systems with automated delivery."),
]

TIMELINE = [
    ("2020", "First APIs and university projects"),
    ("2021", "Team projects and modern frontend frameworks"),
    ("2022–24", "Full-stack products, cloud deployments and team codebases"),
    ("2025 → now", "AI agents, clean architecture and performance"),
]

STATS = ["5+ YEARS", "FULL-STACK", "AI AGENTS & WORKFLOWS", "ARCHITECTURE", "PERFORMANCE", "COSTA RICA"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def defs(t):
    return f'''<linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{VIOLET}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}"/>
  </linearGradient>
  <linearGradient id="gh" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VIOLET}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}"/>
  </linearGradient>
  <linearGradient id="card" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t["card1"]}"/><stop offset="1" stop-color="{t["card2"]}"/>
  </linearGradient>'''


def cards(t):
    w, h = 1200, 500
    cw, ch, gap = 588, 238, 24
    out = []
    for i, (icon, title, accent, body) in enumerate(CARDS):
        x, y = (i % 2) * (cw + gap), (i // 2) * (ch + gap)
        lines = textwrap.wrap(body, 52)
        text = "".join(f'<tspan x="36" dy="{0 if j == 0 else 27}">{esc(l)}</tspan>' for j, l in enumerate(lines))
        per = 2 * (cw + ch)
        out.append(f'''
<g transform="translate({x} {y})">
  <rect x="1" y="1" width="{cw - 2}" height="{ch - 2}" rx="18" fill="url(#card)" stroke="{t["line"]}" stroke-width="1.5"/>
  <rect x="1" y="1" width="{cw - 2}" height="{ch - 2}" rx="18" fill="url(#glow{i})"/>
  <rect x="1" y="1" width="{cw - 2}" height="{ch - 2}" rx="18" fill="none" stroke="url(#g)" stroke-width="2"
        class="run" stroke-dasharray="180 {per - 180}" style="--per:{per};animation-delay:{-i * 1.6}s"/>
  <g transform="translate(36 34)" fill="none" stroke="{accent}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
    <rect x="-10" y="-10" width="60" height="60" rx="14" fill="{accent}" fill-opacity=".12" stroke="none"/>
    {ICONS[icon]}
  </g>
  <text x="112" y="68" class="title">{esc(title)}</text>
  <text x="36" y="136" class="body">{text}</text>
</g>''')
    glows = "".join(
        f'<radialGradient id="glow{i}" cx="{.1 if i % 2 == 0 else .9}" cy="0" r=".9">'
        f'<stop offset="0" stop-color="{c[2]}" stop-opacity=".16"/><stop offset="1" stop-color="{c[2]}" stop-opacity="0"/></radialGradient>'
        for i, c in enumerate(CARDS))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="What I do: AI agents and workflows, software architecture, full-stack engineering, performance and optimization">
<defs>{defs(t)}{glows}</defs>
<style>
  .title {{ font: 700 27px {SANS}; fill: {t["text"]}; letter-spacing: -.3px; }}
  .body {{ font: 400 18px {SANS}; fill: {t["muted"]}; }}
  .run {{ animation: run 7s linear infinite; }}
  @keyframes run {{ to {{ stroke-dashoffset: calc(var(--per) * -1); }} }}
  @media (prefers-reduced-motion: reduce) {{ .run {{ animation: none; }} }}
</style>
{"".join(out)}
</svg>'''


def timeline(t):
    w, h = 1200, 250
    y = 96
    xs = [150, 450, 750, 1050]
    nodes = []
    for i, ((year, label), x) in enumerate(zip(TIMELINE, xs)):
        last = i == len(TIMELINE) - 1
        lines = textwrap.wrap(label, 26)
        text = "".join(f'<tspan x="{x}" dy="{0 if j == 0 else 22}">{esc(l)}</tspan>' for j, l in enumerate(lines))
        ring = f'<circle cx="{x}" cy="{y}" r="16" fill="none" stroke="{PINK}" stroke-width="2" class="ring"/>' if last else ""
        nodes.append(f'''
  {ring}
  <circle cx="{x}" cy="{y}" r="11" fill="{t["bg"]}" stroke="url(#gh)" stroke-width="3"/>
  <circle cx="{x}" cy="{y}" r="4.5" fill="{PINK if last else CYAN}"/>
  <text x="{x}" y="{y - 36}" class="year" text-anchor="middle">{esc(year)}</text>
  <text x="{x}" y="{y + 50}" class="label" text-anchor="middle">{text}</text>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Journey timeline from 2020 to today">
<defs>{defs(t)}</defs>
<style>
  .year {{ font: 800 24px {SANS}; fill: url(#gh); }}
  .label {{ font: 400 16px {SANS}; fill: {t["muted"]}; }}
  .pulse {{ animation: travel 5s ease-in-out infinite; }}
  .ring {{ transform-box: fill-box; transform-origin: center; animation: ring 2s ease-out infinite; }}
  @keyframes travel {{ from {{ transform: translateX(0); opacity: 0; }} 10% {{ opacity: 1; }} 90% {{ opacity: 1; }} to {{ transform: translateX({xs[-1] - xs[0]}px); opacity: 0; }} }}
  @keyframes ring {{ from {{ transform: scale(.8); opacity: .9; }} to {{ transform: scale(1.8); opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{ .pulse, .ring {{ animation: none; }} }}
</style>
<rect x="{xs[0]}" y="{y - 1.5}" width="{xs[-1] - xs[0]}" height="3" rx="1.5" fill="url(#gh)" opacity=".45"/>
<circle cx="{xs[0]}" cy="{y}" r="5" fill="{CYAN}" class="pulse"/>
{"".join(nodes)}
</svg>'''


def strip(t):
    w, h = 1200, 56
    char_w, pad, sep = 10.2, 22, 14
    widths = [len(s) * char_w + pad * 2 for s in STATS]
    total = sum(widths) + sep * (len(STATS) - 1)
    x = (w - total) / 2
    pills = []
    for s, pw in zip(STATS, widths):
        pills.append(
            f'<rect x="{x:.1f}" y="8" width="{pw:.1f}" height="40" rx="20" fill="url(#card)" stroke="{t["line"]}" stroke-width="1.2"/>'
            f'<circle cx="{x + 14:.1f}" cy="28" r="3" fill="url(#gh)"/>'
            f'<text x="{x + pw / 2 + 5:.1f}" y="33" class="s" text-anchor="middle">{esc(s)}</text>')
        x += pw + sep
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(" · ".join(STATS))}">
<defs>{defs(t)}</defs>
<style>.s {{ font: 600 15px {FONT}; fill: {t["text"]}; letter-spacing: 1.2px; }}</style>
{"".join(pills)}
</svg>'''


for mode, t in THEMES.items():
    (OUT / f"cards-{mode}.svg").write_text(cards(t))
    (OUT / f"timeline-{mode}.svg").write_text(timeline(t))
    (OUT / f"strip-{mode}.svg").write_text(strip(t))
print("ok")
