#Author: Nick Loyd

import math, sys, getopt

#contains the latitude and longitude of the center of the territory, around which it is situated. contains a list of places that make up the territory
class Territory:
    name = "placeholder"
    boxnumber = 0 #needed for the text file at the end
    color = "#000000"
    lat = 0
    long = 0
    population = 0
    area = 0
    numterritories = 0
    
    def __init__(self, **kw):
        
        #the list of places within the territory is initially empty
        self.places = []
        #numterritories keeps track of how many original territories have had their land transferred to make up the current territory
        self.numterritories = 1
        for attr in kw:
            try:
                getattr(self,attr)
                setattr(self,attr,kw[attr])
            except:
                raise KeyError("Unsupported argument %s!" % attr)

    #adds one place to the territory, updating the territory's list of places, total population, and total area
    def addplace(self, placename, pop, are):
        self.places.append(placename)
        self.population += pop
        self.area += are

    #adds all places in other to self, then update the population, area, etc. of both territories to reflect the changes
    def absorb(self, other):
        if len(other.places) != 0:
            self.places.extend(other.places)
            self.population += other.population
            self.area += other.area
            self.numterritories += other.numterritories
            other.places = []
            other.population = 0
            other.area = 0
            other.numterritories = 0
    
    def __str__(self):
        return '"' + self.color + '"' + ':{"div":"#box' + str(self.boxnumber) + '","label":"' + self.name + '","paths":["' + '","'.join(self.places) + '"]}'

#returns the great circle distance between two given points. latuno=latitude of the first point, longuno=longitude of the first point, latdos=latitude of the second point, longdos=longitude of the second point
def greatcircledistance(latuno, longuno, latdos, longdos):
    latone = math.radians(latuno)
    longone = math.radians(longuno)
    lattwo = math.radians(latdos)
    longtwo = math.radians(longdos)
    a = 6378.14
    step1 = math.cos(latone) * math.cos(lattwo) * math.cos(longone-longtwo)
    step2 = math.sin(latone) * math.sin(lattwo)
    step2pt5 = step1+step2
    step3 = math.acos(step2pt5)
    d = a * step3
    return d

def main(argv):

    #open all of the input and output files
    input = open("CountyList.txt") #list of all counties, states, countries, etc.
    output = open("MapFile.txt","w") #output file for mapchart
    guide = open("CenterList.txt") #list of territory centers
    isresults = False
    results = open("ResultList.txt") #list of territory transfers
    printstuff = False
    
    #process command line options, opening the necessary files
    try:
        opts, args = getopt.getopt(argv, "hpi:g:o:r:", ["ifile=","gfile=","ofile=","rfile="])
    except getopt.GetoptError:
        print('mapmaker.py -p (print) -i <countylist> -g <centerlist> -o <outputfile> -r <resultfile>')
        sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print('mapmaker.py -p (print) -i <countylist> -g <centerlist> -o <outputfile> -r <resultfile>')
         sys.exit()
      elif opt == '-p':
          printstuff = True
      elif opt in ("-i", "--ifile"):
         input = open(arg)
      elif opt in ("-g", "--gfile"):
         guide = open(arg)
      elif opt in ("-o", "--ofile"):
         output = open(arg)
      elif opt in ("-r", "--rfile"):
         isresults = True
         results = open(arg)

    #populate list of territories
    input.readline()
    terrs = {}
    centers = []
    for ln in guide:
        words = ln.split("\t")
        centers.append(words)
    i = 0
    colorset = set()
    for word in centers:
        if word[3] in colorset:
            print(word[3] + "\n")
        colorset.add(word[3])
        terrs[word[0]] = Territory(name=word[0], boxnumber=i, color=word[3], lat=float(word[1]), long=float(word[2]))
        i += 1
    for line in input:
        words = line.split("\t")
        lat = float(words[5])
        long = float(words[6])
        leastdist = 100000
        closestcenter = Territory()
        #add place to the closest territory
        for t in terrs:
            dist = greatcircledistance(float(lat), float(long), terrs[t].lat, terrs[t].long)
            if dist < leastdist:
                leastdist = dist
                closestcenter = terrs[t]
        closestcenter.addplace(words[0], int(words[1]), float(words[4]))
    strs = []
    
    #transfer territories from results
    if isresults:
        for line in results:
            words = line.split("\t")
            words[1] = words[1].rstrip()
            terrs[words[1]].absorb(terrs[words[0]])
    
    #print out the mapchart file
    for t in terrs:
        if len(terrs[t].places) == 0:
            print(terrs[t].name)
        else:
            strs.append(terrs[t].__str__())
    toprint = ('{"groups":{' + ','.join(strs) + '},"title":"","hidden":[],"borders":"564d4d"}')  
    toprint = toprint.replace("Lake__FL","Lake_FL")
    toprint = toprint.replace("Lyon__NV","Lyon_NV")
    toprint = toprint.replace("Summit__UT","Summit_UT")
    toprint = toprint.replace("Chittenden__VT","Chittenden_VT")
    output.write(toprint)

    if printstuff:
        areatup = []
        placetup = []
        poptup = []
        terrtup = []
        for t in terrs:
            if len(terrs[t].places) != 0:
                areatup.append((terrs[t].name, terrs[t].area))
                placetup.append((terrs[t].name, len(terrs[t].places)))
                poptup.append((terrs[t].name, terrs[t].population))
                terrtup.append((terrs[t].name, terrs[t].numterritories))
        print("Teams by land area:")
        areatup = sorted(areatup, key = lambda tup: tup[1], reverse = True)
        for x in areatup:
            print(x[0], "%.3f" % x[1])
        print("Teams by number of places:")
        placetup = sorted(placetup, key = lambda tup: tup[1], reverse = True)
        for x in placetup:
            print(x[0], x[1])
        print("Teams by population:")
        poptup = sorted(poptup, key = lambda tup: tup[1], reverse = True)
        for x in poptup:
              print(x[0], x[1])
        print("Teams by number of territories:")
        terrtup = sorted(terrtup, key = lambda tup: tup[1], reverse = True)
        for x in terrtup:
              print(x[0], x[1])

if __name__ == "__main__":
   main(sys.argv[1:])
