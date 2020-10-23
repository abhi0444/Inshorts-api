"""
The following api pulls the news from Inshorts and returns it as a dictionary.
The dicitionary then can be used as per the need of the program. The functionality
is achieved by scraping the data from the website. Anyone using this API should first
obtain all the necessary permission from Inshorts before scraping the data and using
it for any commercial purpose.


Also the following API is completely dependant on the HTML structure of the website
thus any change to that will cause this API to fail (A sample for current structure
is given below thus if using this API one must make sure that the HTML structure for
the time is same on which this was dsigned).

It contains two functions:
    1. fetch_all(url, category)
    2. fetch_category(category)
"""
import time

import bs4 as BeautifulSoup
from requests.exceptions import HTTPError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)

chromeOptions = Options()
chromeOptions.headless = True
driver = webdriver.Chrome(options=chromeOptions)

# URL for Inshorts {Basically the place from where all teh news is being fetched from}
URL = "https://inshorts.com/en/read"


# A list of all valid categories
CATEGORIES = [
    "",
    "national",
    "business",
    "sports",
    "world",
    "politics",
    "technology",
    "startup",
    "entertainment",
    "miscellaneous",
    "hatke",
    "science",
    "automobile",
]


def extract_image_url(image_url_data):
    """
    Function to extract URL for images
    Any given image_url_data is of the form =
    background-image: url('URL HERE?')
    Thus the part background-image: url(' from the start and ?') from the end should be removed
    """
    return image_url_data[
        23 : len(image_url_data) - 3
    ]  # Return the final output string


def detect_read_more(bs4tag):
    """
    Not all news has read more thus it must be detected before hand to avoid errors
    For this function a bs4.tag.elemnt is passed as an argument
    It reutrns an empty string if there is no URL for readmore
    Else it return the URL for readmore
    """
    read_more_url = ""
    if bs4tag is not None:
        read_more_url = bs4tag["href"]
    return read_more_url


# Define a class or say a JSON wherein the data about the news fetched from
# the server will be filled this will be common and standardized througout the app
# Since having a class limits the working of this API thus we need to improve
# this and for that a Dictionary is better
NEWS = {"status": "", "category": "", "data": []}

# data variable is a list of dictionaries each element contains the following information
# {
#    headline: '',
#    article: '',
#    read_more: '',
#    image_url: ''
# }


