"""Web Scraper Test Project
Designed to scrape timberline lodge for season pass data (may be scaled up)
first iteration of webscraper will just test timberline"""
from bs4 import BeautifulSoup
import requests
from sys import exit
import pandas as pd
from tabulate import tabulate

base_url = "https://www.timberlinelodge.com/mountain/season-passes"

# Parses the webpage for all headers that represent types of season passes
# Calls CheckExtraHeader to exclude any unwated headers related to javascript
def GetTicketType():
    soup = BeautifulSoup(requests.get(base_url).text, 'html.parser')
    soup_header = soup.find_all('h3')
    ticket_data = CheckExtraHeader(soup_header)

    return ticket_data


# Create a dictionary for the different types of ski passes
# Return Dictionary
def SetTicketType(categories):
    TICKET_CATEGORY_MAPPING = {}
    i = 0
    for x in categories:
        TICKET_CATEGORY_MAPPING[i] = x
        i += 1

    return TICKET_CATEGORY_MAPPING


# Takes a dictionary arg that is the different season pass choices
# Return the input integer that represents the dictionary index
def PromptTicketType(tickets):
    i = 1
    for ticket in tickets:
        ticket_str = tickets[ticket].string
        ticket_str = ticket_str.replace("&nbsp", " ")
        print(str(i) + ":" + ticket_str)
        i += 1

    choice = int(input("Enter Ticket Type: "))
    curr_category = None
    # Test if the input is a choice listed i not exit the program
    try:
        curr_category = tickets[choice - 1]
    except KeyError:
        print("Wrong Choice Entered. Exiting!")
        exit(1)

    return choice


# Takes the dictionary arg and parses the table data of the page related to that dictionary
# Prints the final output which is pass price information
def GetResults(choice):
    r = requests.get(base_url)
    price_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list

    # get the ticket choice index and subtract one which starts at 1, subtract that to get list index of table
    curr_prices = price_list[choice - 1]
    print(tabulate(curr_prices, headers='keys'))


# Takes the ticket dictionary and parses out any unwanted headers related to javascript titles
# Returns clean dictionary
def CheckExtraHeader(ticket_data):
    clean_ticket_data = []
    for x in ticket_data:
        curr_tag_lower = str(x).lower()
        if curr_tag_lower.find('pass') is not -1:
            clean_ticket_data.append(x)
    return clean_ticket_data


categories = GetTicketType()
tickets = SetTicketType(categories)
choice = PromptTicketType(tickets)
GetResults(choice)
