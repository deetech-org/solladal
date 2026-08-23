import os
import subprocess
import base64

def main():
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    out_png_desktop = os.path.join(desktop, 'icon-512.png')
    out_png_assets = os.path.join('assets', 'icons', 'icon-512.png')
    
    with open('assets/icons/icon-512.svg', 'r', encoding='utf-8') as f:
        svg_content = f.read()

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

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{font_face_style}
* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}
html, body {{
  width: 512px;
  height: 512px;
  overflow: hidden;
  background: transparent;
}}
svg {{
  width: 512px;
  height: 512px;
  display: block;
}}
</style>
</head>
<body>
{svg_content}
</body>
</html>
"""
    temp_html = os.path.abspath('temp_render_icon.html')
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_bin = next((p for p in edge_paths if os.path.exists(p)), None)
    if not edge_bin:
        print("Error: Microsoft Edge not found.")
        return

    cmd = [
        edge_bin,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "--window-size=512,512",
        f"--screenshot={out_png_desktop}",
        f"file:///{temp_html.replace(os.sep, '/')}"
    ]

    print(f"Rendering {out_png_desktop} via headless browser...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(out_png_desktop):
        with open(out_png_desktop, 'rb') as src, open(out_png_assets, 'wb') as dst:
            dst.write(src.read())
        size_kb = os.path.getsize(out_png_desktop) / 1024
        print(f"SUCCESS: Saved 512x512 PNG ({size_kb:.1f} KB) to:")
        print(f"  -> {out_png_desktop}")
        print(f"  -> {out_png_assets}")
    else:
        print("Failed to render screenshot. stderr:", res.stderr)

    if os.path.exists(temp_html):
        os.remove(temp_html)

if __name__ == '__main__':
    main()