def fetch_all(category="", depth=0):
    """
    This function will contain news from any and every valid url that
    has been passed to it or it will fetch the top news that made it to homepage
    The return for this function should be returning an array that contains
    all the necessary items that the news has

    1. Image URL (if any)
    2. news data (the actual news)
    3. Read more URL (if any)
    4. Headline (Not the complete data but the only the headline)
    """
    try:

        # Using selenium we do not have to specify a timeout as that
        # will be managed by selenium automatically.

        url = URL + "/" + category
        driver.get(url)

        while depth != 0:
            try:
                load_more_button = driver.find_element_by_id("load-more-btn")
                time.sleep(1.3)
                load_more_button.click()
                depth = depth - 1
            except NoSuchElementException as err:
                break
            except ElementNotInteractableException as err:
                break

        response = driver.page_source
        time.sleep(1)
        soup = BeautifulSoup.BeautifulSoup(response, "html.parser")

        # Any given news article is of the given sample form
        # <div class="">
        #    <div class="news-card z-depth-1" itemscope itemtype="">
        #        <span itemprop="description" content=""></span>
        #        <span itemprop="image" itemscope itemtype="">
        #            <meta itemprop="url" content=""></meta>
        #            <meta itemprop="width" content="864"></meta>
        #            <meta itemprop="height" content="483"></meta>
        #        </span>
        #        <span itemtype="" itemscope="itemscope" itemprop="publisher">
        #            <span itemprop="url" content=""></span>
        #            <span itemprop="name" content="Inshorts"></span>
        #            <span itemprop="logo" itemscope itemtype="">
        #            <span itemprop="url" content=""></span>
        #            <meta itemprop="width" content="400"></meta>
        #            <meta itemprop="height" content="60"></meta>
        #            </span>
        #        </span>
        #        <div class="news-card-image" style= "IMAGE HERE">
        #        </div>
        #        <div class="news-card-title news-right-box">
        #            <a class="clickable" onclick="">
        #            <span itemprop="headline">HEADLINE HERE</span>
        #            </a>
        #            <div class="news-card-author-time news-card-author-time-in-title">
        #            <a href="">
        #            <span class="short">short</span>
        #            </a> by <span class="author">AUTHOR HERE
        #            </span> /
        #            <span class="time" itemprop="datePublished" content="TIME">TIME</span> on
        #            <span clas="date">DATE HERE</span>
        #            </div>
        #        </div>
        #        <div class="news-card-content news-right-box">
        #            <div itemprop="articleBody">ARTICLE HERE</div>
        #            <div class="news-card-author-time news-card-author-time-in-content">
        #            <a href="/">
        #            <span class="short">short</span>
        #            </a> by
        #            <span class="author"></span> /
        #            <span class="time" itemprop="dateModified" content="2020-10-21T17:13:33.000Z" >
        #            10:43 pm
        #            </span> on
        #            <span class="date">
        #            21 Oct
        #            </span>
        #            </div>
        #        </div>
        #        <div class="news-card-footer news-right-box">
        #        <div class="read-more">
        #        read more at
        #        <a class="source" onclick="" href="READ MORE HERE">
        #        </a>
        #        </div>
        #        </div>
        #    </div>
        # </div>

        # From here it is evident that
        #    1. div itemprop = "articleBody" contains the data about the news
        #       that is basically the article itself.
        #    2. span itemprop = "headline" contains the data about the headline of the news.
        #    3. div class = "news-card-image" contains the data about the URL of the
        #       image associated with the news.
        #    4. a class = "source" contains the data about the source of the news.
        # Thus for the whole page we need to extract these divs and spans and then process
        # them to get the neccesary data

        # This can be done by searching for div class
        # "news-card z-depth-1" which will reutrn an
        # array containing all the news with all the associated
        # data that is image, headline and article.
        # We then iterate over this array and extract the data from
        # each element and store it

        all_news_cards = soup.find_all("div", class_="news-card z-depth-1")

        # So for any given app using this the items would keed on appending in the news dictionary
        # thus it has been cleared on every call else the dictionary would have ben getting bigger
        # and bigger and also the items displayed on top would have just been the old ones.

        news = {"status": "", "category": "", "data": []}

        for news_card in all_news_cards:
            data_item = {
                "headline": "",
                "article": "",
                "read_more": "",
                "image_url": "",
            }
            soup = BeautifulSoup.BeautifulSoup(str(news_card), "lxml")
            data_item["article"] = soup.find(itemprop="articleBody").getText()
            data_item["headline"] = soup.find(itemprop="headline").getText()
            image_url_div = soup.find(
                "div", class_="news-card-image"
            )  # Since for image we need data from the div attribute we first find the div
            data_item["image_url"] = extract_image_url(
                image_url_div["style"]
            )  # Then extract data from the attributes
            data_item["read_more"] = detect_read_more(soup.find("a", class_="source"))
            news["data"].append(data_item)

        news["category"] = category
        news["status"] = "sucess"
        return news  # Final return for the news

    except HTTPError as err:
        NEWS["status"] = err
        return NEWS


def fetch_category(category, depth=0):
    """
    This function will get the news from a specific category that the user wants to see
    This must be kept in mind that news from a category can only be
    fetched from the website if the category is actualy a valid one
    The return for this function should be returning an array that
    contains all the necessary items that the news has
    1. Image URL (if any)
    2. news data (the actual news)
    3. Read more URL (if any)
    4. Headline (Not the complete data but the only the headline)
    """
    try:
        if category not in CATEGORIES:
            raise Exception("Invalid Category")

        return fetch_all(category, depth)

    except Exception as err:
        NEWS["status"] = err
        return NEWS


print(fetch_all("business", 4))
