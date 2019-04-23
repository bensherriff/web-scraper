'''
Benjamin Sherriff
Web Scraper
'''

# With help from https://blog.hartleybrody.com/web-scraping-cheat-sheet/

import requests
from bs4 import BeautifulSoup
import csv

class Page(object):
  def __init__(self, site):
    self.site = site
    self.request = ""
    self.status_code = 0
    self.start()

  def pageRequest(self):
    scheme = "http", "https"
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

  def pageParse(self, tag=None):
    soup = BeautifulSoup(self.request.text, "html.parser")
    data = []

    # If collecting generic data
    if tag == None:
      links = soup.find_all("a", href=True)
      divs = soup.find_all("div")
      data.append("Links: " + str(len(links)))
      for i in links:
        data.append(i["href"])
    # If searching for a specific tag
    else:
      data.append("Tag: " + tag)
      info = soup.find_all(tag)
      for i in info:
        data.append(i)
    return data

  def start(self):
    data = []

    self.request = self.pageRequest()
    if (self.request == -1):
      return

    while True:
      # If searching for a specific tag
      choice = input("[Input] Search for specific tag? [Y]/[N]: ")
      if choice.lower() == "y":
        tag = input("[Input] Tag: ")
        data.append(self.pageParse(tag))
      # If collecting generic data
      else:
        data.append(self.pageParse())

      # If collecting more data
      choice = input("[Input] Continue search? [Y]/[N]: ")
      if choice.lower() == "y":
        continue
      # If done collecting data
      else:
        choice = input("[Input] Store data? [Y]/[N]: ")
        if choice.lower() == "y":
          file = input("[Input] File Name: ")
          if file[-4] != ".csv":
            file = file + ".csv"
          with open(file, "w") as f:
            writer = csv.writer(f)
            for i in data:
              writer.writerow(i)
        print("[+] Data written to", file)
        break

def main():
  try:
    while True:
      site = input("[Input] Enter URL or exit: ")
      if (site.lower() == "exit"):
        print("[+] Exiting")
        exit()
      else:
        page = Page(site)
  except KeyboardInterrupt:
    print("\n[+] Exiting")
    exit()


if __name__ == '__main__':
    main()