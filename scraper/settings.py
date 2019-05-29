import json

class Settings(object):
  def __init__(self, configFlag=False):
    self.configFile = "configuration.json"
    self.config = {
      "csv": "output.csv",
      "save": True,
      "generic_search": True,
      "tags": [],
      "parsing": []
    }

    # self.domains = [".com", ".org", ".net", ".int", ".edu", ".gov", ".mil", ".info", ".io", ".co"]

    self.read()
    if configFlag:
      self.configure()

  def read(self):
    try:
      with open(self.configFile, "r") as f:
        self.config = json.loads(f.read())
    # If file does not exist, create file with the default configuration
    except FileNotFoundError:
      with open(self.configFile, "w+") as f:
        json.dump(self.config, f)

  def write(self):
    with open(self.configFile, "w") as f:
      json.dump(self.config, f)

  def configure(self):
    while True:
      saveIn = input("[1] Save data to CSV? " + ("[Y]/N " if self.config["save"] == True else "Y/[N] "))
      if saveIn.lower() == "y" or (saveIn == "" and self.config["save"] == True):
        self.config["save"] = True

        fileIn = input("[2] CSV Save Location: (" + self.config["csv"] + ") ")
        if fileIn != "":
          if fileIn[-4] != ".csv":
            fileIn = fileIn + ".csv"
          self.config["csv"] = fileIn
      else:
        self.config["save"] = False

      genericIn = input("[3] Search for specific tag(s)? " + ("[Y]/N " if self.config["generic_search"] == False else "Y/[N] "))
      if genericIn.lower() == "y" or (genericIn == "" and self.config["generic_search"] == False):
        tagsIn = input("[3.1] Enter tags to search for (separated by space) ")
        tagsIn = tagsIn.split()
        self.config["tags"] = tagsIn
      else:
        self.config["generic_search"] = True

      doneIn = input("[4] Done configuring? [Y]/N ")
      if doneIn.lower() == "y" or doneIn == "":
        self.write()
        break
