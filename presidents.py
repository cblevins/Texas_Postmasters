import csv

def less(pm, p):
	if int(pm["Year"]) < p[2]:
		return 1
	elif int(pm["Year"]) > p[2]:
		return 0
	else:
		if int(pm["Month"]) < p[1]:
			return 1
		elif int(pm["Month"]) > p[0]:
			return 0
		else:
			if int(pm["Day"]) <= p[0]:
				return 1
			else:
				return 0

print(__name__)
if __name__ == "__main__":
	f_obj = open("data/newPostmastersmulti.csv")
	reader = csv.DictReader(f_obj)
	PM = []
	for row in reader:
		PM.append(row)

	toRemove = []

	#discard postmasters with missing date entries:
	for pm in PM:
		if pm["Year"] == "" or pm["Year"] == "0":
			toRemove.append(pm)
		elif pm["Month"] == "" or pm["Month"] == "0":
			toRemove.append(pm)
		elif pm["Day"] == "" or pm["Day"] == "0":
			toRemove.append(pm)

	for pm in toRemove:
		PM.remove(pm)

	#starts with Polk, 30 presidents
	Inaug = [[4,3,1845], [5,3,1849], [10,7,1850], [4,3,1853], [4,3,1857], [4,3,1861], [4,3,1865], [15,4,1865], [4,3,1873], [5,3,1877], [4,3,1881], [20,9,1881], [4,3,1885], [4,3,1889], [4,3,1893], [4,3,1897], [4,3,1901], [14,9,1901], [4,3,1905], [4,3,1909], [4,3,1913], [5,3,1917], [4,3,1921], [4,3,1921], [3,8,1923], [4,3,1925], [4,3,1929], [4,3,1933], [20,1,1937], [20,1,1941]]

	#starts with Johnson, appointed by Polk
	PMGen = [[6,3,1845],[8,3,1849],[23,7,1850],[31,8,1852],[7,3,1853],[6,3,1857],[14,3,1859],[12,2,1861],[5,3,1861],[24,9,1864],[25,7,1866],[5,3,1861], [24,9,1864],[25,7,1866],[5,3,1869],[3,7,1874],[24,8,1874],[12,7,1876],[12,3,1877],[2,6,1880],[5,3,1881],[20,12,1881],[3,4,1883],[14,10,1884],[6,3,1885],[6,1,1888],[5,3,1897],[21,4,1898],[9,1,1902],[10,10,1904],[6,3,1905],[15,1,1907],[5,3,1909],[5,3,1913],[5,3,1921],[4,3,1922],[27,2,1923],[5,3,1929],[4,3,1933],[10,9,1940],[8,5,1945]]

	i = 0
	for p in Inaug:
		p.append(i)
		i = i + 1

        i = 0
        for pgen in PMGen:
                pgen.append(i)
                i = i + 1

	for pm in PM:
		for p in Inaug:
			if less(pm,p)==1:
				pm["President"] = p[3]
				break
	for pm in PM:
		for pgen in PMGen:
			if less(pm,pgen)==1:
				pm["Postmaster General"] = pgen[3]
				break

	for pm in PM:
		print pm

	print i
	f_obj.close()

	fieldnames = PM[0].keys()
	f_obj2 = open("data/PostMastersPresidents.csv", "wb")
	writer = csv.DictWriter(f_obj2,delimiter=",",fieldnames=fieldnames)
	f = dict(zip(fieldnames,fieldnames))
	writer.writerow(f)
	for pm in PM:
		writer.writerow(pm)
	f_obj2.close()
