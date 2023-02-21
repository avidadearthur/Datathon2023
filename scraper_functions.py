import requests
from ipywidgets import IntProgress
from IPython.display import display
from bs4 import BeautifulSoup
import re

# Define a function that takes a list of artist names as input and returns a list of Wikipedia links
def get_wikipedia_links(artists):
    max_count = len(artists)

    f = IntProgress(min=0, max=max_count)  # instantiate the bar
    display(f)  # display the bar

    wikipedia_links = {}
    artists_not_found = []
    for artist in artists:
        f.value += 1
        # Use the Wikipedia API to search for the page title of the artist
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={artist}&format=json"
        search_result = requests.get(search_url).json()

        # Check if the search result is empty
        if len(search_result["query"]["search"]) == 0:
            artists_not_found.append(artist)
            continue

        # Use the page title to get the page ID of the artist's Wikipedia page
        page_title = search_result["query"]["search"][0]["title"]
        page_id_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={page_title}&prop=info&format=json"
        page_id_result = requests.get(page_id_url).json()
        page_id = list(page_id_result["query"]["pages"].keys())[0]

        # Use the page ID to generate the link to the artist's Wikipedia page
        wikipedia_link = f"https://en.wikipedia.org/wiki?curid={page_id}"
        wikipedia_links[artist] = wikipedia_link

    return wikipedia_links, artists_not_found

def get_dates_from_wikipedia(links):
    max_count = len(links)

    f = IntProgress(min=0, max=max_count)  # instantiate the bar
    display(f)  # display the bar

    result_dict = {}

    for artist in links:
        f.value += 1

        name = artist
        url = links[artist]

        # Retrieve the HTML from the Wikipedia page
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the birth and death dates
        birth_year = None
        death_year = None

        # Find the span element with class "bday" for the birth date
        birth_date = soup.find("span", {"class": "bday"})
        if birth_date is not None:
            birth_year = int(birth_date.text.split("-")[0])

        # Find the td element in the th element with "Born" in the text for the birth date
        born_th = soup.find("th", text=re.compile(r"Born"), attrs={"scope": "row"})
        if born_th is not None:
            birth_td = born_th.find_next_sibling("td")
            birth_date_text = birth_td.text.strip()
            match = re.search(r"\d{4}", birth_date_text)
            if match is not None:
                birth_year = int(match.group())

        # Find the span element with class "dday" for the death date
        death_date = soup.find("span", {"class": "dday"})
        if death_date is not None:
            death_year = int(death_date.text.split("-")[0])

        # Find the td element in the th element with "Died" in the text for the death date
        died_th = soup.find("th", text=re.compile(r"Died"), attrs={"scope": "row"})
        if died_th is not None:
            died_td = died_th.find_next_sibling("td")
            death_date_text = died_td.text.strip()
            match = re.search(r"\d{4}", death_date_text)
            if match is not None:
                death_year = int(match.group())

        # Add the artist's info to the result dictionary
        result_dict[name] = {"birth_year": birth_year, "death_year": death_year}

    return result_dict

