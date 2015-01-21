from utils import *

print __name__
if __name__ == "__main__":
	Inaug = getPresidentsDatetime()
	for i in range(len(Inaug)):
		print str(i+1) + " : " + Inaug[i][0] + " : ",
		print Inaug[i][1]
