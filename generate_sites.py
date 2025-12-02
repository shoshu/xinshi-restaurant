import csv
import html
import re
from pathlib import Path
from typing import Dict, List

DATA_FILE = Path("restaurent_xinshi.csv")
OUTPUT_DIR = Path("docs")
ASSETS_DIR = OUTPUT_DIR / "assets"


def slugify(name: str, existing: set[str]) -> str:
    """Create a URL-friendly slug for a restaurant name."""
    # Keep Unicode letters/numbers so Chinese店名不會被清空
    base = re.sub(r"[^\w]+", "-", name, flags=re.UNICODE).strip("-").lower()
    base = base or "restaurant"

    slug = base
    counter = 2
    while slug in existing:
        slug = f"{base}-{counter}"
        counter += 1
    existing.add(slug)
    return slug


def read_restaurants() -> List[Dict[str, str]]:
    with DATA_FILE.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        restaurants = []
        used_slugs: set[str] = set()
        for row in reader:
            row = {k: v.strip() for k, v in row.items()}
            row["Slug"] = slugify(row["Name"], used_slugs)
            restaurants.append(row)
    return restaurants


def render_index(restaurants: List[Dict[str, str]]) -> str:
    cards = []
    for restaurant in restaurants:
        thumb = html.escape(restaurant.get("Thumbnail", ""))
        name = html.escape(restaurant["Name"])
        price = html.escape(restaurant.get("Price", ""))
        rating = html.escape(restaurant.get("Rating", ""))
        cuisine = html.escape(restaurant.get("Type", ""))
        address = html.escape(restaurant.get("Address", ""))
        slug = html.escape(restaurant["Slug"])
        cards.append(
            f"""
            <a class=\"card\" href=\"restaurants/{slug}.html\">
                <div class=\"thumbnail\" role=\"presentation\" aria-hidden=\"true\" style=\"background-image: url('{thumb}')\"></div>
                <div class=\"card-body\">
                    <div class=\"card-header\">
                        <h2>{name}</h2>
                        <span class=\"pill\">⭐ {rating}</span>
                    </div>
                    <p class=\"muted\">{cuisine}</p>
                    <p>{address}</p>
                    <div class=\"meta\">價格：{price}</div>
                </div>
            </a>
            """
        )

    cards_html = "\n".join(cards)
    return f"""
    <!doctype html>
    <html lang=\"zh-Hant\">
    <head>
        <meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <title>新市餐廳地圖</title>
        <link rel=\"stylesheet\" href=\"assets/style.css\">
    </head>
    <body>
        <header class=\"page-header\">
            <div>
                <p class=\"eyebrow\">GitHub Pages 專案</p>
                <h1>新市餐廳地圖</h1>
                <p class=\"lead\">選一間好吃的吧！每個餐廳都有自己的介紹頁面與 Google 地圖連結。</p>
            </div>
        </header>
        <main>
            <div class=\"grid\">
                {cards_html}
            </div>
        </main>
        <footer class=\"page-footer\">資料來自 restaurent_xinshi.csv</footer>
    </body>
    </html>
    """


def render_restaurant_page(restaurant: Dict[str, str]) -> str:
    name = html.escape(restaurant["Name"])
    price = html.escape(restaurant.get("Price", ""))
    rating = html.escape(restaurant.get("Rating", ""))
    cuisine = html.escape(restaurant.get("Type", ""))
    address = html.escape(restaurant.get("Address", ""))
    map_link = html.escape(restaurant.get("GoogleMapLink", ""))
    thumbnail = html.escape(restaurant.get("Thumbnail", ""))

    return f"""
    <!doctype html>
    <html lang=\"zh-Hant\">
    <head>
        <meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <title>{name}</title>
        <link rel=\"stylesheet\" href=\"../assets/style.css\">
    </head>
    <body class=\"detail-page\">
        <header class=\"page-header\">
            <div>
                <p class=\"eyebrow\">餐廳專頁</p>
                <h1>{name}</h1>
                <p class=\"lead\">{cuisine} · ⭐ {rating} · {price}</p>
                <p class=\"lead\">地址：{address}</p>
                <div class=\"actions\">
                    <a class=\"button\" href=\"{map_link}\" target=\"_blank\" rel=\"noopener noreferrer\">查看 Google 地圖</a>
                    <a class=\"button ghost\" href=\"../index.html\">返回餐廳列表</a>
                </div>
            </div>
        </header>
        <main>
            <section class=\"hero\">
                <div class=\"hero-image\" style=\"background-image: url('{thumbnail}')\" role=\"presentation\" aria-hidden=\"true\"></div>
                <div class=\"hero-text\">
                    <h2>店家資訊</h2>
                    <ul>
                        <li><strong>評分：</strong>⭐ {rating}</li>
                        <li><strong>價格範圍：</strong>{price}</li>
                        <li><strong>料理種類：</strong>{cuisine}</li>
                        <li><strong>地址：</strong>{address}</li>
                        <li><strong>地圖：</strong><a href=\"{map_link}\" target=\"_blank\" rel=\"noopener noreferrer\">在 Google 地圖打開</a></li>
                    </ul>
                </div>
            </section>
        </main>
    </body>
    </html>
    """


def write_site(restaurants: List[Dict[str, str]]):
    OUTPUT_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)
    restaurant_dir = OUTPUT_DIR / "restaurants"
    restaurant_dir.mkdir(exist_ok=True)

    for stale_page in restaurant_dir.glob("*.html"):
        stale_page.unlink()

    (OUTPUT_DIR / "index.html").write_text(render_index(restaurants), encoding="utf-8")

    for restaurant in restaurants:
        content = render_restaurant_page(restaurant)
        page_path = restaurant_dir / f"{restaurant['Slug']}.html"
        page_path.write_text(content, encoding="utf-8")


def main():
    restaurants = read_restaurants()
    write_site(restaurants)


if __name__ == "__main__":
    main()
