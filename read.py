import csv
from utils import *

print(__name__)
if __name__== "__main__":
	PO = getLinesCSV("data/Texas_PostOffices.csv");
	PM = getLinesCSV("data/Texas_Postmasters.csv");

	#NewApp is set to -50 if the postmaster office is not found in the post offices list
	for pm in PM:
		pm["NewApp"] = -50;

	#cycle through post masters
	for pm in PM:
		#try to find the correct post office
		for po in PO:
			#if found
			if check_name(pm, po) == 1:
				#set NewApp to show whether the appointment was changeover or establishment
				pm["NewApp"] = check_date(pm, po)
				break

	writeCSV(PM, "data/postmasters.csv");
