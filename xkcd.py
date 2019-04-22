from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve,urlopen 
from tqdm import tqdm
import re
import threading
from queue import Queue

queue = Queue()
base = "https://xkcd.com"


####### add the comic links and names to a queue ######
def queue_links():
	url = "https://xkcd.com/archive/"
	page = requests.get(url)
	soup = BeautifulSoup(page.content.decode(),"html.parser")
	links = soup.find("div", id="middleContainer").find_all("a")   # link and comic name 

	### 500 latest comics ###
	for i in range(500):
		queue.put((links[i]["href"], links[i].text))
	queue.join()



####### func to download the comic img from page ######
def get_comic():
	while True:
		conts = queue.get()
		url = conts[0]
		name = conts[1]
		try:
			image_base = "https://imgs.xkcd.com/comics/"
			page = requests.get((base+url),headers={'Connection':'close'}).content
			img = re.search(rb'src="//imgs.xkcd.com/comics/(.*?)"',page)
			urlretrieve(image_base+img.group(1).decode(), 'xkcd/'+name+'.png')
		except Exception as e:
			#print(str(e))   #Debugging
			continue
		queue.task_done()


for _ in range(10):
    t = threading.Thread(target=get_comic)
    t.daemon = True
    t.start()

queue_links()