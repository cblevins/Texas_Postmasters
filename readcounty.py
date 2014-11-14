import csv

def nameyear(pm):
	s = pm['County'] + pm['Year']


print(__name__)
if __name__== "__main__":
	pm_path = "data/newPostmastersmulti.csv"
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
			CountyAll['EstNum'] = 0
			CountyAll['ChangeNum'] = 0
			if int(pm['NewApp']) == 0:
				CountyAll['ChangeNum'] = CountyAll['ChangeNum'] + 1
			else:
				CountyAll['EstNum'] = CountyAll['EstNum'] + 1
			Counties.append(CountyAll)

			CountyAll = {}
			CountyAll['County'] = pm['County']
			CountyAll['Year'] = pm['Year']
			CountyAll['EstNum'] = 0
                        CountyAll['ChangeNum'] = 0
                        if int(pm['NewApp']) == 0:
                                CountyAll['ChangeNum'] = CountyAll['ChangeNum'] + 1
                        else:
                                CountyAll['EstNum'] = CountyAll['EstNum'] + 1
			Counties.append(CountyAll)

		else:
			i = 0
			for county in Counties:
				if county['County'] == pm['County']:
					if county['Year'] == pm['Year'] or county['Year'] == '-':
						if int(pm['NewApp']) == 0:
							county['ChangeNum'] = county['ChangeNum'] + 1
						else:
							county['EstNum'] = county['EstNum'] + 1
						i = i + 1
			if i < 2:
				County = {}
                		County['County'] = pm['County']
                		County['Year'] = pm['Year']
				County['EstNum'] = 0
				County['ChangeNum'] = 0
				if int(pm['NewApp']) == 0:
					County['ChangeNum'] = County['ChangeNum'] + 1
				else:
					County['EstNum'] = County['EstNum'] + 1 
                		Counties.append(County)
	
	fieldnames = Counties[0].keys()		
	new_path = 'data/Geography/Countiesnew.csv'
	f_obj2 = open(new_path, 'wb')
	writer = csv.DictWriter(f_obj2, delimiter=',',fieldnames=fieldnames)
	f = dict(zip(fieldnames,fieldnames))
	writer.writerow(f)
	for county in Counties:
		writer.writerow(county)
	f_obj2.close()
