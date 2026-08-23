import os
import subprocess
import base64

def main():
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    os.makedirs(os.path.join('assets', 'screenshots'), exist_ok=True)

    with open('css/style.css', 'r', encoding='utf-8') as f:
        css_content = f.read()

    font_path = os.path.join('assets', 'fonts', 'MuktaMalar-800-tamil.woff2')
    font_b64 = ""
    if os.path.exists(font_path):
        with open(font_path, 'rb') as ff:
            font_b64 = base64.b64encode(ff.read()).decode('utf-8')

    font_face_style = ""
    if font_b64:
        font_face_style = f"""
        @font-face {{
            font-family: 'Mukta Malar';
            src: url(data:font/woff2;base64,{font_b64}) format('woff2');
            font-weight: 800;
            font-style: normal;
        }}
        """

    def build_page(body_html, extra_css=""):
        return f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    {font_face_style}
    {css_content}
    body {{
      background: #F1EFEA;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
      padding: 0;
      overflow: hidden;
      font-family: 'Mukta Malar', sans-serif;
    }}
    .app-viewport {{
      width: 100%;
      max-width: 560px;
      height: 100vh;
      background: #FAF7F2;
      box-shadow: 0 0 30px rgba(0,0,0,0.12);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 14px 16px;
      box-sizing: border-box;
    }}
    .top-sub1-banner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-bottom: 4px;
      border-bottom: 1px solid var(--border-subtle);
    }}
    .cultural-invocation {{
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }}
    .invocation-tamil {{
      font-size: 0.85rem;
      font-weight: 800;
      color: var(--primary-gold-dark);
    }}
    .invocation-english {{
      font-size: 0.65rem;
      font-weight: 600;
      color: var(--text-muted);
    }}
    .main-title {{
      display: flex;
      flex-direction: column;
      align-items: center;
      margin: 0;
    }}
    .title-primary {{
      font-size: 1.45rem;
      font-weight: 800;
      color: var(--primary-gold-dark);
      letter-spacing: 0.5px;
    }}
    .title-sub {{
      font-size: 0.62rem;
      font-weight: 800;
      color: var(--temple-navy);
      letter-spacing: 2px;
    }}
    .board-row {{
      display: flex;
      justify-content: center;
      gap: 8px;
      margin-bottom: 6px;
    }}
    .grid-tile {{
      width: 58px;
      height: 58px;
      font-size: 1.6rem;
      font-weight: 800;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #FFFFFF;
      border: 2px solid #CBD5E1;
      box-shadow: 0 3px 0 #CBD5E1;
    }}
    .grid-tile.correct {{
      background: #15803D !important;
      border-color: #166534 !important;
      color: #FFFFFF !important;
      box-shadow: 0 3px 0 #166534 !important;
    }}
    .grid-tile.present {{
      background: #D97706 !important;
      border-color: #B45309 !important;
      color: #FFFFFF !important;
      box-shadow: 0 3px 0 #B45309 !important;
    }}
    .grid-tile.absent {{
      background: #64748B !important;
      border-color: #475569 !important;
      color: #FFFFFF !important;
      box-shadow: 0 3px 0 #475569 !important;
    }}
    .key-btn {{
      height: 35px;
      font-size: 1.05rem;
    }}
    {extra_css}
  </style>
</head>
<body>
  {body_html}
