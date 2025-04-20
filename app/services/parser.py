import requests
import math
import random

from bs4 import BeautifulSoup

def parser_science_news():
    category = ['astronomy', 'cosmonautics', 'physics', 'chemistry', 'medicine', 'biology']
    category_for_news = random.choice(category)
    
    base_url = "https://naked-science.ru/article"
    res = requests.get(f"{base_url}/{category_for_news}")
    soup = BeautifulSoup(res.text, "html.parser")

    articles = soup.select(".news-item-title")
    hrefs = [a.find("a")["href"] for a in articles if a.find("a")]
    news = []

    score_list = {
        1: "Не цікаво",
        2: "Таке",
        3: "Середнє",
        4: "Цікаво",
        5: "Потрібно подивитися",
    }

    for href in hrefs:
        if not href:
            continue
        try:
            res = requests.get(href)
            soup = BeautifulSoup(res.text, "html.parser")
            post_info = soup.find("div", class_="content")

            post_rating_text = post_info.select_one(".post-raitng")
            post_rating = post_rating_text.text if post_rating_text else ""

            meta_grid = post_info.find("div", class_="meta-items grid")
            post_view_text = meta_grid.select_one(".fvc-view") if meta_grid else None
            post_view = post_view_text.text if post_view_text else ""

            rating_score = 0
            for part in (post_view + " " + post_rating).split():
                if part.isdigit():
                    rating_score = int(part)

            if rating_score > 300:
                post_body_description = soup.find("div", class_="body")
                
                post_title = post_info.select_one(".post-title")
                post_lead = post_info.select_one(".post-lead")
                
                paragraphs = post_body_description.find_all("p") if post_body_description else []

                description = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

                post_img_url = None
                try:
                    img_container = soup.find("div", class_="post-image-container")
                    if img_container:
                        img_tag = img_container.select_one("img")
                        post_img_url = img_tag.get("data-lazy-src")
                except:
                    post_img_url = None

                score = 5 * (1 - math.exp(-rating_score / 300))
                rounded_score = min(5, max(1, round(score)))
                rating_name = score_list[rounded_score]
                news.append({
                    "title": post_title.text.strip() if post_title else "No title",
                    "rating": rating_name,
                    "lead": post_lead.text.strip() if post_lead else "No lead",
                    "description": description if description else "No description",
                    "image_url": post_img_url,
                })
        except Exception as ex:
            print(f"Error while processing {href}: {ex}")
            continue

    return news