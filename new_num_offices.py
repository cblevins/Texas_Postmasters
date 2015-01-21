from utils import *

print __name__
if __name__ == "__main__":
	PO = getLinesCSV("testing.csv")
	PO = changeDates(PO)
	date = datetime.date(1868, 6, 1)
	num_offices = 0
	for po in PO:
		this_office = 0
		for i in range(1, 9):
			if po["Est"+str(i)] != "" and po["Est"+str(i)] <= date:
				this_office = this_office + 1
			if po["Dis"+str(i)] != "" and po["Dis"+str(i)] <= date:
				this_office = this_office - 1
		if this_office > 1:
			print po
		num_offices = num_offices + this_office
	print num_offices
