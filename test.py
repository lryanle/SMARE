from bs4 import BeautifulSoup
# from notify_run import Notify
import time
import requests
import datetime


def findFirstPost():
	source = requests.get('https://dallas.craigslist.org/search/cta').text
	soup = BeautifulSoup(source, 'lxml')
	row = soup.find('li', class_='result-row')
	firstPostName = row.p.a.text
	firstPostPrice = row.a.span.text
	badDate = row.find('time', class_='result-date')['title']
	firstPostDate = convertToDateItem(badDate)
	return firstPostDate

def convertToDateItem(badDate):
	splitDate = badDate.split(' ')
	formattedDate = (splitDate[2] + ' ' + splitDate[1] + ' ' + str(datetime.date.today().year) + ' ' + splitDate[3] + ' ' + splitDate[4])
	LastComparedItem = datetime.datetime.strptime(formattedDate, '%b %d %Y %I:%M:%S %p')
	return LastComparedItem

def findAllPost():
	# notify = Notify()
	latestDateItem = findFirstPost()
	while True:
		mostRecentItem = findFirstPost()
		source = requests.get('https://dallas.craigslist.org/search/cta').text
		soup = BeautifulSoup(source, 'lxml')
		try:
			print('Im running')
			for row in soup.find_all('li', class_='result-row'):
				badDate = row.find('time', class_='result-date')['title']
				postDate = convertToDateItem(badDate)
				postName = row.p.a.text
				postPrice = row.a.span.text
				if(postDate > latestDateItem):
					print(postName)
					# notify.send(postName)
					print('condition is true')
		except Exception as e:
			pass
		latestDateItem = mostRecentItem
		time.sleep(300)
	
def main():
	findAllPost()
	

if __name__ == "__main__":
	main()