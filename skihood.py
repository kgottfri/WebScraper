"""Web Scraper Test Project
Designed to scrape timberline lodge for season pass data (may be scaled up)
first iteration of webscraper will just test skihood"""
from bs4 import BeautifulSoup
import requests
from sys import exit
from tabulate import tabulate

base_url = "https://www.timberlinelodge.com/mountain/lift-tickets"
base_data = ["Age, Time, Price"]
#define global str for age category to search
CHOICE_CATEGORY_MAPPING = {}

def get_Results():
    # Utilize a get request to gather HTML text from webpage and save as BeautifulSoup object
    soup = BeautifulSoup(requests.get(base_url).text, 'html.parser')
    prices = soup.find_all('td')
    return prices


def set_Category(prices, CHOICES):
    i = 0
    for x in range(0, len(prices)//3):
        if x == 0:
            CHOICES[x + 1] = prices[i].string
            i +=3
        elif x <= len(prices) -1:
            CHOICES[x +1] = prices[i].string
            i += 3
    return CHOICES


def prompt_Category(category):
    choice = prices
    print("Choose your ticket age:")
    for x in range(0, len(choice)):
        print(str(x) + ": " + str(choice[x]))


def get_Age():
    choice = int(input("Enter Choice: "))
    curr_category = None
    try:
        curr_category = CHOICE_CATEGORY_MAPPING[choice]
    except KeyError:
        print("Wrong Choice Entered. Exiting!")
        exit(1)
    return curr_category


def get_Price(price, category):
    curr_category = category
    for i in range(0, len(price)):
        curr_age = price[i]
        if curr_category in curr_age:
            if i+2 <= len(price):
                curr_time = price[i+1]
                curr_price = price[i+2]
                return curr_age.string, curr_time.string, curr_price.string
            else:
                print("Price not available... exiting")
                exit(1)
        else:
            i+=1
    return print("Couldn't parse HTML... exiting"), exit(1)


prices = get_Results()
category = set_Category(prices, CHOICE_CATEGORY_MAPPING)
# prompt_Category(category)

category = get_Age()
price = get_Price(prices, category)
print("\n", tabulate([[price[0], price[1], price[2]]], headers=['Age', 'Time', 'Price']))


