from telegram import Bot, ParseMode
import requests
from bs4 import BeautifulSoup


# Telegram bot API token
TELEGRAM_TOKEN = ""

# BBC News URL to scrape
BBC_CHELSEA_NEWS_URL = r"https://www.bbc.com/sport/football/teams/chelsea"

# Initialize the Telegram bot
bot = Bot(token=TELEGRAM_TOKEN)


# Function to scrape news from BBC News
def scrape_bbc_chelsea_news():
    # Send a GET request to the BBC News website
    response = requests.get(BBC_CHELSEA_NEWS_URL)
    response.raise_for_status()

    # Parse the HTML response
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the news articles on the page
    articles = soup.find_all('article', {'class': 'ssrcss-1wieoaj-ContentPost e6wdqbx2'})

    # Extract the relevant information from each article
    news_items = []
    invalid_news_item = [None, 'Listen to the full episode here', 'Listen to Football Daily on BBC Sounds',
                         'Listen to Euro Leagues on BBC Sounds', 'Here are some more thoughts:',
                         'Want more transfer news?']

    for article in articles[:4]:
        title = article.header.span.span.string
        contents = [content.string for content in article.find_all('p') if content.string not in invalid_news_item]
        news_items.append({'title': title, 'contents': contents})
    return news_items


# Function to send news to Telegram
def send_news_to_telegram(news_items):
    for item in news_items:
        if len(item['contents']) != 0:
            i_title = item['title']
            i_content = '\n'.join(item['contents'])

            message = f"? {i_title}\n\n{i_content}\n\n@BBC News"

            try:
                with open("log.txt", "r") as file:
                    saved_titles = [line.rstrip("\n") for line in file.readlines()]

                if i_title not in saved_titles:
                    try:
                        # Save the title
                        with open("log.txt", 'a') as file:
                            file.write(i_title)
                            file.write("\n")

                        # Send the message to Telegram
                        bot.send_message(chat_id='-1001765090306', text=message, parse_mode=ParseMode.MARKDOWN)
                        print(message)

                    except UnicodeError:
                        pass

            except FileNotFoundError:
                # Incase Logfile not found
                with open("log.txt", 'a') as file:
                    file.write(i_title)
                    file.write("\n")


# Main function to run the bot
def main():
    # Scrape the news from BBC News
    news_items = scrape_bbc_chelsea_news()

    # Send the news to Telegram
    send_news_to_telegram(news_items)
