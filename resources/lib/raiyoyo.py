from phate89lib import rutils
import re
import math
import urllib

class Raiyoyo(rutils.RUtils):

  USERAGENT="RaiYoYo Kodi Addon"

  def get_url_groupList(self):
    elements = []
    url = "http://www.raiyoyo.rai.it/dl/PortaliRai/Multimedia/PublishingBlock-672f7b84-fa3b-4dcb-ab87-cac436b53f33.html";
    self.log('Trying to get the video list from url ' + url, 4)
    soup = self.getSoup(url)
    container = soup.find("div", class_="boxMultimedia")
    container = container.find('div', class_='mid')
    subparts = container.find_all('div', class_='inBox')
# YO YO        
    elements.append({'title': 'YO YO', 'id': 'yoyo'})
# Vita da giungla: alla riscossa!
    elements.append({'title': 'Vita da giungla: alla riscossa!', 'id': 'vitadagiunglaallariscossa'})
# Mofy
    elements.append({'title': 'Mofy', 'id': 'mofy'})  
# Heidi 3D
    elements.append({'title': 'Heidi 3D', 'id': 'heidi3d'}) 
# Pumpkin Reports
    elements.append({'title': 'Pumpkin Reports', 'id': 'pumpkinreports'}) 
# Barbapapa'
#    elements.append({'title': 'Barbapapa\'', 'id': 'barbapap'})
# other shows
    for subpart in subparts:
      top_part = subpart.find('div', class_="top")
      mid_part = subpart.find('div', class_="mid")
      name = top_part.find('h3')
      if name and name.text.strip():
        self.log("TITLE : "+name.text.strip())
        vidcont = mid_part.find('div', class_='videoContainer')
        divid = vidcont.find('div')
        self.log("ID : "+divid['id'])
        elements.append({ 'title': name.text.strip().encode('utf-8') , 'id': divid['id']})
    return elements
    
  def get_url_punList(self,id):
    elements = []
    if (id == "yoyo") or (id == "vitadagiunglaallariscossa") or (id == "barbapap") or (id == "mofy") or (id == "heidi3d") or (id == "pumpkinreports"):
# get extra cartoon page - this show is not listed in videos section
      soup = self.getSoup("http://www.raiplay.it/programmi/"+id+"/")
      container = soup.find('div',class_="slick-row")
      episodes = container.find_all('div', class_='columns')
      for ep in episodes:
        ep_a = ep.find('a',class_='video')
        ep_url = ep_a['href'].replace('/raiplay/','http://www.raiplay.it/')
        ep_url = ep_url+"?json"
        data = self.getJson(ep_url)
        elements.append({ 'id': data["ID"], 'title': data["name"], 'url': data["video"]['contentUrl'], 'thumbs': data["images"]['landscape'], 'plot': data["description"] })
    else:          
# other shows
      url = "http://www.raiyoyo.rai.it/dl/RaiTV/programmi/json/liste/"+id+"-json-V-0.html"
      data = self.getJson(url)
      for ep in data["list"]:
        if ep["masterImage"][0] == '/':
          ep["masterImage"] = "http://www.raiyoyo.rai.it"+ep["masterImage"]
        elements.append({ 'id': ep["itemId"], 'title': ep["name"], 'url': ep["h264"], 'thumbs': ep["masterImage"], 'plot': ep["desc"] })
    return elements