</body>
</html>"""

    mei_keys = ['க்','ங்','ச்','ஞ்','ட்','ண்','த்','ந்','ப்','ம்','ய்','ர்','ல்','வ்','ழ்','ள்','ற்','ன்','ஜ்','ஶ்','ஷ்','ஸ்','ஹ்','க்ஷ்']
    uyir_keys = ['அ','ஆ','இ','ஈ','உ','ஊ','எ','ஏ','ஐ','ஒ','ஓ','ஔ','ஃ']

    def render_keypads(sel_mei="ப்", sel_uyir="உ"):
        mei_html = "".join([f'<button class="key-btn {"selected" if k==sel_mei else ""}">{k}</button>' for k in mei_keys])
        uyir_html = "".join([f'<button class="key-btn {"selected" if k==sel_uyir else ""}">{k}</button>' for k in uyir_keys])
        return mei_html, uyir_html

    # Screen 1: 7-inch Tablet (1200x1920) — 3-Letter Gameplay with Clues
    mei_h1, uyir_h1 = render_keypads("ப்", "உ")
    s1_body = f"""
  <div class="app-viewport">
    <header class="top-section">
      <div class="top-sub1-banner">
        <div class="cultural-invocation left-invocation"><span class="invocation-tamil">அன்பே இறை</span><span class="invocation-english">Love is Divine</span></div>
        <h1 class="main-title"><span class="title-primary">சொல்லாடல்</span><span class="title-sub">TAMIL WORD GAME</span></h1>
        <div class="cultural-invocation right-invocation"><span class="invocation-tamil">அறமே வழி</span><span class="invocation-english">Virtue is the Path</span></div>
      </div>
      <div class="top-sub2-controls" style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
        <button class="btn-pill-control">3 எழுத்து ▾</button>
        <button class="btn-tactile btn-next-word">அடுத்த சொல் ❯</button>
        <button class="btn-pill-control">Beginner ▾</button>
      </div>
    </header>

    <main class="middle-section" style="margin: 10px 0;">
      <div class="middle-top-grid">
        <div class="game-board-container">
          <div class="board-row">
            <div class="grid-tile absent">க</div>
            <div class="grid-tile present">வி</div>
            <div class="grid-tile absent">தை</div>
          </div>
          <div class="board-row current-attempt active">
            <div class="grid-tile correct">அ</div>
            <div class="grid-tile present">ன்</div>
            <div class="grid-tile correct">பு</div>
          </div>
          <div class="board-row"><div class="grid-tile"></div><div class="grid-tile"></div><div class="grid-tile"></div></div>
          <div class="board-row"><div class="grid-tile"></div><div class="grid-tile"></div><div class="grid-tile"></div></div>
          <div class="board-row"><div class="grid-tile"></div><div class="grid-tile"></div><div class="grid-tile"></div></div>
          <div class="board-row"><div class="grid-tile"></div><div class="grid-tile"></div><div class="grid-tile"></div></div>
        </div>
      </div>

      <div class="middle-bottom-clues clues-panel" style="margin-top: 10px; display:flex; flex-direction:column; gap:6px;">
        <div class="clue-item-card" style="background:#FFFBEB; border:1.5px solid #D97706; padding:8px 12px; border-radius:8px;">
          <div style="display:flex; align-items:center; gap:6px; font-weight:800; color:#D97706; font-size:0.88rem;">
            <span>💡</span><span>குறிப்பு 1 (பொருள்):</span>
          </div>
          <div style="margin-top:3px; font-size:0.85rem; color:#1E293B;">
            <span style="font-weight:700;">பாசம், நேசம், கருணை</span>
            <span style="font-style:italic; color:#64748B; margin-left:6px;">(Affection, love, kindness)</span>
          </div>
        </div>
        <div class="clue-item-card" style="background:#F8FAFC; border:1px solid #E2E8F0; padding:6px 12px; border-radius:8px;">
          <div style="display:flex; align-items:center; gap:6px; font-weight:800; color:#64748B; font-size:0.82rem;">
            <span>🔒</span><span>குறிப்பு 2 (இலக்கியம்):</span>
            <span style="font-style:italic; font-weight:600; color:#94A3B8; margin-left:4px;">4-வது முயற்சியில் திறக்கும்</span>
          </div>
        </div>
        <div class="clue-item-card" style="background:#F8FAFC; border:1px solid #E2E8F0; padding:6px 12px; border-radius:8px;">
          <div style="display:flex; align-items:center; gap:6px; font-weight:800; color:#64748B; font-size:0.82rem;">
            <span>🔒</span><span>குறிப்பு 3 (விடுகதை):</span>
            <span style="font-style:italic; font-weight:600; color:#94A3B8; margin-left:4px;">5-வது முயற்சியில் திறக்கும்</span>
          </div>
        </div>
      </div>
    </main>

    <footer class="bottom-section">
      <div class="bottom-sub1-combo" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <div class="combo-preview-container">
          <div class="preview-tile highlight">ப்</div>
          <span class="combo-operator">+</span>
          <div class="preview-tile highlight">உ</div>
          <span class="combo-operator">=</span>
          <div class="preview-tile preview-result highlight">பு</div>
          <button class="btn-tactile btn-select-tick">✓</button>
        </div>
        <div class="action-btn-group">
          <button class="btn-tactile btn-nav"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg></button>
          <button class="btn-tactile btn-nav"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg></button>
          <button class="btn-tactile btn-check"><span>சரிபார் ⏎</span></button>
        </div>
      </div>
      <div class="bottom-sub2-keypad">
        <div class="keypad-column mei-column">
          <div class="keypad-subheading">மெய் எழுத்துக்கள் (Mei)</div>
          <div class="keypad-grid" id="mei-keypad" style="grid-template-columns: repeat(6, 1fr);">{mei_h1}</div>
        </div>
        <div class="keypad-vertical-divider"></div>
        <div class="keypad-column uyir-column">
          <div class="keypad-subheading">உயிர் எழுத்துக்கள் (Uyir)</div>
          <div class="keypad-grid" id="uyir-keypad" style="grid-template-columns: repeat(4, 1fr);">{uyir_h1}</div>
        </div>
      </div>
      <div class="bottom-sub3-utilities" style="display:flex; justify-content:center; gap:16px; margin-top:6px;">
        <button class="btn-utility"><span class="util-badge">ழ்</span><span class="util-text">சொல் வங்கி</span></button>
        <button class="btn-utility"><span class="util-badge">?</span><span class="util-text">விளையாடும் முறை</span></button>
      </div>
    </footer>
  </div>
