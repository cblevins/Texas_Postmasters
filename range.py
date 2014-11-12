import csv
print(__name__)
if __name__ == "__main__":
        f_obj1 = open("data/PostMastersPresidents.csv")
        reader = csv.DictReader(f_obj1)

        PM = []
        for row in reader:
                PM.append(row)
        f_obj1.close()

        toRemove = []
        #remove postmasters who were appointed before 1867 or after 1902
        for pm in PM:
                if int(pm["Year"]) < 1867 or ((int(pm["Year"]) == 1867) and (int(pm["Month"]) < 7)):
                        toRemove.append(pm)
		elif int(pm["Year"]) > 1902 or ((int(pm["Year"]) == 1902) and (int(pm["Month"]) > 6)):
			toRemove.append(pm)
        for pm in toRemove:
                PM.remove(pm)

	fieldnames = PM[0].keys()
        f_obj2 = open("data/PostMastersInRange.csv", "wb")
        writer = csv.DictWriter(f_obj2,delimiter=",",fieldnames=fieldnames)
        f = dict(zip(fieldnames,fieldnames))
        writer.writerow(f)
        for pm in PM:
                writer.writerow(pm)
        f_obj2.close()	
