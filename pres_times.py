from utils import *

print __name__
if __name__ == "__main__":
	Inaug = getPresidentsDatetime ()
	start = Inaug[0][1]
	for ina in Inaug:
		print (ina[1]-start).days
