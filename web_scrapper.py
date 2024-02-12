import requests
from bs4 import BeautifulSoup
import re
def scrape_website(url, keywords_file, extensions_file):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ""
        for element in soup.find_all(['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text += element.get_text() + " "
        with open(keywords_file.strip(), 'r') as f:
            keywords = [keyword.strip() for keyword in f.readlines()]
        with open(extensions_file.strip(), 'r') as f:
            file_extensions = [extension.strip() for extension in f.readlines()]
        keyword_locations = {}
        for keyword in keywords:
            keyword_locations[keyword] = [(match.start(), match.end(), text[max(match.start() - 50, 0):min(match.end() + 50, len(text))]) for match in re.finditer(keyword, text)]
        extension_locations = {}
        for extension in file_extensions:
            extension_locations[extension] = [(match.start(), match.end()) for match in re.finditer(r'\.' + re.escape(extension), text)]
        print("All data from the webpage:\n", text)
        print("\nKeyword locations:")
        for keyword, locations in keyword_locations.items():
            if locations:
                print("Keyword '{}' found at the following locations:".format(keyword))
                for location in locations:
                    print("Start: {}, End: {}, Text: {}".format(location[0], location[1], location[2]))
            else:
                print("Keyword '{}' not found in the data.".format(keyword))
        print("\nFile extension locations:")
        for extension, locations in extension_locations.items():
            if locations:
                print("Extension '{}' found at the following locations:".format(extension))
                for location in locations:
                    print("Start: {}, End: {}".format(location[0], location[1]))
            else:
                print("Extension '{}' not found in the data.".format(extension))
    else:
        print("Failed to retrieve webpage")
url = input("Enter the URL of the webpage you want to scrape: ")
keywords_file = input("Enter the path to the file containing keywords: ")
extensions_file = input("Enter the path to the file containing file extensions: ")
scrape_website(url, keywords_file, extensions_file)
