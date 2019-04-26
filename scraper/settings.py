import json

class Settings(object):
  def __init__(self):
    self.file = {}
    self.configFile = "configuration.json"
    self.read()

  def read(self):
    with open(self.configFile, "r") as f:
      self.file = json.loads(f.read())

  def write(self):
    with open(self.configFile, "w") as f:
      json.dump(self.file, f)

  def configure(self):
    while True:
      saveIn = input("[1] Save data to CSV? " + ("[Y]/N " if self.file["save"] == True else "Y/[N]"))
      if saveIn.lower() == "y" or (saveIn == "" and self.file["save"] == True):
        self.file["save"] = True

        fileIn = input("[2 CSV Save Location: (" + self.file["csv"] + ") ")
        if fileIn != "":
          if fileIn[-4] != ".csv":
            fileIn = fileIn + ".csv"
          self.file["csv"] = fileIn
      else:
        self.file["save"] = False

      genericIn = input("[3] Search for specific tag(s)? " + ("[Y]/N " if self.file["generic_search"] == False else "Y/[N]"))
      if genericIn.lower() == "y" or (genericIn == "" and self.file["generic_search"] == False):
        tagsIn = input("[3.1] Enter tags to search for (separated by space) ")
        tagsIn = tagsIn.split()
        self.file["tags"] = tagsIn
      else:
        self.file["generic_search"] = True

      doneIn = input("[4] Done configuring? [Y]/N ")
      if doneIn.lower() == "y" or doneIn == "":
        self.write()
        break
