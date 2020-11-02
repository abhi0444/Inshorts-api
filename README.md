# News App

This is a very simple news scraper or can also be said as an API for Inshorts.


## Installation ##
 * Clone the repo using
     ```sh
    git clone https://github.com/Taru-garg/Inshorts-api
    ```
 * Open the repo and install the requirements using
 
     ```sh
     cd Inshorts-api
     pip install -r requirements.txt (or pip3 install -r requirements.txt)
     ```
         
## Running the app ##
  * Use this in case you want to run the complete app with all the frontend
    ```sh
    cd app
    python app.py (or python3 app.py)
    ```
   * Use this in case you only want to test the api
      ```sh
      cd app
      python app_api.py (or python3 app_api.py)
      ```
 
## Features of the API ##
The API has 3 features or (endpoints):
  * _**/news**_                      : This gives you the news from the homepage or the top news of the day
  * _**/news/\<category>**_          : This gives you news from the specified category given the category is valid only top 25 items
  * _**/news/\<category>/\<depth>**_ : This gives you news from the specified category upto a specific depth each increment gives 25 more items
                                (Depth starts from 0).
      * Supported categories 
          * business
          * hatke
          * national
          * sports
          * world
          * politics
          * technology
          * startup
          * entertainment
          * miscellaneous
          * science
          * automobile
