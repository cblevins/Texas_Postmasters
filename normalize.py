import csv
print(__name__)
if __name__ == "__main__":
	f_obj1 = open("data/PostMastersPresidents.csv")
	reader = csv.DictReader(f_obj1)

	PM = []
	for row in reader:
		PM.append(row)
	f_obj1.close()

	f_obj2 = open("data/OfficesByState_Total.csv")
	reader = csv.DictReader(f_obj2)
	
	TotalOffices = 0

	for row in reader:
		if row["State"] == "Texas":
			totalOffices = row
			break
	f_obj2.close()
	print Totaloffices
