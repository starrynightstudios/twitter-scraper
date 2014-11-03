# Twitter Scraper

Scrapes Twitter for data attached to a certain hashtag or user mention.
Mentions in the tweet are saved to a database to be evaluated later.

## Installation
### MongoDB and Databases
1. Install MongoDB, [http://docs.mongodb.org/manual/installation/](http://docs.mongodb.org/manual/installation/)
2. Create `dev_tweets` and `tweets` databases and users
  * `mongo`
  * `use dev_tweets`
  * ```
    db.createUser(
                  {
                    user: 'twitterScraper', 
                    pwd: 'twitterScraper', 
                    roles: [ "readWrite", "dbAdmin" ]
                  }
                )
    ```
  * `use tweets`
  * ```
    db.createUser(
                  {
                    user: 'twitterScraper', 
                    pwd: 'twitterScraper', 
                    roles: [ "readWrite", "dbAdmin" ]
                  }
                )
    ```
### Project Setup
1. Clone project to your machine
2. Create a virtualenv for twitter-scraper
3. Start that virtualenv
2. `pip install -r requirements.txt`
3. Edit `twitter-scraper.py`
  1. Enter your Twitter Application Keys, [https://apps.twitter.com](https://apps.twitter.com)
  2. Enter what you would like to be watching for on Twitter
  3. Verify MongoDB users and database address
  4. Save
4. Run `python twitter-scraper.py`
  * For developer mode, to save to dev_tweets, run with `-d true`
  * For verbose output to console run with `-v true`

## Developing
Clone the repository and open a pull request to be merged back in.