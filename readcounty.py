import csv

def nameyear(pm):
	s = pm['County'] + pm['Year']


print(__name__)
if __name__== "__main__":
	pm_path = "data/Texas_Postmasters.csv"
	f_obj1 = open(pm_path, "rU")
	pm_reader = csv.DictReader(f_obj1);

	PM = []
	Counties = []


	for row in pm_reader:
		PM.append(row)

	CountyNames = []

	for pm in PM:
		if pm['County'] not in CountyNames:
			CountyNames.append(pm['County'])
			CountyAll = {}
			CountyAll['County'] = pm['County']
			CountyAll['Year'] = '-'
			CountyAll['Num'] = 1
			Counties.append(CountyAll)	

			County = {}
			County['County'] = pm['County']
			County['Year'] = pm['Year']
			County['Num'] = 1
			Counties.append(County)

		else:
			i = 0
			for county in Counties:
				if county['County'] == pm['County']:
					if county['Year'] == pm['Year'] or county['Year'] == '-':
						county['Num'] = county['Num'] + 1
						i = i + 1
			if i < 2:
				County = {}
                		County['County'] = pm['County']
                		County['Year'] = pm['Year']
                		County['Num'] = 1
                		Counties.append(County)
	
	fieldnames = Counties[0].keys()		
	new_path = 'data/Counties.csv'
	f_obj2 = open(new_path, 'wb')
	writer = csv.DictWriter(f_obj2, delimiter=',',fieldnames=fieldnames)
	f = dict(zip(fieldnames,fieldnames))
	writer.writerow(f)
	for county in Counties:
		writer.writerow(county)
	f_obj2.close()
