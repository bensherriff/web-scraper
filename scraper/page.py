import requests, csv, settings
from bs4 import BeautifulSoup

class Webpage(object):
  def __init__(self, site):
    self.site = site
    self.request = ""
    self.file = ""
    self.status_code = 0
    self.pageStart()

  '''
  pageRequest()
  Description: Takes self.site and checks if it is a valid url. If it is not a valid url,
    it will attempt to make it valid before sending a requests.get(). If requests.get()
    is valid, it is stored in requests and returned. If requests.get() is not valid,
    request is set to -1 and returned.
  Arguments: None
  Return: Request
  '''
  def pageRequest(self):
    scheme = ["http", "https"]
    domains = [".com", ".org", ".net", ".int", ".edu", ".gov", ".mil"]
    
    try:
      # Check if site includes scheme (http:// or https://)
      prefix = self.site.partition("://")
      if not prefix in scheme:
        self.site = "http://" + self.site
        print("[+] Missing scheme, fixing format...\n    URL:", self.site)
      
      request = requests.get(self.site, params=dict(
          query="web scraping",
          page=2
      ))
      self.status_code = request.status_code
      if self.status_code != 200:
        print("[Error] Status: %d" % self.status_code)
    except:
      print("[Error] Invalid URL: %s" % self.site)
      request = -1

    return request

  '''
  pageParse()
  Description:
  Arguments:
  Return: Data
  '''
  def pageParse(self, tag=None):
    soup = BeautifulSoup(self.request.text, "html.parser")
    data = []

    links = soup.find_all("a", href=True)
    divs = soup.find_all("div")
    data.append("Links: " + str(len(links)))
    for i in links:
      link = (i["href"])
      data.append(link)
    return data

  '''
  pageWrite()
  Description:
  Arguments:
  Return:
  '''
  def pageWrite(self, file, data):
    file = file["csv"]
    with open(file, "w") as f:
      writer = csv.writer(f)
      writer.writerow(data)
    print("[+] Data written to", file)

  '''
  pageStart()
  Description:
  Arguments:
  Return:
  '''
  def pageStart(self):
    s = settings.Settings()

    self.request = self.pageRequest()
    if (self.request == -1):
      return

    data = self.pageParse()

    if s.file["save"] == True:
      self.pageWrite(s.file, data)


    # while True:
    #   # If searching for a specific tag
    #   choice = input("[Input] Search for specific tag? [Y]/[N]: ")
    #   if choice.lower() == "y":
    #     tag = input("[Input] Tag: ")
    #     data.append(self.pageParse(tag))
    #   # If collecting generic data
    #   else:
    #     data.append(self.pageParse())

    #   # If collecting more data
    #   choice = input("[Input] Continue search? [Y]/[N]: ")
    #   if choice.lower() == "y":
    #     continue
    #   # If done collecting data
    #   else:
    #     if choice.lower() == "y":
    #       choice = input("[Input] Store data? [Y]/[N]: ")         
    #       break

    #   self.pageWrite(data)