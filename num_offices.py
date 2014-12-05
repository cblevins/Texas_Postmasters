from utils import *

def main():
	PO = getLinesCSV("data/Texas_PostOffices.csv")
	earliestYear = 1846
	num = 0
	for po in PO:
		if getpoyear(po, "Est1") == 1846:
			num = num+1
	print "Est in 1846: ", 
	print num

	for po in PO:
		if getpoyear(po, "Est1") == -1:
			continue
		if getpoyear(po, "Est1") > 1867:
			continue
		if getpoyear(po, "Dis1") < 1867 and getpoyear(po, "Dis1") != -1:
			continue
		if getpoyear(po, "Dis1") == -1:
			print po
		num = num + 1
	print num

if __name__ == "__main__":
	main()
