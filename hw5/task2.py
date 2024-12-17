import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch_page(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()
        else:
            print(f"Error fetching {url}: Status code {response.status}")
            return None

async def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')

    ads = soup.find_all('div', class_='some-ad-class')
    for ad in ads:
        try:
            title = ad.find('h2', class_='some-title-class').text.strip()
            price = ad.find('span', class_='some-price-class').text.strip()

            yield {
                'title': title,
                'price': price,
            }
        except AttributeError:
            print("Warning: Could not parse ad data.")


async def scrape_cian(url, limit=10):
    ads = []
    async with aiohttp.ClientSession() as session:
        html = await fetch_page(session, url)
        if html:
            ad_count = 0
            async for ad_data in parse_page(html):
                ads.append(ad_data)
                ad_count += 1
                if ad_count >= limit:
                    break

    return ads

async def main():
    url = "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&region=1"
    scraped_ads = await scrape_cian(url, limit=50)

    import json
    with open('artifacts/task2/cian_ads.json', 'w', encoding='utf-8') as f:
        json.dump(scraped_ads, f, ensure_ascii=False, indent=4)

    print(f"Scraped {len(scraped_ads)} ads.")

if __name__ == "__main__":
    asyncio.run(main())
