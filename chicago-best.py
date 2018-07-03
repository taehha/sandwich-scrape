from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
from time import sleep

base_url = ("http://www.chicagomag.com/Chicago-Magazine/"
            "November-2012/Best-Sandwiches-Chicago/")
						
domainname = 'http://www.chicagomag.com'

def make_soup(url):
	html = urlopen(url).read()
	return BeautifulSoup(html, "lxml")

#Returns list of sandwich winner urls
def get_sammy_urls(sammy_link):
	soup = make_soup(sammy_link)
	sammies = soup.findAll('div', 'sammy')
	sammy_urls = [div.a['href'] for div in sammies]
	return sammy_urls

#Writes to tsv file different info for each sandwich
def write_sammy_descr(url):
    #Some urls contain domain name, some do not
    if url.find(domainname) == -1:
        url = 'http://www.chicagomag.com'+url
    soup = make_soup(url)
		
    rankAndTitle = [h1.string for h1 in soup.findAll('h1', 'headline')][0].split('.')
    #Title does not always include both rank and title
    if len(rankAndTitle) == 1:
        rank = rankcounter
        sandwichrestaurant = rankAndTitle[0].split(':')[1]
    else:
        rank = int(rankAndTitle[0])
        sandwichrestaurant = rankAndTitle[1]
    rankcounter = rankcounter + 1
		
    description2 = str([p.em for p in soup.findAll('p', 'addy')]).split('>', 1)[1]
    #Separating the price with rest of the second portion of the description.
    #Some prices have whole numbers ie. $5, some have decimals ie $5.50, below if statement checks and splits accordingly
    if len(description2.split('.')[1]) < 3:
        price = '.'.join(description2.split('.',2)[:2])
        addressandnumber = description2.split('.',2)[2].split(',')
    else:
        description2 = description2.split('.',1)
        price = description2[0]
        addressandnumber = description2[1].split(',')
    address = addressandnumber[0]
    if addressandnumber[0] == ' Multiple locations':
        phonenumber = ''
    else:
        phonenumber = addressandnumber[1]
    #Not all restaurants have a website
    if soup.find('p', 'addy').em.a:
        websiteurl = [p.a['href'] for p in soup.findAll('p', 'addy')][0]
    else:
        websiteurl = ''
    output.writerow([rank, sandwichrestaurant, price, address, phonenumber, websiteurl])
		
if __name__ == '__main__':
	sammy_urls = get_sammy_urls(base_url)
		
	with open('data-src-best-sandwiches.tsv', 'w+') as f:
		fieldnames = ('Rank', 'Sandwich+Restaurant', 'Price', 'Address', 'PhoneNumber', 'WebsiteUrl')
		output = csv.writer(f, delimiter = '\t')
		output.writerow(fieldnames)
		rankcounter = 1
		
		for url in sammy_urls:
			write_sammy_descr(url)
			sleep(1)
	print('Done writing file.')
