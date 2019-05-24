'''
Benjamin Sherriff
Web Scraper
'''

import page, args, settings

def main():
  try:
    a = args.Arguments()
    s = settings.Settings(a.argv.settings)
    t = page.Worker(a.argv)
    for i in t.links["external"]:
        arg = a.argv
        arg.URL = i
        arg.depth = arg.depth - 1
        page.Worker(arg)
    # threads = []
    # for i in range(a.argv.threads):
    #     t = Worker(a.argv)
    #     threads.append(t)
  except KeyboardInterrupt:
    print("\n[+] Exiting")
    exit()