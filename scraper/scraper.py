'''
Benjamin Sherriff
Web Scraper
'''

import threadpool, args, settings

def main():
  try:
    a = args.Arguments()
    s = settings.Settings(a.argv.settings)
    pool = threadpool.ThreadPool(a.argv, [a.argv.URL])
    # pool.closeThreads()
  except KeyboardInterrupt:
    print("\n[+] Exiting")
    exit()