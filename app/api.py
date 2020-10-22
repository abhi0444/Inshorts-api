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
import json
import requests
import bs4 as BeautifulSoup
from requests.exceptions import HTTPError

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
    background-image: url('https://static.inshorts.com/inshorts/images/v1/variants/jpg/m/2020/10_oct/21_wed/img_1603300338355_948.jpg?')
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


# Define a class or say a JSON wherein the data about the news fetched from the server will be filled this will be common and standardized througout the app
# Since having a class limits the working of this API thus we need to improve this and for that a Dictionary is better
NEWS = {"status": "", "category": "", "data": []}

# data variable is a list of dictionaries each element contains the following information
# {
#    headline: '',
#    article: '',
#    read_more: '',
#    image_url: ''
# }


def fetch_all(some_url=URL, category=""):
    """
    This function will contain news from any and every valid url that
    has been passed to it or it will fetch the top news that made it to homepage
    The return for this function should be returning an array that contains
    all the necessary items that the news has

    1. Image URL (if any)
    2. News data (the actual news)
    3. Read more URL (if any)
    4. Headline (Not the complete data but the only the headline)
    """
    try:
        response = requests.get(some_url, timeout=5, allow_redirects=True)
        soup = BeautifulSoup.BeautifulSoup(response.text, "html.parser")

        """
        Any given news article is of the given sample form
        <div class="">
            <div class="news-card z-depth-1" itemscope itemtype="http://schema.org/NewsArticle">
                <span content="" itemscope itemprop="mainEntityOfPage" itemType="https://schema.org/WebPage" itemid="https://inshorts.com/en/news/maharashtra-govt-blocks-cbi-from-probing-cases-in-state-without-consent-1603300413288"></span>
                <span itemtype="https://schema.org/Person" itemscope="itemscope" itemprop="author">
                    <span itemprop="name" content="Nandini Sinha "></span>
                </span>
                <span itemprop="description" content="Maharashtra govt blocks CBI from probing cases in state without consent"></span>
                <span itemprop="image" itemscope itemtype="https://schema.org/ImageObject">
                    <meta itemprop="url" content="https://static.inshorts.com/inshorts/images/v1/variants/jpg/m/2020/10_oct/21_wed/img_1603299666614_411.jpg?"></meta>
                    <meta itemprop="width" content="864"></meta>
                    <meta itemprop="height" content="483"></meta>
                </span>
                <span itemtype="https://schema.org/Organization" itemscope="itemscope" itemprop="publisher">
                    <span itemprop="url" content="https://inshorts.com/"></span>
                    <span itemprop="name" content="Inshorts"></span>
                    <span itemprop="logo" itemscope itemtype="https://schema.org/ImageObject">
                    <span itemprop="url" content="https://assets.inshorts.com/inshorts/images/v1/variants/jpg/m/2018/11_nov/21_wed/img_1542823931298_497.jpg"></span>
                    <meta itemprop="width" content="400"></meta>
                    <meta itemprop="height" content="60"></meta>
                    </span>
                </span>
                <div class="news-card-image" style= "background-image: url('https://static.inshorts.com/inshorts/images/v1/variants/jpg/m/2020/10_oct/21_wed/img_1603299666614_411.jpg?')">
                </div>
                <div class="news-card-title news-right-box">
                    <a class="clickable" onclick="ga('send', {'hitType': 'event', 'eventCategory': 'TitleOfNews', 'eventAction': 'clicked', 'eventLabel': 'Maharashtra%20govt%20blocks%20CBI%20from%20probing%20cases%20in%20state%20without%20consent)' });"  style="color:#44444d!important" href="/en/news/maharashtra-govt-blocks-cbi-from-probing-cases-in-state-without-consent-1603300413288">
                    <span itemprop="headline">Maharashtra govt blocks CBI from probing cases in state without consent</span>
                    </a>
                    <div class="news-card-author-time news-card-author-time-in-title">
                    <a href="/prev/en/news/maharashtra-govt-blocks-cbi-from-probing-cases-in-state-without-consent-1603300413288"><span class="short">short</span></a> by <span class="author">Nandini Sinha </span> /
                    <span class="time" itemprop="datePublished" content="2020-10-21T17:13:33.000Z">10:43 pm</span> on <span clas="date">21 Oct 2020,Wednesday</span>
                    </div>
                </div>
                <div class="news-card-content news-right-box">
                    <div itemprop="articleBody">The Maharashtra government has withdrawn the general consent extended to CBI to probe cases in the state. CBI will now have to approach the state government for permission to carry out an investigation on a case by case basis. This comes a day after CBI registered an FIR in the TRP scam case based on a complaint filed in UP.</div>
                    <div class="news-card-author-time news-card-author-time-in-content">
                    <a href="/prev/en/news/maharashtra-govt-blocks-cbi-from-probing-cases-in-state-without-consent-1603300413288"><span class="short">short</span></a> by <span class="author">Nandini Sinha </span> /
                    <span class="time" itemprop="dateModified" content="2020-10-21T17:13:33.000Z" >10:43 pm</span> on <span class="date">21 Oct</span>
                    </div>
                </div>
                <div class="news-card-footer news-right-box">
                <div class="read-more">read more at <a class="source" onclick="ga('send', {'hitType': 'event', 'eventCategory': 'ReadMore', 'eventAction': 'clicked', 'eventLabel': 'vedantu.com' });" target="_blank" href="https://inshorts.com/safe_redirect?url=https%3A%2F%2Fvedantu.app.link%2Fg9mIAb41Kab&amp;inshorts_open_externally=true ">vedantu.com</a></div>
                </div>
            </div>
        </div>

        From here it is evident that
            1. div itemprop = "articleBody" contains the data about the news that is basically the article itself.
            2. span itemprop = "headline" contains the data about the headline of the news.
            3. div class = "news-card-image" contains the data about the URL of the image associated with the news.
            4. a class = "source" contains the data about the source of the news.
        Thus for the whole page we need to extract these divs and spans and then process them to get the neccesary data

        This can be done by searching for div class "news-card z-depth-1" which will reutrn an array containing all the news with all the associated data that is image, headline and article.
        We then iterate over this array and extract the data from each element and store it
        """

        all_news_cards = soup.find_all("div", class_="news-card z-depth-1")

        # So for any given app using this the items would keed on appending in the News dictionary
        # thus it has been cleared on every call else the dictionary would have ben getting bigger
        # and bigger and also the items displayed on top would have just been the old ones.

        News = {"status": "", "category": "", "data": []}

        for news_card in all_news_cards:
            soup = BeautifulSoup.BeautifulSoup(str(news_card), "lxml")
            article = soup.find(itemprop="articleBody").getText()
            headline = soup.find(itemprop="headline").getText()
            image_url_div = soup.find(
                "div", class_="news-card-image"
            )  # Since for image we need data from the div attribute we first find the div
            image_url = extract_image_url(
                image_url_div["style"]
            )  # Then extract data from the attributes
            read_more_url = detect_read_more(soup.find("a", class_="source"))
            data_item = {
                "headline": headline,
                "article": article,
                "read_more": read_more_url,
                "image_url": image_url,
            }
            News["category"] = category
            News["data"].append(data_item)
            News["status"] = "sucess"

        return json.dumps(News, indent=4)  # Final return for the News

    except HTTPError as err:  # Return some error in case of an error
        NEWS["status"] = err
        return json.dumps(NEWS, indent=4)


def fetch_category(category):
    """
    This function will get the news from a specific category that the user wants to see
    This must be kept in mind that news from a category can only be fetched from the website if the category is actualy a valid one
    The return for this function should be returning an array that contains all the necessary items that the news has
    1. Image URL (if any)
    2. News data (the actual news)
    3. Read more URL (if any)
    4. Headline (Not the complete data but the only the headline)
    """
    try:
        if category not in CATEGORIES:
            raise Exception("Invalid Category")

        modified_url = URL + "/" + category
        return fetch_all(modified_url, category)

    except Exception as err:
        NEWS["status"] = err
        return json.dumps(NEWS, indent=4)
