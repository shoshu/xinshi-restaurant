import csv
import html
from pathlib import Path
import re

DATA_FILE = Path('restaurent_xinshi.csv')
OUTPUT_DIR = Path('docs')
RESTAURANT_DIR = OUTPUT_DIR / 'restaurants'


def slugify(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", '-', name)
    name = re.sub(r"-+", '-', name).strip('-')
    return name or 'restaurant'


def read_restaurants():
    with DATA_FILE.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        restaurants = [row for row in reader]
    for r in restaurants:
        r['Name'] = r['Name'].strip()
        r['Slug'] = slugify(r['Name'])
    restaurants.sort(key=lambda r: r['Name'])
    return restaurants


def ensure_output_dirs():
    OUTPUT_DIR.mkdir(exist_ok=True)
    RESTAURANT_DIR.mkdir(parents=True, exist_ok=True)


def write_css():
    css = (
        """
        :root {
            --bg: #0b1021;
            --card: #141b36;
            --text: #eef2ff;
            --muted: #9fb3d9;
            --accent: #7dc4ff;
            --accent-strong: #4ac6e4;
        }
        * { box-sizing: border-box; }
        body {
            font-family: 'Inter', 'Noto Sans TC', system-ui, -apple-system, sans-serif;
            margin: 0;
            background: radial-gradient(circle at 20% 20%, rgba(125,196,255,0.12), transparent 35%),
                        radial-gradient(circle at 80% 0%, rgba(74,198,228,0.2), transparent 40%),
                        linear-gradient(145deg, #050814, #0b1021 60%);
            color: var(--text);
            min-height: 100vh;
        }
        header {
            padding: 48px 24px 24px;
            text-align: center;
        }
        header h1 { margin: 0; font-size: 2.4rem; letter-spacing: 0.03em; }
        header p { margin: 8px 0 0; color: var(--muted); }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
            padding: 24px;
            max-width: 1200px;
            margin: 0 auto 48px;
        }
        .card {
            background: linear-gradient(145deg, rgba(20,27,54,0.9), rgba(20,27,54,0.7));
            border: 1px solid rgba(125,196,255,0.2);
            border-radius: 14px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.35);
            overflow: hidden;
            transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
            text-decoration: none;
            color: inherit;
            backdrop-filter: blur(6px);
        }
        .card:hover {
            transform: translateY(-4px);
            border-color: rgba(125,196,255,0.45);
            box-shadow: 0 18px 46px rgba(0,0,0,0.42);
        }
        .card img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            display: block;
        }
        .card .content { padding: 14px 16px 18px; }
        .card h2 { margin: 0 0 6px; font-size: 1.1rem; }
        .pill-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
        .pill {
            padding: 4px 10px;
            border-radius: 999px;
            border: 1px solid rgba(125,196,255,0.5);
            color: var(--accent);
            font-size: 0.85rem;
        }
        .meta { color: var(--muted); font-size: 0.92rem; margin: 0; }
        .meta strong { color: var(--text); }
        main { max-width: 960px; margin: 0 auto; padding: 32px 24px 64px; }
        .hero {
            display: grid;
            grid-template-columns: minmax(240px, 1fr) 1.5fr;
            gap: 20px;
            align-items: center;
        }
        .hero img {
            width: 100%;
            border-radius: 18px;
            border: 1px solid rgba(125,196,255,0.25);
            box-shadow: 0 20px 40px rgba(0,0,0,0.35);
        }
        .hero h1 { margin: 0 0 12px; font-size: 2.2rem; }
        .hero .meta-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; margin-top: 16px; }
        .meta-box {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(125,196,255,0.25);
            border-radius: 12px;
            padding: 12px;
        }
        .meta-box span { display: block; color: var(--muted); font-size: 0.88rem; }
        .meta-box strong { color: var(--text); font-size: 1.05rem; }
        a.button {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: linear-gradient(135deg, #4ac6e4, #7dc4ff);
            color: #041124;
            padding: 12px 16px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            box-shadow: 0 14px 30px rgba(74,198,228,0.35);
        }
        a.button:hover { transform: translateY(-1px); box-shadow: 0 16px 36px rgba(74,198,228,0.42); }
        .back-link { color: var(--accent); text-decoration: none; }
        @media (max-width: 780px) {
            .hero { grid-template-columns: 1fr; }
        }
        footer {
            color: var(--muted);
            text-align: center;
            padding: 24px;
            font-size: 0.9rem;
        }
        """
    )
    (OUTPUT_DIR / 'styles.css').write_text(css.strip() + '\n', encoding='utf-8')


def render_index(restaurants):
    cards = []
    for r in restaurants:
        cards.append(
            "\n".join(
                [
                    f"            <a class='card' href='restaurants/{r['Slug']}.html'>",
                    f"                <img src='{html.escape(r['Thumbnail'])}' alt='{html.escape(r['Name'])}'>",
                    "                <div class='content'>",
                    f"                    <h2>{html.escape(r['Name'])}</h2>",
                    "                    <div class='pill-row'>",
                    f"                        <span class='pill'>評分 {html.escape(r['Rating'])}</span>",
                    f"                        <span class='pill'>{html.escape(r['Price'])}</span>",
                    f"                        <span class='pill'>{html.escape(r['Type'])}</span>",
                    "                    </div>",
                    f"                    <p class='meta'><strong>地址：</strong>{html.escape(r['Address'])}</p>",
                    "                </div>",
                    "            </a>",
                ]
            )
        )

    html_page = f"""
    <!doctype html>
    <html lang='zh-Hant'>
    <head>
        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <title>新市美食地圖</title>
        <link rel='stylesheet' href='styles.css'>
    </head>
    <body>
        <header>
            <h1>新市餐廳地圖</h1>
            <p>為每一家店鋪建立專屬頁面，快速找到想吃的料理。</p>
        </header>
        <div class='grid'>
{chr(10).join(cards)}
        </div>
        <footer>資料來源：restaurent_xinshi.csv · 共有 {len(restaurants)} 間餐廳</footer>
    </body>
    </html>
    """
    (OUTPUT_DIR / 'index.html').write_text(html_page.strip() + '\n', encoding='utf-8')


def render_detail(r):
    page = f"""
    <!doctype html>
    <html lang='zh-Hant'>
    <head>
        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <title>{html.escape(r['Name'])}｜新市餐廳地圖</title>
        <link rel='stylesheet' href='../styles.css'>
    </head>
    <body>
        <main>
            <p><a class='back-link' href='../index.html'>← 返回所有餐廳</a></p>
            <section class='hero'>
                <img src='{html.escape(r['Thumbnail'])}' alt='{html.escape(r['Name'])}'>
                <div>
                    <h1>{html.escape(r['Name'])}</h1>
                    <div class='pill-row'>
                        <span class='pill'>評分 {html.escape(r['Rating'])}</span>
                        <span class='pill'>{html.escape(r['Price'])}</span>
                        <span class='pill'>{html.escape(r['Type'])}</span>
                    </div>
                    <div class='meta-grid'>
                        <div class='meta-box'><span>地址</span><strong>{html.escape(r['Address'])}</strong></div>
                        <div class='meta-box'><span>Google 地圖</span><strong><a class='back-link' href='{html.escape(r['GoogleMapLink'])}' target='_blank' rel='noopener'>開啟連結</a></strong></div>
                    </div>
                </div>
            </section>
        </main>
    </body>
    </html>
    """
    (RESTAURANT_DIR / f"{r['Slug']}.html").write_text(page.strip() + '\n', encoding='utf-8')


def render_details(restaurants):
    for r in restaurants:
        render_detail(r)


def main():
    restaurants = read_restaurants()
    ensure_output_dirs()
    write_css()
    render_index(restaurants)
    render_details(restaurants)
    print(f"Generated {len(restaurants)} restaurant pages and index in {OUTPUT_DIR}/")


if __name__ == '__main__':
    main()
