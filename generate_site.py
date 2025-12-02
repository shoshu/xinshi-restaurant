import csv
import html
import os
import pathlib
import re
from typing import List, Dict

ROOT = pathlib.Path(__file__).parent
CSV_PATH = ROOT / "restaurent_xinshi.csv"
DOCS_DIR = ROOT / "docs"
RESTAURANTS_DIR = DOCS_DIR / "restaurants"
STYLE_PATH = DOCS_DIR / "styles.css"


def slugify(name: str) -> str:
    # Allow alphanumerics and common CJK ranges; replace other characters with dashes
    safe = re.sub(r"[^\w\u4e00-\u9fff]+", "-", name.strip(), flags=re.UNICODE)
    return safe.strip("-") or "restaurant"


def load_restaurants() -> List[Dict[str, str]]:
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def ensure_dirs():
    RESTAURANTS_DIR.mkdir(parents=True, exist_ok=True)


def write_styles():
    STYLE_PATH.write_text(
        """
        :root {
          --bg: #f7f7f9;
          --card: #ffffff;
          --accent: #ce1f51;
          --text: #1f2d3d;
          --muted: #5f6b7a;
        }
        * { box-sizing: border-box; }
        body {
          font-family: 'Segoe UI', 'Noto Sans TC', sans-serif;
          margin: 0;
          background: var(--bg);
          color: var(--text);
        }
        a { color: var(--accent); text-decoration: none; }
        header {
          background: linear-gradient(135deg, #ff8fa3, #f45d75);
          color: white;
          padding: 2.5rem 1.25rem;
          text-align: center;
        }
        header h1 { margin: 0 0 0.35rem; }
        header p { margin: 0; color: rgba(255,255,255,0.9); }
        main { max-width: 1100px; margin: -2.5rem auto 3rem; padding: 0 1.25rem; }
        .grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
          gap: 1rem;
        }
        .card {
          background: var(--card);
          border-radius: 14px;
          box-shadow: 0 15px 40px rgba(0,0,0,0.05);
          overflow: hidden;
          display: flex;
          flex-direction: column;
          transition: transform 150ms ease, box-shadow 150ms ease;
        }
        .card:hover { transform: translateY(-4px); box-shadow: 0 18px 48px rgba(0,0,0,0.08); }
        .card img { width: 100%; height: 160px; object-fit: cover; }
        .card .content { padding: 1rem; flex: 1; display: flex; flex-direction: column; gap: 0.3rem; }
        .pill {
          display: inline-block;
          background: rgba(206,31,81,0.12);
          color: var(--accent);
          padding: 0.2rem 0.6rem;
          border-radius: 999px;
          font-size: 0.85rem;
        }
        .muted { color: var(--muted); font-size: 0.95rem; }
        .details { max-width: 780px; margin: 0 auto; background: var(--card); padding: 1.5rem; border-radius: 14px; box-shadow: 0 15px 40px rgba(0,0,0,0.05); }
        .details img { width: 100%; max-height: 360px; object-fit: cover; border-radius: 10px; }
        .section { margin-top: 1rem; }
        nav { margin-bottom: 1rem; }
        nav a { font-weight: 600; }
        footer { text-align: center; padding: 2rem 1rem; color: var(--muted); font-size: 0.9rem; }
        @media (max-width: 600px) { header { padding: 2rem 1rem; } .card img { height: 140px; } }
        """,
        encoding="utf-8",
    )


def render_index(restaurants: List[Dict[str, str]]):
    cards = []
    for row in restaurants:
        slug = slugify(row["Name"])
        cards.append(
            f"""
            <article class='card'>
              <a href="restaurants/{html.escape(slug)}.html" aria-label="{html.escape(row['Name'])} 專頁">
                <img src="{html.escape(row['Thumbnail'])}" alt="{html.escape(row['Name'])} thumbnail" loading="lazy" />
              </a>
              <div class='content'>
                <div class='pill'>{html.escape(row['Type'])}</div>
                <h3><a href="restaurants/{html.escape(slug)}.html">{html.escape(row['Name'])}</a></h3>
                <div class='muted'>評分 {html.escape(row['Rating'])} · 價位 {html.escape(row['Price'])}</div>
                <div class='muted'>{html.escape(row['Address'])}</div>
              </div>
            </article>
            """
        )
    cards_html = "\n".join(cards)
    index_html = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>新市餐廳地圖</title>
      <link rel="stylesheet" href="styles.css" />
    </head>
    <body>
      <header>
        <h1>新市餐廳地圖</h1>
        <p>瀏覽每家店的評價、價位與位置，快速找到下一餐的好去處。</p>
      </header>
      <main>
        <section class='grid'>
          {cards_html}
        </section>
      </main>
      <footer>資料來源：restaurent_xinshi.csv</footer>
    </body>
    </html>
    """
    (DOCS_DIR / "index.html").write_text(index_html, encoding="utf-8")


def render_detail(row: Dict[str, str]):
    slug = slugify(row["Name"])
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>{html.escape(row['Name'])}</title>
      <link rel="stylesheet" href="../styles.css" />
    </head>
    <body>
      <header>
        <h1>{html.escape(row['Name'])}</h1>
        <p>評分 {html.escape(row['Rating'])} · 價位 {html.escape(row['Price'])} · {html.escape(row['Type'])}</p>
      </header>
      <main>
        <div class='details'>
          <img src="{html.escape(row['Thumbnail'])}" alt="{html.escape(row['Name'])} 照片" loading="lazy" />
          <div class='section'>
            <strong>地址：</strong> {html.escape(row['Address'])}
          </div>
          <div class='section'>
            <a class='pill' href="{html.escape(row['GoogleMapLink'])}">在 Google 地圖開啟</a>
          </div>
          <nav class='section'>
            <a href="../index.html">← 回到總覽</a>
          </nav>
        </div>
      </main>
      <footer>資料來源：restaurent_xinshi.csv</footer>
    </body>
    </html>
    """
    (RESTAURANTS_DIR / f"{slug}.html").write_text(html_content, encoding="utf-8")


def main():
    restaurants = load_restaurants()
    ensure_dirs()
    write_styles()
    render_index(restaurants)
    for row in restaurants:
        render_detail(row)


if __name__ == "__main__":
    main()
