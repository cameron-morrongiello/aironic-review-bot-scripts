import random
import asyncio
from pyppeteer import launch

MAX_PRODUCT_LINK_CHOICE_ATTEMPTS = 10


async def scrape_product(product_url=None, category=None):

    if product_url and category:
        raise ValueError("Cannot have both product_url and category set")

    if category:
        url = f'https://www.amazon.com{category}'
    else:
        url = 'https://www.amazon.com/Best-Sellers/zgbs'

    browser = await launch()
    page = await browser.newPage()

    # Set user-agent headers to mimic a web browser
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]

    # Set a random user-agent header
    user_agent = random.choice(user_agents)
    await page.setUserAgent(user_agent)

    # FIXME: Books

    # Only run if random best seller or random category product
    if not product_url:
        await page.goto(url, {'waitUntil': 'domcontentloaded'})

        # Extract the product links
        product_links = await page.querySelectorAll('a.a-link-normal')

        print(product_links)

        for _ in range(MAX_PRODUCT_LINK_CHOICE_ATTEMPTS):
            # Try to select a valid random product link
            random_link = random.choice(product_links)

            # Get the URL of the selected product
            product_url = await page.evaluate('(elem) => elem.href', random_link)

            # Rejeect review links
            if "amazon.com/product-reviews" not in product_url:
                break

        print(product_url)

        # Introduce a delay before navigating to the product page
        delay = 2  # seconds
        await asyncio.sleep(delay)

    await page.goto(product_url)

    # Extract the product title
    product_title = await page.evaluate('(elem) => elem.textContent', await page.querySelector('#productTitle'))
    product_title = product_title.strip()

    # Extract the "About this item" section
    about_section = await page.querySelector('#feature-bullets')

    # Extract the list items from the "About this item" section
    about_items = await about_section.querySelectorAll('span.a-list-item')

    # Extract the text from each list item
    about_text = [await page.evaluate('(elem) => elem.textContent', item) for item in about_items]
    about_text = '\n'.join(about_text).strip()

    await browser.close()

    return product_title, about_text, product_url


"https://www.amazon.com/Realistic-Beginners-Lifelike-Hands-Free-Stimulation/dp/B08JL9Z97C/ref=sr_1_2?crid=51BB1NFYI1F4&keywords=dildo&qid=1684447838&sprefix=dildo%2Caps%2C167&sr=8-2"
# Example usage
# # Enter your Amazon Associate ID here
# associate_id = 'reviewzillabo-20'

# # # Scrape a random product and print its title, "About this item" section, and the product URL with your Associate ID
# loop = asyncio.get_event_loop()
# random_product_title, about_product_text, product_url_with_id = loop.run_until_complete(
#     scrape_random_product(associate_id))
# print(f"Random Amazon Best-Selling Product: {random_product_title}\n")
# print(f"About this item:\n{about_product_text}")
# print(f"\nProduct URL (with Associate ID): {product_url_with_id}")
