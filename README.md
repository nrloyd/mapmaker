# MapMaker

This project can be used to color maps according to proximity to a set of defined points, using mapchart.net. The input to the program comes from two or three text files, and the output is a text file that matches the specifications of the text input to mapchart.net. If specified, the program also outputs the population, area, number of places, and number of territories within each territory.

## Input files
There are two input files required for this program, and one additional optional input file.

### countylist (specify file with -i option)
This input file defines all of the counties, states, countries, or other subdivisions that make up the map. Name, Latitude, and Longitude are essential to the function of the program in every case. Population and Total Area are only relevant if the "-p" option is selected. Land and Water Area are not used in any case and future updates will remove them from the tables. The countylist corresponds to a certain map on mapchart.net, and several countylists are included in this repository:
* United States - Counties (CountyList.txt) (this is currently the only countylist with full population and area included)
* Canada - Provinces (CanadaList.txt)
* Canada - Census div. (CanadaDistrictList.txt)
* Mexico (MexicoList.txt)
* The Americas - Detailed (AmericasList.txt)
* Europe (EuropeList.txt)
* Africa (AfricaList.txt)
* Asia (AsiaList.txt)
* Oceania (OceaniaList.txt)
* World - Detailed (WorldList.txt)

### centerlist (specify with -g)
This input file defines the central point of each territory. Each subdivision is made part of the territory whose central point is closest to its central point. Each territory has a unique name and color on the map. The Secondary Color field is not relevant to the code, but is included in some files for ease of substitution. If any territory contains no land, its name will be printed, but the code will still function properly. If any colors are used by more than one territory, the color will be printed, and some of the duplicate territories will be uncolored. Several centerlists are included in the repository, each of which corresponds to the stadiums of a set of sports teams. These files provide support for:
* Division I College Football (CenterList.txt)
* National Football League (NFLCenters.txt)
* Major League Soccer (MLSCenters.txt)
* National Basketball Association (NBAList.txt)
* Canadian Football League (CFLList.txt)

### resultlist (specify with -r)
This input file is optional, and allows the user to transfer land from territory to territory. Each transfer is complete: all of the land from one territory is added to another. Each entry in the file should be formatted as one line, separated by a tab, with the territory from which the land is to be transferred first, and the territory to which the land is to be transferred last.

## Output file (specify with -o)
This output file will contain the map information required to color the map on mapchart.net. It will already be formatted correctly.

## Author
Nicholas Loyd

## Acknowledgments
Inspired by [this](https://www.reddit.com/r/CFB/comments/7fv3aa/week_13_college_football_imperialism_map/) and similar "imperialism" posts.
