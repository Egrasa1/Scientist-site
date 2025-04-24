import requests
import math
import random
import logging

from requests.exceptions import RequestException, HTTPError
from bs4 import BeautifulSoup

def parser_science_news():
    logger = logging.getLogger(__name__)
    logger.info("Парсенг сайту почався")
    category = ['astronomy', 'cosmonautics', 'physics', 'chemistry', 'medicine', 'biology']
    category_for_news = random.choice(category)
    
    base_url = "https://naked-science.ru/article"
    try:
        logger.info(f"Категорія для парсингу: {category_for_news}")
        res = requests.get(f"{base_url}/{category_for_news}", timeout=10)
        res.raise_for_status()
    except HTTPError as error:
        logger.error(f'Виникла помилка при спробі відправити request: {error}')
        return []
    except RequestException as error:
        logger.error(f"Запит не вдався: {error}")
        return []
    except Exception as error:
        logger.exception(f"Неочікувана помилка під час запиту: {error}")
        return []
    
    try:
        soup = BeautifulSoup(res.text, "html.parser")
        articles = soup.select(".news-item-title")
        hrefs = [a.find("a")["href"] for a in articles if a.find("a")]
       
        if not hrefs:
            logger.warning('Ссилкі на новини не було отриманно')
    except Exception as error:
        logger.exception(f"Неочікувана помилка під час запиту: {error}")
        return []

    score_list = {
        1: "Не цікаво",
        2: "Таке",
        3: "Середнє",
        4: "Цікаво",
        5: "Потрібно подивитися",
    }
    news = []
    for href in hrefs:
        if not href:
            continue
        
        try:
            logger.debug(f"Процес обробки новини: {href}")
            try:
                res = requests.get(href, timeout=10)
                res.raise_for_status()
            except HTTPError as error:
                logger.error(f'Виникла помилка при спробі відправити request: {error}')
                return []
            except RequestException as error:
                logger.error(f"Запит не вдався: {error}")
                return []    
                    
            soup = BeautifulSoup(res.text, "html.parser")
            post_info = soup.find("div", class_="content")
            if not post_info:
                logging.error(f"Не вдалося получити інформацію про статью: {href}")
                break
                
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
                logger.debug(f"Відсортировка новин за рейтингов: {rating_score}")
                
                post_body_description = soup.find("div", class_="body")
                post_title_inf = post_info.select_one(".post-title")
                post_title = post_title_inf.find('h1')
                post_lead = post_info.select_one(".post-lead")
                
                paragraphs = post_body_description.find_all("p") if post_body_description else []
                description = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

                post_img_url = None
                try:
                    img_container = soup.find("div", class_="post-image-container")
                    if img_container:
                        a_tag = img_container.select_one("a")
                        post_img_url = a_tag.get("href")
                except Exception as error:
                    logger.warning(f"Помилка при спробі получити картинку з {href}: {error}")

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
                logger.debug(f"Успішно оброблена стаття: {href}")
        except Exception as ex:
            logger.exception(f"Помилка під час обробки {href}: {ex}")
            continue
    logger.info(f"Парсінг завершено. Знайдено {len(news)} статей")
    return news