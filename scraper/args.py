import argparse, settings

class Arguments(object):
  def __init__(self):
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="Configure scraper for given url")
    parser.add_argument("-s", "--settings", help="Configure scraper", action="store_true")
    self.argv = parser.parse_args()

    if self.argv.settings == True:
      s = settings.Settings()
      s.configure()
