import argparse, settings

class Arguments(object):
  def __init__(self):
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="scrape the given URL")
    parser.add_argument("-d", "--depth", dest="depth", help="set how many levels of links the scraper will search",
        default=1, type=int)
    # parser.add_argument("-t", "--threads", dest="threads", help="configure the scraper",
    #     default=1, type=int)
    parser.add_argument("-s", "--settings", help="configure the scraper", action="store_true", default=False)
    self.argv = parser.parse_args()