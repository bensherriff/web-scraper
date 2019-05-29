import requests, settings, datetime
from bs4 import BeautifulSoup

class Webpage(object):
  def __init__(self, url):
    self.site = url
    self.request = ""
    self.status_code = 0
    self.s = settings.Settings()
    self.links = {
      "internal": [],
      "external": [],
      "mail": []
    }
    self.scheme = ["http", "https"]
    self.domains = [".com",".co",".app",".online",".space",".store",".tech",".net",".org",".club",".design",".shop",
    ".site",".io",".me",".us",".ca",".ac",".academy",".accountant",".accountants",".actor",".adult",".ae.org",".ae",
    ".af",".africa",".ag",".agency",".ai",".am",".apartments",".com.ar",".archi",".art",".as",".asia",".associates",
    ".at",".attorney",".com.au",".id.au",".net.au",".org.au",".auction",".band",".bar",".bargains",".bayern",".be",
    ".beer",".berlin",".best",".bet",".bid",".bike",".bingo",".bio",".biz",".black",".blog",".blue",".boats",
    ".boston",".boutique",".br.com",".brussels",".build",".builders",".business",".buzz",".bz",".cab",".cafe",".cam",
    ".camera",".camp",".capetown",".capital",".cards",".care",".career",".careers",".casa",".cash",".casino",
    ".catering",".cc",".center",".ch",".charity",".chat",".cheap",".church",".city",".cl",".claims",".cleaning",
    ".click",".clinic",".clothing",".cloud",".cm",".cn.com",".co.uk",".coach",".codes",".coffee",".college",
    ".cologne",".community",".company",".computer",".condos",".construction",".consulting",".contractors",".cooking",
    ".cool",".country",".coupons",".courses",".credit",".cricket",".cruises",".cx",".cz",".dance",".date",".dating",
    ".de",".deals",".degree",".delivery",".democrat",".dental",".dentist",".dev",".diamonds",".digital",".direct",
    ".directory",".discount",".dk",".doctor",".dog",".domains",".download",".durban",".earth",".ec",".eco",
    ".education",".email",".energy",".engineer",".engineering",".enterprises",".equipment",".es",".estate",".eu",
    ".eu.com",".events",".exchange",".expert",".exposed",".express",".fail",".faith",".family",".fan",".fans",".farm",
    ".fashion",".fi",".finance",".financial",".fish",".fishing",".fit",".fitness",".flights",".florist",".fm",
    ".football",".forsale",".foundation",".fr",".fun",".fund",".furniture",".futbol",".fyi",".gallery",".games",
    ".garden",".gd",".gg",".gift",".gifts",".gives",".gl",".glass",".global",".gold",".golf",".gr",".graphics",
    ".gratis",".green",".gripe",".group",".gs",".guide",".guru",".gy",".hamburg",".haus",".health",".healthcare",
    ".help",".hn",".hockey",".holdings",".holiday",".homes",".horse",".hospital",".host",".house",".how",".ht",".id",
    ".im",".immo",".immobilien",".in",".industries",".info",".ink",".institute",".insure",".international",
    ".investments",".is",".it",".je",".jetzt",".jewelry",".joburg",".jp",".jpn.com",".kaufen",".kim",".kitchen",
    ".kiwi",".koeln",".kyoto",".la",".land",".lat",".lawyer",".lc",".lease",".legal",".lgbt",".li",".life",
    ".lighting",".limited",".limo",".link",".live",".loan",".loans",".lol",".london",".love",".lt",".ltd",".lu",
    ".luxe",".lv",".maison",".management",".market",".marketing",".mba",".media",".melbourne",".memorial",".men",
    ".menu",".miami",".mn",".mobi",".moda",".moe",".mom",".money",".mortgage",".ms",".mu",".mx",".nagoya",".name",
    ".network",".news",".ngo",".ninja",".nl",".nu",".nyc",".ac.nz",".org.nz",".kiwi.nz",".net.nz",".school.nz",
    ".gen.nz",".geek.nz",".nz",".co.nz",".maori.nz",".okinawa",".one",".onl",".organic",".osaka",".page",".paris",
    ".partners",".parts",".party",".pe",".pet",".ph",".photo",".photography",".photos",".pics",".pictures",".pink",
    ".pizza",".pl",".plumbing",".plus",".pm",".poker",".porn",".press",".pro",".productions",".promo",".properties",
    ".pt",".pub",".pw",".qa",".qpon",".quebec",".racing",".re",".realestate",".recipes",".red",".rehab",".reise",
    ".reisen",".rent",".rentals",".repair",".report",".republican",".rest",".restaurant",".review",".reviews",".rip",
    ".rocks",".rodeo",".ru.com",".run",".ryukyu",".sa.com",".sale",".salon",".sarl",".com.sb",".sc",".school",
    ".schule",".science",".scot",".se",".services",".sexy",".sg",".com.sg",".sh",".shiksha",".shoes",".shopping",
    ".show",".singles",".ski",".soccer",".social",".software",".solar",".solutions",".soy",".stream",".studio",
    ".study",".style",".supplies",".supply",".support",".surf",".surgery",".sx",".sydney",".systems",".taipei",
    ".tattoo",".tax",".taxi",".tc",".team",".technology",".tel",".tennis",".tf",".theater",".tienda",".tips",".tires",
    ".tk",".tl",".to",".today",".tokyo",".tools",".top",".tours",".town",".toys",".trade",".trading",".training",
    ".tube",".tv",".tw",".org.uk",".me.uk",".uk",".uk.com",".university",".uno",".us.com",".vacations",".vc",".vegas",
    ".ventures",".vet",".vg",".viajes",".video",".villas",".vin",".vip",".vision",".vlaanderen",".vodka",".vote",
    ".voyage",".wales",".wang",".watch",".webcam",".website",".wedding",".wf",".wien",".wiki",".win",".wine",".work",
    ".world",".ws",".wtf",".орг",".xyz",".yoga",".yokohama",".yt",".co.za",".za.com"]
    self.pageStart()

  '''
  pageRequest()
  Description: Takes self.site and checks if it is a valid url. If it is not a valid url,
    it will attempt to make it valid before sending a requests.get(). If requests.get()
    is valid, it is stored in requests and returned. If requests.get() is not valid,
    request is set to -1 and returned.
  Arguments: None
  Return: Request
  '''
  def pageRequest(self):
    
    preFix = False
    postFix = False
    
    # Check if site includes scheme (http:// or https://)
    for substring in self.scheme:
      if substring in self.site:
        preFix = True
        break

    # Check if site includes domain (.com, .org, etc)
    for substring in self.domains:
      if substring in self.site:
        postFix = True
        break
    try:

      # If scheme is missing, try adding http
      if preFix == False:
        print("[Error] Invalid URL: %s" % self.site)
        print("        Missing Scheme: http:// or https://")
        self.site = "http://" + self.site
        print("        Adding Scheme: %s" % self.site)

      # If domain is missing, show error and return
      if postFix == False:
        print("[Error] Invalid URL: %s - Missing Domain" % self.site)
        return -1
        
      # If domain is valid, continue with request
      else:
        request = requests.get(self.site, params=dict(
            query="web scraping",
            page=2
        ))
        self.status_code = request.status_code
        if self.status_code != 200:
          print("[Error] Site: %s" % self.site)
          print("        Status: %d" % self.status_code)
    except Exception as e:
      print("[Error] URL: %s\n        %s" % (self.site, e))
      return -1

    return request

  '''
  pageParse()
  Description:
  Arguments:
  Return: Data
  '''
  def pageParse(self, tag=None):
    soup = BeautifulSoup(self.request.text, "html.parser")
    data = [[],[]]
    
    divs = soup.find_all("div")
    data[0] = []
    for i in divs:
      data[0].append(i)

    links = soup.find_all("a", href=True)
    for i in links:
      d = i["href"]
      if d == "#" or d == "/" or d == "":
        continue
      if d[0:1] == "#" or d[0:1] == "/":
        self.links["internal"].append(d)
      elif d[0:6] == "mailto":
        self.links["mail"].append(d[7:])
      else:
        self.links["external"].append(d)
    return data

  '''
  pageWrite()
  Description:
  Arguments:
  Return:
  '''
  def pageWrite(self, configuration, data):
    fileName = configuration["csv"]
    with open(fileName, "a") as f:

      f.write("URL: " + self.site + "\n")
      currentDT = datetime.datetime.now()
      f.write("Time: " + str(currentDT.strftime("%Y-%m-%d %H:%M:%S")) + "\n")
      f.write("TOTAL LINKS (" + str(sum(map(len, self.links.values()))) + ")\n")

      if len(self.links["internal"]) > 0:
        f.write("INTERNAL LINKS (" + str(len(self.links["internal"])) + ")\n")
        for i in self.links["internal"]:
          f.write(str(i))
          if i is not self.links["internal"][-1]:
            f.write(",")
        f.write("\n")

      if len(self.links["external"]) > 0:
        f.write("EXTERNAL LINKS (" + str(len(self.links["external"])) + ")\n")
        for i in self.links["external"]:
          f.write(str(i))
          if i is not self.links["external"][-1]:
            f.write(",")
        f.write("\n")

      if len(self.links["mail"]) > 0:
        f.write("MAIL LINKS (" + str(len(self.links["mail"])) + ")\n")
        for i in self.links["mail"]:
          f.write(str(i))
          if i is not self.links["mail"][-1]:
            f.write(",")
        f.write("\n")

      f.write("\n")

    print("[+] Data written to", fileName)

  '''
  pageStart()
  Description:
  Arguments:
  Return:
  '''
  def pageStart(self):
    self.request = self.pageRequest()
    if (self.request == -1):
      return 0

    print("[+] Accessing " + self.site)
    data = self.pageParse()

    if self.s.config["save"] == True:
      self.pageWrite(self.s.config, data[0])
    else:
      return 1