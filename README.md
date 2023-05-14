# Visa appointments scraper

This scraper is made for checking the ais.usvisa-info.com site in time intervals. It logs you in, and scrapes the website for available appointments and sends a notification via telegram

## Setup

Clone the repo and `cd` into it with:

```sh
git clone https://github.com/vedantthapa/not-visa-scraper.git
cd not-visa-scraper
```

Create a virtual environment using a tool of your choice with `Python 3.11.3` and install the project dependencies with:

```sh
pip install -r requirements.txt
```

Download and install the relevant version of [chromedriver](https://chromedriver.chromium.org/downloads).

There is a `default.env` file that serves as a template for the actual `.env` file. The user is expected to create the `.env` file.

> Note: The `URL_ID` can be obtained from the website URL: https://ais.usvisa-info.com/en-ca/niv/schedule/\<YOUR-URL-ID\>/appointment

Since the program uses Telegram to send messages, you'll additionally need [create a bot](https://core.telegram.org/bots#how-do-i-create-a-bot) to configure the `CHAT_ID` and `TOKEN` environment variables. Here's a [tutorial](https://medium.com/codex/using-python-to-send-telegram-messages-in-3-simple-steps-419a8b5e5e2).

Run the program with:

```sh
python src/main.py
```
