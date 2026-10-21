import html
import json
import math
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="KERZENZEIT · Kerzendesigner",
    page_icon="🕯️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Product-specific color references. Hex values are visual approximations and should
# be calibrated against the final physical wax samples before commercial release.
WAX_COLORS = {
    "Reinweiß": "#F4F0E7",
    "Zitronengelb": "#F4D52E",
    "Kräftiges Rot": "#E52F40",
    "Rosa": "#E88FB7",
    "Violett": "#7839A7",
    "Orange": "#F18B32",
    "Grasgrün": "#55A85B",
    "Kieferngrün": "#426A49",
    "Hellblau": "#77C8E5",
    "Traumblau": "#244AA6",
    "Mokkabraun": "#95634B",
    "Schwarz": "#242424",
}

STRAND_COLORS = {
    "Zitronengelb": WAX_COLORS["Zitronengelb"],
    "Kräftiges Rot": WAX_COLORS["Kräftiges Rot"],
    "Rosa": WAX_COLORS["Rosa"],
    "Violett": WAX_COLORS["Violett"],
    "Orange": WAX_COLORS["Orange"],
    "Grasgrün": WAX_COLORS["Grasgrün"],
    "Kieferngrün": WAX_COLORS["Kieferngrün"],
    "Traumblau": WAX_COLORS["Traumblau"],
    "Mokkabraun": WAX_COLORS["Mokkabraun"],
}

PRESETS = {
    "Color Block": {"base": "Zitronengelb", "accent": "Kräftiges Rot", "accent2": "Orange", "style": "Diagonaler Farbstreifen"},
    "Blütentraum": {"base": "Zitronengelb", "accent": "Rosa", "accent2": "Grasgrün", "style": "Blüten"},
    "Sternennacht": {"base": "Traumblau", "accent": "Zitronengelb", "accent2": "Violett", "style": "Sterne & Punkte"},
    "Natur & Formen": {"base": "Grasgrün", "accent": "Kieferngrün", "accent2": "Mokkabraun", "style": "Botanische Linien"},
    "Farbige Wellen": {"base": "Rosa", "accent": "Orange", "accent2": "Kräftiges Rot", "style": "Wellenlinien"},
    "Minimal": {"base": "Reinweiß", "accent": "Schwarz", "accent2": "Grasgrün", "style": "Minimal"},
}

STYLES = ["Diagonaler Farbstreifen", "Blüten", "Sterne & Punkte", "Botanische Linien", "Wellenlinien", "Geometrische Linien", "Minimal"]


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def hex_points(cx, cy, r, rotation=0):
    pts = []
    for i in range(6):
        a = math.radians(rotation + i * 60)
        pts.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
    return " ".join(pts)


def star_points(cx, cy, outer=15, inner=6, n=5, rotation=-90):
    pts = []
    for i in range(n * 2):
        r = outer if i % 2 == 0 else inner
        a = math.radians(rotation + i * 180 / n)
        pts.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
    return " ".join(pts)


def flower_svg(cx, cy, petal_color, center_color, scale=1.0, petals=5):
    parts = []
    radius = 10 * scale
    petal_r = 5.7 * scale
    for i in range(petals):
        angle = math.radians(i * 360 / petals - 90)
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        parts.append(
            f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{petal_r:.1f}" ry="{petal_r*0.72:.1f}" '
            f'fill="{petal_color}" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="0.7" '
            f'transform="rotate({i*360/petals:.1f} {px:.1f} {py:.1f})"/>'
        )
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{4.0*scale:.1f}" fill="{center_color}" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="0.7"/>')
    return "".join(parts)


def apply_preset():
    """Apply one inspiration preset before the page widgets rerun."""
    selected = PRESETS[st.session_state["preset_name"]]
    st.session_state["base_name"] = selected["base"]
    st.session_state["strand1_name"] = selected["accent"]
    st.session_state["strand2_name"] = selected["accent2"]
    st.session_state["style_name"] = selected["style"]


