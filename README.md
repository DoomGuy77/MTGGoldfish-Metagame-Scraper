# MTG Goldfish Metagame Scraper

A simple web scraper using BeautifulSoup and Requests to get data from MTG Goldfish on the top decks in each format

### How to use

1. Install a recent version of [Python](https://www.python.org/downloads/)
2. Install the Beautiful Soup and Requests modules by opening command prompt and running the following commands:
```pip3 install beautifulsoup4``` and ```pip3 install requests```
3. Download ```metagameScraper.py``` and put it in a folder by itself
4. Run ```metagameScraper.py``` with the following arguments:

    ```-f``` or ```--format```: specifies which format's metagame to download. Choose an option between ```alchemy```, ```brawl```, ```commander```, ```commander_1v1```, ```historic```, ```historic_brawl```, ```legacy```, ```modern```, ```pauper```, ```penny_dreadful```, ```pioneer```, ```standard```, ```vintage```, ```all_formats```, ```MTGA_formats```. Default =```standard```
    
    ```--getDeckPopularCards```: Including this argument makes the scraper also get data on the most played cards for each deck. Note that this will significantly increase the time required to run the script.

### Reading the output

The script will output data in ```.csv``` files
General metagame data is stored at ```/Metagames/<format>-meta.csv```
Individual deck data is stored at ```/Archetypes/<format>/<archetype>.csv``` Note that```/```characters are omitted from archetype names here



### Troubleshooting
| Issue | Solution |
| ----- | -------- |
| PermissionError: [Errno 13] Permission denied | Make sure the spreadsheet (.csv) files are not open in any other program |
| UnicodeEncodeError: 'charmap' codec can't encode character '~' in position ~: character maps to <undefined> | The character encoding is not set to UTF-8 (you can set it on windows by running the command```cp 65001```in command prompt) |
| The script is taking a long time to run | This scraper is very simplistic, going through the webpages one by one. This means that running the script can take a long time. For example, it takes about 12 minutes for me to run the script scraping all formats and deck information, but your own speeds may vary depending on your connection |
