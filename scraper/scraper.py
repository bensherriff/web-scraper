'''
Benjamin Sherriff
Web Scraper
'''

# With help from https://blog.hartleybrody.com/web-scraping-cheat-sheet/

import page, args

def main():
  try:
    a = args.Arguments()
    p = page.Webpage(a.argv)
  except KeyboardInterrupt:
    print("\n[+] Exiting")
    exit()