"""

    # Screen 3: 10-inch Tablet (1600x2560) — 5-Letter Win & 3 Clues Unlocked
    mei_h3, uyir_h3 = render_keypads("க்", "அ")
    s3_body = f"""
  <div class="app-viewport">
    <header class="top-section">
      <div class="top-sub1-banner">
        <div class="cultural-invocation left-invocation"><span class="invocation-tamil">அன்பே இறை</span><span class="invocation-english">Love is Divine</span></div>
        <h1 class="main-title"><span class="title-primary">சொல்லாடல்</span><span class="title-sub">TAMIL WORD GAME</span></h1>
        <div class="cultural-invocation right-invocation"><span class="invocation-tamil">அறமே வழி</span><span class="invocation-english">Virtue is the Path</span></div>
      </div>
      <div class="top-sub2-controls" style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
        <button class="btn-pill-control">5 எழுத்து ▾</button>
        <button class="btn-tactile btn-next-word">அடுத்த சொல் ❯</button>
        <button class="btn-pill-control">Intermediate ▾</button>
      </div>
    </header>

    <main class="middle-section" style="margin: 10px 0;">
      <div class="middle-top-grid">
        <div class="game-board-container">
          <div class="board-row">
            <div class="grid-tile absent">பா</div>
            <div class="grid-tile absent">ர</div>
            <div class="grid-tile present">தி</div>
            <div class="grid-tile absent">யா</div>
            <div class="grid-tile absent">ர்</div>
          </div>
          <div class="board-row">
            <div class="grid-tile absent">த</div>
            <div class="grid-tile absent">மி</div>
            <div class="grid-tile absent">ழ</div>
            <div class="grid-tile present">ன்</div>
            <div class="grid-tile absent">சொ</div>
          </div>
          <div class="board-row current-attempt active">
            <div class="grid-tile correct">வ</div>
            <div class="grid-tile correct">ண</div>
            <div class="grid-tile correct">க்</div>
            <div class="grid-tile correct">க</div>
            <div class="grid-tile correct">ம்</div>
          </div>
          <div class="board-row"><div class="grid-tile"></div><div class="grid-tile"></div><div class="grid-tile"></div><div class="grid-tile"></div><div class="grid-tile"></div></div>
          <div class="board-row"><div class="grid-tile"></div><div class="grid-tile"></div><div class="grid-tile"></div><div class="grid-tile"></div><div class="grid-tile"></div></div>
          <div class="board-row"><div class="grid-tile"></div><div class="grid-tile"></div><div class="grid-tile"></div><div class="grid-tile"></div><div class="grid-tile"></div></div>
        </div>
      </div>

      <div class="middle-bottom-clues clues-panel" style="margin-top: 10px; display:flex; flex-direction:column; gap:6px;">
        <div class="clue-item-card" style="background:#FFFBEB; border:1.5px solid #D97706; padding:8px 12px; border-radius:8px;">
          <div style="display:flex; align-items:center; gap:6px; font-weight:800; color:#D97706; font-size:0.88rem;">
            <span>💡</span><span>குறிப்பு 1 (பொருள்):</span>
          </div>
          <div style="margin-top:3px; font-size:0.85rem; color:#1E293B;">
            <span style="font-weight:700;">இரு கைகளையும் கூப்பி அன்போடு வரவேற்பது</span>
            <span style="font-style:italic; color:#64748B; margin-left:6px;">(Traditional respectful greeting)</span>
          </div>
        </div>
        <div class="clue-item-card" style="background:#FFFBEB; border:1px solid #D97706; padding:8px 12px; border-radius:8px;">
          <div style="display:flex; align-items:center; gap:6px; font-weight:800; color:#D97706; font-size:0.88rem;">
            <span>📖</span><span>குறிப்பு 2 (இலக்கியம்):</span>
          </div>
          <div style="margin-top:3px; font-size:0.85rem; color:#1E293B;">
            <span style="font-weight:700;">எல்லார்க்கும் நன்றாம் பணிதல் (திருக்குறள் 95)</span>
            <span style="font-style:italic; color:#64748B; margin-left:6px;">(Humility is virtue for all)</span>
          </div>
        </div>
        <div class="clue-item-card" style="background:#FFFBEB; border:1px solid #D97706; padding:8px 12px; border-radius:8px;">
          <div style="display:flex; align-items:center; gap:6px; font-weight:800; color:#D97706; font-size:0.88rem;">
            <span>🧩</span><span>குறிப்பு 3 (விடுகதை):</span>
          </div>
          <div style="margin-top:3px; font-size:0.85rem; color:#1E293B;">
            <span style="font-weight:700;">இரு கைகள் ஒன்று சேரும்... மரியாதையின் வாசலைத் திறக்கும்...</span>
          </div>
        </div>
      </div>
    </main>

    <footer class="bottom-section">
      <div class="bottom-sub1-combo" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <div class="combo-preview-container">
          <div class="preview-tile highlight">க்</div>
          <span class="combo-operator">+</span>
          <div class="preview-tile highlight">அ</div>
          <span class="combo-operator">=</span>
          <div class="preview-tile preview-result highlight">க</div>
          <button class="btn-tactile btn-select-tick">✓</button>
        </div>
        <div class="action-btn-group">
          <button class="btn-tactile btn-nav"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg></button>
          <button class="btn-tactile btn-nav"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg></button>
          <button class="btn-tactile btn-check"><span>சரிபார் ⏎</span></button>
        </div>
      </div>
      <div class="bottom-sub2-keypad">
        <div class="keypad-column mei-column">
          <div class="keypad-subheading">மெய் எழுத்துக்கள் (Mei)</div>
          <div class="keypad-grid" id="mei-keypad" style="grid-template-columns: repeat(6, 1fr);">{mei_h3}</div>
        </div>
        <div class="keypad-vertical-divider"></div>
        <div class="keypad-column uyir-column">
          <div class="keypad-subheading">உயிர் எழுத்துக்கள் (Uyir)</div>
          <div class="keypad-grid" id="uyir-keypad" style="grid-template-columns: repeat(4, 1fr);">{uyir_h3}</div>
        </div>
      </div>
      <div class="bottom-sub3-utilities" style="display:flex; justify-content:center; gap:16px; margin-top:6px;">
        <button class="btn-utility"><span class="util-badge">ழ்</span><span class="util-text">சொல் வங்கி</span></button>
        <button class="btn-utility"><span class="util-badge">?</span><span class="util-text">விளையாடும் முறை</span></button>
      </div>
    </footer>
  </div>
