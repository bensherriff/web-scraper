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
    preFix = False
    postFix = False
    
    try:
      # Check if site includes scheme (http:// or https://)
      for substring in scheme:
        if substring in self.site:
          preFix = True
          break

      # If scheme is missing, try adding http
      if preFix == False:
        print("[Error] Invalid URL: %s - Missing Scheme" % self.site)
        self.site = "http://" + self.site
        print("        Adding Scheme: %s" % self.site)

      # Check if site includes domain (.com, .org, etc)
      for substring in domains:
        if substring in self.site:
          postFix = True
          break

      # If domain is missing, show error and return
      if postFix == False:
        print("[Error] Invalid URL: %s - Missing Domain" % self.site)
        return -1
        
      # If domain is valid, continue with request
      else:
        request = requests.get(self.site, params=dict(
            query="web scraping",
            page=2
        ))
        self.status_code = request.status_code
        if self.status_code != 200:
          print("[Error] Status: %d" % self.status_code)
    except Exception as e:
      print("[Error] URL: %s\n        %s" % (self.site, e))
      return -1

    return request

  '''
  pageParse()
  Description:
  Arguments:
  Return: Data
  '''
  def pageParse(self, tag=None):
    soup = BeautifulSoup(self.request.text, "html.parser")
    data = [[],[]]
    
    divs = soup.find_all("div")
    data[0] = []
    for i in divs:
      data[0].append([i])

    links = soup.find_all("a", href=True)
    for i in links:
      d = i["href"]
      data[1].append([d])
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
      w = csv.writer(f)
      
      w.writerow(["DIVS (" + str(len(data[0])) + ")"])
      for i in data[0]:
        w.writerow(i)
      w.writerow(["LINKS (" + str(len(data[1])) + ")"])
      # w.writerow(data[1])
      for i in data[1]:
        w.writerow(i)
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