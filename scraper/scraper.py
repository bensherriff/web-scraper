'''
Benjamin Sherriff
Web Scraper
'''

# With help from https://blog.hartleybrody.com/web-scraping-cheat-sheet/

import page, args, settings

def main():
  try:
    a = args.Arguments()
    s = settings.Settings(a.argv.settings)
    p = page.Webpage(a.argv)
  except KeyboardInterrupt:
    print("\n[+] Exiting")
    exit()