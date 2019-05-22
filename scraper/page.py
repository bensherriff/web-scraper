import requests, settings
from bs4 import BeautifulSoup

class Webpage(object):
  def __init__(self, argv):
    self.site = argv.URL
    self.depth = argv.depth
    self.request = ""
    self.status_code = 0
    self.links = {
      "internal": [],
      "external": [],
      "mail": []
    }
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
    
    # Check if site includes scheme (http:// or https://)
    for substring in scheme:
      if substring in self.site:
        preFix = True
        break

    # Check if site includes domain (.com, .org, etc)
    for substring in domains:
      if substring in self.site:
        postFix = True
        break
    try:

      # If scheme is missing, try adding http
      if preFix == False:
        print("[Error] Invalid URL: %s" % self.site)
        print("        Missing Scheme: http:// or https://")
        self.site = "http://" + self.site
        print("        Adding Scheme: %s" % self.site)

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
      data[0].append(i)

    links = soup.find_all("a", href=True)
    for i in links:
      d = i["href"]
      if d == "#" or d == "/" or d == "":
        continue
      if d[0:1] == "#" or d[0:1] == "/":
        self.links["internal"].append(d)
      elif d[0:6] == "mailto":
        self.links["mail"].append(d[7:])
      else:
        self.links["external"].append(d)
    return data

  '''
  pageWrite()
  Description:
  Arguments:
  Return:
  '''
  def pageWrite(self, configuration, data):
    fileName = configuration["csv"]
    with open(fileName, "w") as f:

      f.write("URL: " + self.site + "\n")
      f.write("TOTAL LINKS (" + str(sum(map(len, self.links.values()))) + ")\n")

      if len(self.links["internal"]) > 0:
        f.write("INTERNAL LINKS (" + str(len(self.links["internal"])) + ")\n")
        for i in self.links["internal"]:
          f.write(str(i))
          if i is not self.links["internal"][-1]:
            f.write(",")

      if len(self.links["external"]) > 0:
        f.write("\nEXTERNAL LINKS (" + str(len(self.links["external"])) + ")\n")
        for i in self.links["external"]:
          f.write(str(i))
          if i is not self.links["external"][-1]:
            f.write(",")

      if len(self.links["mail"]) > 0:
        f.write("\nMAIL LINKS (" + str(len(self.links["mail"])) + ")\n")
        for i in self.links["mail"]:
          f.write(str(i))
          if i is not self.links["mail"][-1]:
            f.write(",")

    print("[+] Data written to", fileName)

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

    if s.config["save"] == True:
      self.pageWrite(s.config, data)
    else:
      return


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