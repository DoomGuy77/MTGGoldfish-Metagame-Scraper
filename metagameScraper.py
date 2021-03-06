import string
import requests
from bs4 import BeautifulSoup
import csv
import sys
import os
import getopt

def getMeta(format):
    #Get metagame page data
    url = f'https://www.mtggoldfish.com/metagame/{format}/full#paper'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div',class_='archetype-tile-description-wrapper')
    print(f'Downloaded {format} metagame page')

    #Find the data that we care about
    archetypes = []
    metaShares = []
    for i in results:
        archetype = i.find('span', class_='deck-price-paper').find('a').text
        metaShare = i.find('div', class_='archetype-tile-statistic metagame-percentage').find('div',class_='archetype-tile-statistic-value').find(text=True).strip()
        
        #Exception for some weird characters that show up at the end of standard mono W aggro. No idea what it is or where it comes from, but it only happens to that one specific deck and no others
        #First remove the weird characters
        printable = set(string.printable)
        archetype = ''.join(filter(lambda x: x in printable, archetype))
        #Then remove the space at the end
        if archetype[len(archetype)-1] == ' ':
            tmp = list(archetype)
            tmp[-1] = ''
            archetype = ''.join(tmp)

        metaShares.append(metaShare)
        archetypes.append(archetype)
        
    #Write the data to a csv file
    file = open(f'Metagames/{format}-meta.csv', 'w', newline='', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(['Deck Archetype', 'Meta%']) #Headers Row
    for i in range(len(archetypes)):
        writer.writerow([archetypes[i],metaShares[i]])
    print(f'Parsed and stored {format} metagame data')

def getDeck(format, archetype):
    #Get deck page data
    tmpArchetype = archetype.replace(' // ','-').replace(' ','-')
    url = f'https://www.mtggoldfish.com/archetype/{format}-{tmpArchetype}-znr#paper'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='spoiler-card-container')
    print(f'Downloaded {archetype} deck data')

    #Get the specific data that we care about
    mdCards = [] #Main-deck cards
    mdQuantities = [] #Main-deck quantities
    mdPercent = [] #Main-deck inclusion percent
    sbCards = [] #Sideboard cards
    sbQuantities = [] #Sideboard quantities
    sbPercent = [] #Sideboard inclusion percent
    for i in results:
        cardTile = i.find_all('div', class_='spoiler-card')
        for j in cardTile:
            card = j.find('span', class_='price-card-invisible-label').text
            data = j.find('p', class_='archetype-breakdown-featured-card-text').text
            quantity = data[:data.find('.')+2]
            percent = data[data.find('%')-3:data.find('%')+1]
            percent = percent.replace(' ','')
            if i.find('h3').text == 'Sideboard':
                sbCards.append(card)
                sbQuantities.append(quantity)
                sbPercent.append(percent)
            else:
                mdCards.append(card)
                mdQuantities.append(quantity)
                mdPercent.append(percent)

    #Write the data to a csv file
    tmpArchetype = archetype.replace(' // ','-')
    file = open(f'Archetypes/{format}/{tmpArchetype}.csv', 'w', newline='', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(['Card Name', 'Average Quantity', 'Percent of Decks including']) #Headers Row
    writer.writerow(['MAIN DECK'])
    for i in range(len(mdCards)):
        writer.writerow([mdCards[i],mdQuantities[i],mdPercent[i]])
    writer.writerow(['SIDEBOARD'])
    for i in range(len(sbCards)):
        writer.writerow([sbCards[i],sbQuantities[i],sbPercent[i]])
    print(f'Parsed and stored {archetype} deck data')

def getDecksFromFormat(format):
    file = f'Metagames/{format}-meta.csv'
    with open(file,'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not ('Deck' in row[0]):
                getDeck(format,row[0])

def MakeDirs():
    print('Checking for /Metagames directory')
    try:
        os.mkdir('./Metagames')
        print('Created /Metagames directory')
    except FileExistsError:
        print('/Metagames directory already exists')
    
    print('Checking for /Archetypes directory')
    try:
        os.mkdir('./Archetypes')
        print('Created /Archetypes directory')
    except FileExistsError:
        print('/Archetypes directory already exists')
    
    print('Checking for deck directories')
    for i in formats:
        try:
            os.mkdir(f'./Archetypes/{i}')
            print(f'Created Archetypes/{i} directory')
        except FileExistsError:
            print(f'Archetypes/{i} directory already exists')
    

#Argument defaults
formats = ['standard']
getDeckPopularCards = False

#Handle arguments
try:
    opts, args = getopt.getopt(sys.argv[1:],'f:', ['format=','getDeckPopularCards'])
except getopt.GetoptError:
    print('metagameScraper.py -f <format> --getDeckPopularCards[optional]')
    sys.exit(0)
for opt, arg in opts:
    if opt in ('-f', '--format'):
        if arg in ('alchemy', 'brawl','commander','commander_1v1','historic','historic_brawl','legacy','modern','pauper','penny_dreadful','pioneer','standard','vintage'):
            formats = [arg]
        elif arg == 'MTGA_formats':
            formats = ['alchemy', 'brawl', 'historic', 'historic-brawl', 'standard']
        elif arg == 'all_formats':
            formats = ['alchemy', 'brawl','commander','commander_1v1','historic','historic_brawl','legacy','modern','pauper','penny_dreadful','pioneer','standard','vintage']
        else:
            print('Invalid format. Please choose from \'alchemy\', \'brawl\',\'commander\',\'commander_1v1\',\'historic\',\'historic_brawl\',\'legacy\',\'modern\',\'pauper\',\'penny_dreadful\',\'pioneer\',\'standard\',\'vintage\',\'all_formats\',\'MTGA_formats\'')
            sys.exit(0)
    elif opt == '--getDeckPopularCards':
        getDeckPopularCards = True



#Ensure correct directories exist
MakeDirs()

#Get the overall metagame info
for i in formats:
    getMeta(i)


#Get card break downs for each deck
for i in formats:
    getDecksFromFormat(i)
