'''
Benjamin Sherriff
Web Scraper
'''

# With help from https://blog.hartleybrody.com/web-scraping-cheat-sheet/

import page, args

def main():
  try:
    a = args.Arguments()
    url = a.argv.URL
    p = page.Webpage(url)
  except KeyboardInterrupt:
    print("\n[+] Exiting")
    exit()