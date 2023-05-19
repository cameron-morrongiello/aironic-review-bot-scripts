import asyncio
import random
import argparse
import sys

from scrape_bestseller import scrape_product
from generate_review import generate_sarcastic_review
from send_twitter import post_tweet_thread
from submitted_links import use_random_product_link

CATEGORIES = {'Amazon Devices & Accessories': '/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices', 'Amazon Renewed': '/Best-Sellers-Amazon-Renewed/zgbs/amazon-renewed', 'Appliances': '/Best-Sellers-Appliances/zgbs/appliances', 'Apps & Games': '/Best-Sellers-Apps-Games/zgbs/mobile-apps', 'Arts, Crafts & Sewing': '/Best-Sellers-Arts-Crafts-Sewing/zgbs/arts-crafts', 'Audible Books & Originals': '/Best-Sellers-Audible-Books-Originals/zgbs/audible', 'Automotive': '/Best-Sellers-Automotive/zgbs/automotive', 'Baby': '/Best-Sellers-Baby/zgbs/baby-products', 'Beauty & Personal Care': '/Best-Sellers-Beauty-Personal-Care/zgbs/beauty', 'Books': '/best-sellers-books-Amazon/zgbs/books', 'Camera & Photo Products': '/best-sellers-camera-photo/zgbs/photo', 'CDs & Vinyl': '/best-sellers-music-albums/zgbs/music', 'Cell Phones & Accessories': '/Best-Sellers-Cell-Phones-Accessories/zgbs/wireless', 'Climate Pledge Friendly': '/Best-Sellers-Climate-Pledge-Friendly/zgbs/climate-pledge', 'Clothing, Shoes & Jewelry': '/Best-Sellers-Clothing-Shoes-Jewelry/zgbs/fashion', 'Collectible Coins': '/Best-Sellers-Collectible-Coins/zgbs/coins', 'Computers & Accessories': '/Best-Sellers-Computers-Accessories/zgbs/pc', 'Digital Educational Resources': '/Best-Sellers-Digital-Educational-Resources/zgbs/digital-educational-resources', 'Digital Music': '/Best-Sellers-Digital-Music/zgbs/dmusic', 'Electronics': '/Best-Sellers-Electronics/zgbs/electronics', 'Entertainment Collectibles': '/Best-Sellers-Entertainment-Collectibles/zgbs/entertainment-collectibles',
              'Gift Cards': '/Best-Sellers-Gift-Cards/zgbs/gift-cards', 'Grocery & Gourmet Food': '/Best-Sellers-Grocery-Gourmet-Food/zgbs/grocery', 'Handmade Products': '/Best-Sellers-Handmade-Products/zgbs/handmade', 'Health & Household': '/Best-Sellers-Health-Household/zgbs/hpc', 'Home & Kitchen': '/Best-Sellers-Home-Kitchen/zgbs/home-garden', 'Industrial & Scientific': '/Best-Sellers-Industrial-Scientific/zgbs/industrial', 'Kindle Store': '/Best-Sellers-Kindle-Store/zgbs/digital-text', 'Kitchen & Dining': '/Best-Sellers-Kitchen-Dining/zgbs/kitchen', 'Magazine Subscriptions': '/Best-Sellers-Magazine-Subscriptions/zgbs/magazines', 'Movies & TV': '/best-sellers-movies-TV-DVD-Blu-ray/zgbs/movies-tv', 'Musical Instruments': '/Best-Sellers-Musical-Instruments/zgbs/musical-instruments', 'Office Products': '/Best-Sellers-Office-Products/zgbs/office-products', 'Patio, Lawn & Garden': '/Best-Sellers-Patio-Lawn-Garden/zgbs/lawn-garden', 'Pet Supplies': '/Best-Sellers-Pet-Supplies/zgbs/pet-supplies', 'Software': '/best-sellers-software/zgbs/software', 'Sports & Outdoors': '/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods', 'Sports Collectibles': '/Best-Sellers-Sports-Collectibles/zgbs/sports-collectibles', 'Tools & Home Improvement': '/Best-Sellers-Tools-Home-Improvement/zgbs/hi', 'Toys & Games': '/Best-Sellers-Toys-Games/zgbs/toys-and-games', 'Unique Finds': '/Best-Sellers-Unique-Finds/zgbs/boost', 'Video Games': '/best-sellers-video-games/zgbs/videogames'}


def __auto_scrape():
    # Create loop
    loop = asyncio.get_event_loop()

    # Attempt to get a user submitted link
    product_link = use_random_product_link()

    if product_link:
        return loop.run_until_complete(scrape_product(product_url=product_link))

    category_name = random.choice(list(CATEGORIES))
    category_link = CATEGORIES[category_name]
    return loop.run_until_complete(scrape_product(category=category_link))


def __manual_scrape(args):
    # Create loop
    loop = asyncio.get_event_loop()

    if args.product_link or args.pick_random_user:
        # Product link option selected

        if args.pick_random_user:
            product_link = use_random_product_link()
        else:
            product_link = args.product_link

        print(f"Product link option selected: {product_link}")
        return loop.run_until_complete(scrape_product(product_url=product_link))
    else:
        # No valid option selected, default to random

        if args.category:
            # if category is specified
            category_name = args.category
            print(f"Category option selected: {category_name}")
            try:
                category_link = CATEGORIES[category_name]
            except KeyError:
                raise ValueError("Invalid category name.")
        else:
            # if completely random
            print("Random option selected")
            category_name = random.choice(list(CATEGORIES))
            category_link = CATEGORIES[category_name]

        print("Cateogry Name: ", category_name)
        print("Cateogry Link: ", category_link)
        return loop.run_until_complete(scrape_product(category=category_link))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", action="store_true",
                        help="Choose a random user selection, if none, a random option")
    parser.add_argument("--random", action="store_true",
                        help="Choose a random option")
    parser.add_argument("--pick_random_user", action="store_true",
                        help="Choose a random option")
    parser.add_argument("--category", type=str,
                        metavar="<category_name>", help="Specify a category")
    parser.add_argument("--product_link", type=str,
                        metavar="<product_link>", help="Specify a product link")

    args, unknown_args = parser.parse_known_args()

    if len(unknown_args) > 0:
        # Unknown arguments detected, raise an error
        unknown_args_str = " ".join(unknown_args)
        raise ValueError(f"Invalid argument(s): {unknown_args_str}")

    if args.auto:
        # Try a user pick and then defualt to a random product
        random_product_title, about_product_text, product_url = __auto_scrape()
    else:
        # Scrape the correct thing based on args passed in
        random_product_title, about_product_text, product_url = __manual_scrape(
            args)

    print("Product Title: ", random_product_title)
    print("Product About: ", about_product_text)
    print("Associate Link: ", product_url)

    # Gernerate review
    review = generate_sarcastic_review(
        random_product_title,
        about_product_text
    )

    print("AI Review: ", review)

    # Amazon Associate ID
    associate_id = 'reviewzillabo-20'
    # Append the Associate ID to the product URL
    product_url_with_id = f"{product_url}?tag={associate_id}"

    # Post Tweet thread
    post_tweet_thread(review, product_url)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
