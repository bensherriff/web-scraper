import argparse, settings

class Arguments(object):
  def __init__(self):
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="Configure scraper for given url")
    parser.add_argument("-d", "--depth", dest="depth", help="How many links to enter and parse", default=1, type=int)
    parser.add_argument("-s", "--settings", help="Configure scraper", action="store_true", default=False)
    self.argv = parser.parse_args()

    if self.argv.settings == True:
      s = settings.Settings()
      s.configure()
