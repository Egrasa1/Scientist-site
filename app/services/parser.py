import requests
import math
from bs4 import BeautifulSoup


def parser_science_news():
    base_url = "https://naked-science.ru"
    res = requests.get(f"{base_url}/community")
    soup = BeautifulSoup(res.text, "html.parser")

    articles = soup.select(".shesht-comment-template__pagelink a")
    news = []

    score_list = {
        1: "Не цікаво",
        2: "Таке",
        3: "Середнє",
        4: "Цікаво",
        5: "Потрібно подивитися",
    }

    for arti in articles:
        href = arti.get('href')
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


parser_science_news()

# url = 'https://naked-science.ru/community/1067516'
# res = requests.get(url)

# soup = BeautifulSoup(res.text, 'html.parser')

# score_list = {
#         1: 'Не цікаво',
#         2: 'Таке',
#         3: 'Середнє',
#         4: 'Цікаво',
#         5: 'Потрібно подивитися'
# }

# post_rating = "Рейтинг: 627"
# for rating in post_rating.split():
#     if rating.isdigit():
#         post_rating = int(rating)
# score = 5 * (1 - math.exp(-post_rating / 300))

# print(score)

# news = {
#     'score': score_list[int(score)]
# }

# print('\n', news)
# post_body_description = soup.find('div', class_='body community-article')
# post_img_container = post_body_description.find('div', class_='post-image-container')
# post_img_tag = post_img_container.select_one('img')
# post_img_url = post_img_tag['data-lazy-src']

# post_info = soup.find('div', class_='content')
# post_raitng = post_info.select_one('.post-raitng').text
# post_title = post_info.select_one('.post-title').text

# description = '\n\n'.join(p.get_text(strip=True) for p in post_description)
# print(description)
