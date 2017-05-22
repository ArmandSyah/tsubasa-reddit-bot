<div><img src="Images/tsubasa-smug.jpg"</img></div>

# Tsubasa Reddit Bot

My little pet project, Tsubasa, is a Work-In-Progress Reddit Bot designed to look up info on an anime (names, source,
synopsis, ect.) for you and display it through a neat and tidy reddit message. So far, all the modules related to scrapping
info have been completed and the next step is to make the reddit interface to interact with the user.

### Update 5/22/2017

I have completed the reddit functionality to this bot, and when it's running, you can actually search and obtain results
on anime info. In the future, to search for an anime, PM [this user](https://www.reddit.com/user/KieranBot) as such, 
typing this in the body:

> \>*Name of anime*

You can put anything in the subject heading of the message. The more precise the title you search, the better the 
result.

## Requirements

* Python 3.6
* BeautifulSoup4
* Requests
* PRAW 
* Spice API

### Big TODOS

* ~~Finish Scrapping Anime Info and websites~~
* ~~Add Reddit Interface~~
* Create SQLite or (PostgreSQL) DB to reduce page requests
* Figure out a way leave script running persistenly
* Find a way to keep search results consistent

### Thats all for now, I'll keep working on this and hopefully it'll be great!