import csv
from utils import *
#PM = inRange(PM, [1867,7,1],[1902,6,30])

print(__name__)
if __name__ == "__main__":
	PM = getLinesCSV("data/newPostmastersmulti.csv")

	#starts with Johnson, appointed by Polk
	PMGen = [[6,3,1845],[8,3,1849],[23,7,1850],[31,8,1852],[7,3,1853],[6,3,1857],[14,3,1859],[12,2,1861],[5,3,1861],[24,9,1864],[25,7,1866],[5,3,1861], [24,9,1864],[25,7,1866],[5,3,1869],[3,7,1874],[24,8,1874],[12,7,1876],[12,3,1877],[2,6,1880],[5,3,1881],[20,12,1881],[3,4,1883],[14,10,1884],[6,3,1885],[6,1,1888],[5,3,1897],[21,4,1898],[9,1,1902],[10,10,1904],[6,3,1905],[15,1,1907],[5,3,1909],[5,3,1913],[5,3,1921],[4,3,1922],[27,2,1923],[5,3,1929],[4,3,1933],[10,9,1940],[8,5,1945]]

	Inaug = getPresidents()
	M = getPresidentsMap()

	#examine postmaster appointments from Polk to F.D.R.
	PM = inRange(PM, [1845,3,4],[1941,1,19])

	#count number of est and change appointments under each president
	Est = [0]*len(Inaug)
	Change = [0]*len(Inaug)
	for pm in PM:
		ind = getPresidentForpm(pm,Inaug)
		if ind == -1:
			continue
		if isChangeover(pm):
			Change[ind] = Change[ind] + 1
		else:
			Est[ind] = Est[ind] + 1

	for i in range(len(Inaug)):
		print M[i] + ":- ",
		print "Est: " + str(Est[i]),
		print " Change: " + str(Change[i]),
		try:
			print " Change/Est ratio: " + str(float(Change[i])/Est[i])
		except ZeroDivisionError:
			print ""
			continue
