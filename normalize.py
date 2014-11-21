import csv
from datetime import date
def toDays(in1, in2):
	d1 = date(in1[2],in1[1],in1[0]);
	d2 = date(in2[2],in2[1],in2[0]);
	return d2 - d1

def lengths():
	Inaug = [[4,3,1845], [5,3,1849], [10,7,1850], [4,3,1853], [4,3,1857], [4,3,1861], [4,3,1865], [15,4,1865], [4,3,1869], [4,3,1873], [5,3,1877], [4,3,1881], [20,9,1881], [4,3,1885], [4,3,1889], [4,3,1893], [4,3,1897], [4,3,1901], [14,9,1901], [4,3,1905], [4,3,1909], [4,3,1913], [5,3,1917], [4,3,1921], [3,8,1923], [4,3,1925], [4,3,1929], [4,3,1933], [20,1,1937], [20,1,1941]]
	A = []
	l = len(Inaug)
	i = 0
	while i < l - 1:
		A.append(toDays(Inaug[i],Inaug[i+1]))
		i = i + 1
	d1 = date(Inaug[0][2],Inaug[0][1],Inaug[0][0])
	d2 = date(1867,6,30)
	A[0] = A[0] - (d2 - d1)
	return A
		
print(__name__)
if __name__ == "__main__":
	f_obj1 = open("data/PostMastersInRange.csv")
	reader = csv.DictReader(f_obj1)

	PM = []
	for row in reader:
		PM.append(row)
	f_obj1.close()
	
	NumOffices = [452,494,489,521,596,654,749,818,861,908,1022,1131,1218,1344,1364,1438,1448,1604,1684,1830,1907,2045,2106,2248,2349,2477,2572,2687,2730,2755,2766,2860,2968,3112,3188,3245]

	for pm in PM:
		ind = int(pm["Year"]) - 1867
		if int(pm["Month"]) < 7:
			ind = ind -1
		pm["Weight"] = NumOffices[ind]

	Presidents = []
	PresidentsEst = []
	i = 0
	while i < 36:
		Presidents.append(0)
		PresidentsEst.append(0)
		i = i + 1

	for pm in PM:
		ind = int(pm["President"]) - 1;
		w = 1.0/float(int(pm["Weight"]))
		if pm["NewApp"] == "0":
			Presidents[ind] = Presidents[ind] + w
		else:
			PresidentsEst[ind] = PresidentsEst[ind] + w
	A = lengths();
	i = 0
	l = len(A)
	while i < len(A):
		Presidents[i] = Presidents[i] * 365 / A[i].days
		PresidentsEst[i] = PresidentsEst[i] * 365 / A[i].days
		i = i + 1
	print Presidents
	print PresidentsEst

	Inaug = [[4,3,1845], [5,3,1849], [10,7,1850], [4,3,1853], [4,3,1857], [4,3,1861], [4,3,1865], [15,4,1865], [4,3,1869], [4,3,1873], [5,3,1877], [4,3,1881], [20,9,1881], [4,3,1885], [4,3,1889], [4,3,1893], [4,3,1897], [4,3,1901], [14,9,1901], [4,3,1905], [4,3,1909], [4,3,1913], [5,3,1917], [4,3,1921], [3,8,1923], [4,3,1925], [4,3,1929], [4,3,1933], [20,1,1937], [20,1,1941]]

	for i in range(len(Presidents)):
		print Inaug[i],
		print "	",
		if PresidentsEst[i] == 0:
			print 0
			continue
		else:
			print Presidents[i]/PresidentsEst[i]
		
