import csv
import html
import pathlib
import re
from typing import List, Dict

DATA_PATH = pathlib.Path('restaurent_xinshi.csv')
OUTPUT_DIR = pathlib.Path('docs')
REST_DIR = OUTPUT_DIR / 'restaurants'
STYLE_PATH = OUTPUT_DIR / 'style.css'


def load_restaurants(path: pathlib.Path) -> List[Dict[str, str]]:
    with path.open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        restaurants = []
        for row in reader:
            # Normalize potential BOM on first header
            if '\ufeffGoogleMapLink' in row:
                row['GoogleMapLink'] = row.pop('\ufeffGoogleMapLink')
            restaurants.append(row)
    return restaurants


def slugify(name: str) -> str:
    normalized = re.sub(r'[^\w\s-]', '', name)
    normalized = re.sub(r'\s+', '-', normalized.strip())
    slug = normalized.lower()
    return slug or 'restaurant'


def ensure_dirs():
    OUTPUT_DIR.mkdir(exist_ok=True)
    REST_DIR.mkdir(exist_ok=True)


def write_style():
    STYLE_PATH.write_text(
        """
        :root {
            color-scheme: light;
            --bg: #f5f5f5;
            --card-bg: #ffffff;
            --text: #1f1f1f;
            --accent: #1976d2;
            --muted: #555;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: 'Segoe UI', 'Noto Sans TC', system-ui, -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
        }
        header {
            background: linear-gradient(135deg, #1e88e5, #42a5f5);
            color: white;
            padding: 32px 16px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }
        header h1 { margin: 0 0 8px; font-size: 2rem; }
        header p { margin: 0; font-size: 1.05rem; }
        main { max-width: 1100px; margin: 24px auto 48px; padding: 0 16px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
        .card {
            background: var(--card-bg);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 6px 16px rgba(0,0,0,0.08);
            transition: transform 0.15s ease, box-shadow 0.2s ease;
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
        }
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.12);
        }
        .card img { width: 100%; height: 160px; object-fit: cover; background: #ddd; }
        .card-body { padding: 14px 16px 16px; flex: 1; display: flex; flex-direction: column; gap: 6px; }
        .name { font-weight: 700; font-size: 1.1rem; }
        .meta { display: flex; gap: 10px; color: var(--muted); font-size: 0.95rem; align-items: center; }
        .meta span { display: inline-flex; align-items: center; gap: 6px; }
        .pill { background: #e3f2fd; color: #0d47a1; padding: 6px 10px; border-radius: 999px; font-weight: 600; font-size: 0.9rem; align-self: flex-start; }
        .address { color: var(--muted); font-size: 0.95rem; }
        footer { text-align: center; color: var(--muted); margin: 24px 0; font-size: 0.9rem; }
        .back { display: inline-block; margin-bottom: 12px; color: var(--accent); font-weight: 600; text-decoration: none; }
        .details { background: var(--card-bg); border-radius: 12px; padding: 16px; box-shadow: 0 6px 16px rgba(0,0,0,0.08); }
        .map-link { display: inline-flex; align-items: center; gap: 8px; padding: 10px 14px; border-radius: 10px; background: #e8f1ff; color: var(--accent); font-weight: 600; text-decoration: none; margin-top: 12px; }
        @media (max-width: 600px) {
            header h1 { font-size: 1.5rem; }
            .card img { height: 140px; }
        }
        """,
        encoding="utf-8",
    )


def render_index(restaurants: List[Dict[str, str]]):
    cards = []
    for r in restaurants:
        slug = slugify(r['Name'])
        cards.append(
            f"""
            <a class="card" href="restaurants/{html.escape(slug)}.html">
                <img src="{html.escape(r['Thumbnail'])}" alt="{html.escape(r['Name'])}">
                <div class="card-body">
                    <div class="name">{html.escape(r['Name'])}</div>
                    <div class="meta">
                        <span>⭐ {html.escape(r['Rating'])}</span>
                        <span>💲 {html.escape(r['Price'])}</span>
                    </div>
                    <div class="pill">{html.escape(r['Type'])}</div>
                    <div class="address">📍 {html.escape(r['Address'])}</div>
                </div>
            </a>
            """
        )

    OUTPUT_DIR.joinpath('index.html').write_text(
        f"""
        <!doctype html>
        <html lang="zh-Hant">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>台南新市餐廳地圖</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <header>
                <h1>台南新市餐廳索引</h1>
                <p>瀏覽餐廳名單，點擊卡片開啟各店的獨立頁面。</p>
            </header>
            <main>
                <div class="grid">
                    {''.join(cards)}
                </div>
            </main>
            <footer>資料來源：restaurent_xinshi.csv</footer>
        </body>
        </html>
        """,
        encoding="utf-8",
    )


def render_restaurant_page(r: Dict[str, str]):
    slug = slugify(r['Name'])
    REST_DIR.joinpath(f"{slug}.html").write_text(
        f"""
        <!doctype html>
        <html lang="zh-Hant">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{html.escape(r['Name'])} | 餐廳介紹</title>
            <link rel="stylesheet" href="../style.css">
        </head>
        <body>
            <header>
                <h1>{html.escape(r['Name'])}</h1>
                <p>{html.escape(r['Type'])}</p>
            </header>
            <main>
                <a class="back" href="../index.html">← 返回列表</a>
                <div class="details">
                    <img src="{html.escape(r['Thumbnail'])}" alt="{html.escape(r['Name'])}" style="width:100%; border-radius: 10px; object-fit: cover; max-height: 320px;">
                    <div class="meta" style="margin-top:12px;">
                        <span>⭐ 評分：{html.escape(r['Rating'])}</span>
                        <span>💰 價位：{html.escape(r['Price'])}</span>
                    </div>
                    <div class="pill" style="margin-top:12px;">{html.escape(r['Type'])}</div>
                    <p class="address" style="margin-top:12px;">📍 地址：{html.escape(r['Address'])}</p>
                    <a class="map-link" href="{html.escape(r['GoogleMapLink'])}" target="_blank" rel="noopener">🗺️ 在 Google 地圖查看</a>
                </div>
            </main>
            <footer>資料來源：restaurent_xinshi.csv</footer>
        </body>
        </html>
        """,
        encoding="utf-8",
    )


def main():
    restaurants = load_restaurants(DATA_PATH)
    ensure_dirs()
    write_style()
    render_index(restaurants)
    for r in restaurants:
        render_restaurant_page(r)


if __name__ == '__main__':
    main()