"""

    screens = [
        ("temp_tab1.html", build_page(s1_body), "tablet-7inch-screenshot-1.png", 1200, 1920, 2.0),
        ("temp_tab3.html", build_page(s3_body), "tablet-10inch-screenshot-1.png", 1600, 2560, 2.5),
    ]

    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_bin = next((p for p in edge_paths if os.path.exists(p)), None)

    for temp_f, html, png_name, w, h, scale in screens:
        with open(temp_f, 'w', encoding='utf-8') as f:
            f.write(html)

        out_desktop = os.path.join(desktop, png_name)
        out_assets = os.path.join('assets', 'screenshots', png_name)
        vp_w = int(w / scale)
        vp_h = int(h / scale)

        cmd = [
            edge_bin,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--force-device-scale-factor={scale}",
            f"--window-size={vp_w},{vp_h}",
            f"--screenshot={out_desktop}",
            f"file:///{os.path.abspath(temp_f).replace(os.sep, '/')}"
        ]
        print(f"Rendering {png_name} ({w}x{h})...")
        subprocess.run(cmd, capture_output=True, text=True)

        if os.path.exists(out_desktop):
            with open(out_desktop, 'rb') as src, open(out_assets, 'wb') as dst:
                dst.write(src.read())
            size_kb = os.path.getsize(out_desktop) / 1024
            print(f"  -> SUCCESS: {out_desktop} ({size_kb:.1f} KB)")
        else:
            print(f"  -> FAILED: {png_name}")

        if os.path.exists(temp_f):
            os.remove(temp_f)

if __name__ == '__main__':
    main()
