import csv
from utils import *

def nameyear(pm):
	return pm["County"] + pm["Year"]

def newCounty(pm, withYear):
	newCounty = {}
	#set county name
	newCounty["Name"] = pm["County"]
	#set establishment and changeover numbers
	newCounty["EstNum"] = 0
	newCounty["ChangeNum"] = 0
	if isChangeover(pm):
		newCounty["ChangeNum"] = 1
	else:
		newCounty["EstNum"] = 1
	#set year
	if withYear == 1:
		newCounty["Year"] = pm["Year"]
	else:
		newCounty["Year"] = "-"
	return newCounty

def increment(Counties, pm):
	for County in Counties:
		if (pm["County"] == County["Name"]) and (County["Year"] in [pm["Year"],"-"]):
			if isChangeover(pm):
				County["ChangeNum"] = County["ChangeNum"] + 1
			else:
				County["EstNum"] = County["EstNum"] + 1
	return Counties

print(__name__)
if __name__== "__main__":
	PM = getLinesCSV("data/postmasters.csv")
	Counties = []

	CountyNames = set()
	CountyNameYears = set()

	#cycle through postmasters
	for pm in PM:
		#if county has not been encountered, create two new entries: one for the postmaster's year and one for all years
		if pm["County"] not in CountyNames:
			Counties.append(newCounty(pm, 1))
			Counties.append(newCounty(pm, 0))
			#add to set so that, on later iterations, we know the counties have already been seen
			CountyNames.add(pm["County"])
			CountyNameYears.add(nameyear(pm))
		#if the county does not have an entry for the postmaster's year, create one
		elif nameyear(pm) not in CountyNameYears:
			#increment the total for the county
			Counties = increment(Counties,pm)
			Counties.append(newCounty(pm,1))
			#add to set
			CountyNameYears.add(nameyear(pm))
		#if both entries exist, increment
		else:
			Counties = increment(Counties,pm)
	writeCSV(Counties, "data/counties.csv")
