class posplit:
	earliest_name = “”
	latest_name = “”
	counties = []
	length = 0

	def __init__(self, po):
		Dates = []
		for i in range(1,9):
			if po["Est" + str(i)] != "":
				Dates.append(["Est" + str(i), po["Est" + str(i)]])
		for i in range(1,9):
			if po["Dis" + str(i)] != "":
				Dates.append(["Dis" + str(i), po["Dis" + str(i)]])
		for i in range(1,6):
			if po["NameChangeDate" + str(i)] != "":
				Dates.append(["NameChangeDate" + str(i), po["NameChangeDate" + str(i)]])
		
		Dates = sorted(Dates, key = lambda date: date[1])

		Names = []
		for d in Dates:
			if "NameChangeDate" in d[0]:
				Names.append([d[1], po["FormerName" + d[0][-1]]])

		