def render_candle_svg(base_color, accent_color, accent2_color, style, motif_count=3, candle_label="Dein Design"):
    # SVG preview of a slim candle wrapped with raised honeycomb wax texture.
    base_color = esc(base_color)
    accent_color = esc(accent_color)
    accent2_color = esc(accent2_color)
    title = esc(candle_label)
    pieces = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="540" height="720" viewBox="0 0 540 720" role="img" aria-label="Vorschau einer dekorierten Kerze" style="width:100%;height:auto;display:block;max-width:540px;margin:auto">
    <defs>
      <linearGradient id="bg" x1="0" y1="0" x2="0.9" y2="1"><stop offset="0" stop-color="#FBF7EF"/><stop offset="1" stop-color="#EFE5D6"/></linearGradient>
      <linearGradient id="candleShade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000000" stop-opacity="0.17"/><stop offset="0.18" stop-color="#FFFFFF" stop-opacity="0.08"/><stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.00"/><stop offset="1" stop-color="#000000" stop-opacity="0.18"/></linearGradient>
      <pattern id="honeycomb" width="18" height="16" patternUnits="userSpaceOnUse">
        <path d="M4.5 0 L9 2.7 L9 8 L4.5 10.7 L0 8 L0 2.7 Z M13.5 8 L18 10.7 L18 16 L13.5 18.7 L9 16 L9 10.7 Z" fill="none" stroke="#FFFFFF" stroke-opacity="0.34" stroke-width="1.2"/>
        <path d="M4.5 1.5 L7.5 3.3 L7.5 7.2 L4.5 9 L1.5 7.2 L1.5 3.3 Z" fill="#FFFFFF" fill-opacity="0.07"/>
      </pattern>
      <clipPath id="candleClip"><path d="M218 128 C218 108 235 98 270 98 C305 98 322 108 322 128 L322 570 C322 594 299 607 270 607 C241 607 218 594 218 570 Z"/></clipPath>
      <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>
    </defs>
    <rect width="540" height="720" rx="28" fill="url(#bg)"/>
    <circle cx="80" cy="90" r="56" fill="#FFFFFF" opacity="0.30"/>
    <circle cx="458" cy="595" r="82" fill="#FFFFFF" opacity="0.25"/>
    <g opacity="0.42" fill="none" stroke="#C7A86A" stroke-width="1.3">
      <path d="M58 195 C85 170 100 148 105 118 C112 151 127 171 150 183"/>
      <path d="M430 145 C454 170 466 195 466 225 C449 207 432 196 410 194"/>
      <polygon points="445,82 450,94 463,95 453,103 456,116 445,108 434,116 437,103 427,95 440,94"/>
      <circle cx="88" cy="540" r="5"/><circle cx="452" cy="310" r="4"/>
    </g>
    <ellipse cx="270" cy="604" rx="78" ry="19" fill="#51483D" opacity="0.17" filter="url(#shadow)"/>
    <ellipse cx="270" cy="605" rx="57" ry="11" fill="#8C7964" opacity="0.16"/>
    <path d="M270 102 C266 92 274 84 270 74" stroke="#51453A" stroke-width="3" stroke-linecap="round" fill="none"/>
    <path d="M218 128 C218 108 235 98 270 98 C305 98 322 108 322 128 L322 570 C322 594 299 607 270 607 C241 607 218 594 218 570 Z" fill="{base_color}"/>
    <g clip-path="url(#candleClip)"><rect x="218" y="95" width="104" height="520" fill="url(#honeycomb)"/><rect x="218" y="95" width="104" height="520" fill="url(#candleShade)"/></g>
    <ellipse cx="270" cy="128" rx="52" ry="24" fill="{base_color}" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="1.2"/>
    <ellipse cx="270" cy="128" rx="43" ry="17" fill="url(#honeycomb)" opacity="0.9"/>
    <path d="M218 128 C218 108 235 98 270 98 C305 98 322 108 322 128 L322 570 C322 594 299 607 270 607 C241 607 218 594 218 570 Z" fill="none" stroke="#FFFFFF" stroke-opacity="0.30" stroke-width="1.4"/>
    ''']

    # Decorations are deliberately thin and restrained to keep the honeycomb surface visible.
    count = int(motif_count)
    if style == "Diagonaler Farbstreifen":
        pieces.append(f'<path d="M205 245 L335 188 L335 231 L205 288 Z" fill="{accent_color}" stroke="#FFFFFF" stroke-opacity="0.25" stroke-width="1.2"/>')
        pieces.append(f'<path d="M205 245 L335 188 L335 231 L205 288 Z" fill="url(#honeycomb)" opacity="0.6"/>')
        pieces.append(f'<path d="M210 245 L329 193" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="1.1"/>')
    elif style == "Blüten":
        centers = [(263, 228), (290, 283), (248, 340), (284, 395), (258, 451)]
        for i, (x, y) in enumerate(centers[:max(1, count)]):
            pieces.append(flower_svg(x, y, accent_color, accent2_color, scale=0.85 if i % 2 else 0.95, petals=5))
        pieces.append(f'<path d="M266 244 Q280 270 270 288 T251 340 T286 398 T258 462" fill="none" stroke="{accent2_color}" stroke-width="4" stroke-linecap="round"/>')
        for x, y, rot in [(275, 267, -25), (260, 315, 30), (274, 372, -30), (269, 428, 28)][:max(1, count)]:
            pieces.append(f'<ellipse cx="{x}" cy="{y}" rx="10" ry="4.5" fill="{accent2_color}" transform="rotate({rot} {x} {y})"/>')
    elif style == "Sterne & Punkte":
        coords = [(252, 205, 15), (289, 266, 10), (247, 328, 11), (291, 379, 14), (254, 445, 9), (284, 500, 12)]
        for i, (x, y, r) in enumerate(coords[:max(1, count+1)]):
            points = star_points(x, y, outer=r, inner=r*0.44)
            pieces.append(f'<polygon points="{points}" fill="{accent_color}" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="1"/>')
            pieces.append(f'<circle cx="{x+18}" cy="{y+18}" r="2.8" fill="{accent2_color}"/>')
    elif style == "Botanische Linien":
        pieces.append(f'<path d="M258 540 C300 480 228 435 277 380 S231 280 278 205" fill="none" stroke="{accent_color}" stroke-width="4" stroke-linecap="round"/>')
        pieces.append(f'<path d="M280 390 C305 370 305 345 301 330" fill="none" stroke="{accent2_color}" stroke-width="3.5" stroke-linecap="round"/>')
        leaves = [(268, 480, -38), (269, 438, 32), (269, 363, -36), (267, 309, 35), (269, 260, -38), (272, 225, 32)]
        for i, (x,y,rot) in enumerate(leaves[:max(2, count+2)]):
            col = accent2_color if i in (1,4) else accent_color
            pieces.append(f'<path d="M{x} {y} q{-18} {-18} {-20} {-4} q4 16 20 4 Z" fill="{col}" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="0.8" transform="rotate({rot} {x} {y})"/>')
    elif style == "Wellenlinien":
        pieces.append(f'<path d="M214 230 C245 205 294 255 326 225 M214 290 C245 265 294 315 326 285 M214 350 C245 325 294 375 326 345 M214 410 C245 385 294 435 326 405" fill="none" stroke="{accent_color}" stroke-width="4.2" stroke-linecap="round"/>')
        pieces.append(f'<path d="M214 260 C245 235 294 285 326 255 M214 320 C245 295 294 345 326 315 M214 380 C245 355 294 405 326 375" fill="none" stroke="{accent2_color}" stroke-width="3" stroke-linecap="round"/>')
    elif style == "Geometrische Linien":
        pieces.append(f'<path d="M216 235 L322 280 M216 290 L322 335 M216 345 L322 390 M216 400 L322 445" fill="none" stroke="{accent_color}" stroke-width="4" stroke-linecap="round"/>')
        pieces.append(f'<path d="M216 255 L322 300 M216 310 L322 355 M216 365 L322 410" fill="none" stroke="{accent2_color}" stroke-width="3" stroke-linecap="round"/>')
    else:  # Minimal
        pieces.append(flower_svg(270, 320, accent_color, accent2_color, scale=0.95, petals=5))
        pieces.append(f'<path d="M270 338 C286 363 258 385 270 408" fill="none" stroke="{accent2_color}" stroke-width="3" stroke-linecap="round"/>')
        pieces.append(f'<ellipse cx="270" cy="390" rx="10" ry="4.5" fill="{accent2_color}" transform="rotate(-35 270 390)"/>')

    pieces.append(f'''
    <text x="270" y="657" text-anchor="middle" font-family="Georgia,serif" font-size="24" fill="#38342F">KERZENZEIT</text>
    <text x="270" y="682" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" letter-spacing="2.4" fill="#81766A">{title}</text>
    </svg>''')
    return "".join(pieces)


st.markdown("""
<style>
  .stApp { background: #faf7f0; color: #302e2a; }
  h1, h2, h3 { color: #302e2a; }
  .hero { padding: 1.0rem 0 0.3rem 0; }
  .kicker { letter-spacing: .18em; text-transform: uppercase; color: #8a795d; font-size: .72rem; font-weight: 700; }
  .subtext { color: #756d62; font-size: 1rem; line-height: 1.5; }
  .swatch { display: inline-block; width: 16px; height: 16px; border-radius: 50%; vertical-align: middle; border: 1px solid rgba(0,0,0,.12); margin-right: 6px; }
  div[data-testid="stDownloadButton"] button { border-radius: 12px; }
  .note { font-size: .82rem; color: #6c665d; line-height: 1.4; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><div class="kicker">KERZENZEIT · DEIN KREATIV-GUIDE</div><h1>Gestalte deine eigene Designkerze</h1><p class="subtext">Wähle deine Wachsfarbe, kombiniere Wachsstränge und entdecke dein persönliches Kerzendesign.</p></div>', unsafe_allow_html=True)

with st.expander("So funktioniert dein Kerzendesigner", expanded=False):
    st.write("1. Wähle die Farbe deiner Wachsplatte. 2. Wähle zwei Farben für deine Wachsstränge. 3. Entscheide dich für ein Muster und passe die Dekoration an. Die Vorschau ist eine kreative Orientierung und kein maßstabsgetreues Produktmuster.")

left, right = st.columns([0.92, 1.08], gap="large")

# Initialize widget state once. Selecting a preset subsequently updates all four design controls.
if "preset_name" not in st.session_state:
    st.session_state["preset_name"] = "Color Block"
_initial_preset = PRESETS[st.session_state["preset_name"]]
for _key, _value in {
    "base_name": _initial_preset["base"],
    "strand1_name": _initial_preset["accent"],
    "strand2_name": _initial_preset["accent2"],
    "style_name": _initial_preset["style"],
}.items():
    if _key not in st.session_state:
        st.session_state[_key] = _value

with left:
    st.subheader("1 · Farben & Stil")
    st.selectbox("Lass dich inspirieren", list(PRESETS.keys()), key="preset_name", on_change=apply_preset)
    base_name = st.selectbox("Farbe der Wachsplatte", list(WAX_COLORS.keys()), key="base_name")
    strand1_name = st.selectbox("Wachsstrang · Farbe 1", list(STRAND_COLORS.keys()), key="strand1_name")
    strand2_name = st.selectbox("Wachsstrang · Farbe 2", list(STRAND_COLORS.keys()), key="strand2_name")
    style = st.selectbox("Dekorationsstil", STYLES, key="style_name")
    motif_count = st.slider("Dekorationsmenge", min_value=1, max_value=5, value=3, key="motif_count", help="Steuert die Anzahl der Motive in der Vorschau, soweit der gewählte Stil dies unterstützt.")
    design_name = st.text_input("Name deiner Kerze", value="Meine Designkerze", max_chars=32, key="design_name")

with right:
    st.subheader("2 · Deine Vorschau")
    svg = render_candle_svg(WAX_COLORS[base_name], STRAND_COLORS[strand1_name], STRAND_COLORS[strand2_name], style, motif_count, design_name.strip() or "Meine Designkerze")
    components.html(svg, height=620, scrolling=False)
    st.caption("Vorschau: schlanke Kerze mit Wabenstruktur und handgeformten Wachsdetails.")

config = {
    "design_name": design_name.strip() or "Meine Designkerze",
    "wax_sheet_color": {"name_de": base_name, "hex": WAX_COLORS[base_name]},
    "wax_strand_color_1": {"name_de": strand1_name, "hex": STRAND_COLORS[strand1_name]},
    "wax_strand_color_2": {"name_de": strand2_name, "hex": STRAND_COLORS[strand2_name]},
    "style": style,
    "motif_count": motif_count,
    "note": "Digitale Designvorschau; tatsächliche Farben können je nach Materialcharge und Bildschirm abweichen. Dekorierte Kerzen nur anzünden, wenn ihr Brennverhalten geprüft wurde."
}

st.markdown("### 3 · Design mitnehmen")
c1, c2 = st.columns(2)
with c1:
    st.download_button(
        "⬇️ Design als SVG speichern",
        data=svg.encode("utf-8"),
        file_name="kerzenzeit-design.svg",
        mime="image/svg+xml",
        use_container_width=True,
    )
with c2:
    st.download_button(
        "⬇️ Farbkombination speichern",
        data=json.dumps(config, ensure_ascii=False, indent=2).encode("utf-8"),
        file_name="kerzenzeit-farbkombination.json",
        mime="application/json",
        use_container_width=True,
    )

st.markdown("""
<div class="note">
<strong>Hinweis:</strong> Diese Vorschau dient der kreativen Inspiration. Die dargestellten Farbtöne sind Näherungen an die Materialfarben. Bei dekorierten Kerzen muss die Brennsicherheit des fertigen Designs geprüft sein; andernfalls bitte nur als Dekoration verwenden.
</div>
""", unsafe_allow_html=True)

with st.expander("Impressum / Kontakt (für die spätere Veröffentlichung)"):
    st.write("Hier vor Veröffentlichung die Angaben des verantwortlichen Unternehmens ergänzen: Peakqust, Kontakt-E-Mail und gegebenenfalls Datenschutzinformationen.")
