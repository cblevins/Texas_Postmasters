from utils import *

def median(l):
	half = len(l) / 2
	l.sort()
	if len(l) % 2 == 0:
		return (l[half-1] + l[half]) / 2.0
	else:
		return l[half]

print __name__
if __name__ == "__main__":
	PM = getLinesCSV("data/PostmastersDuration.csv")
	Table = [[] for i in range(30)]
	for pm in PM:
		Table[int(pm["PresidentIndex"])-1].append(int(pm["Duration"]))
	Medians = []
	for tab in Table:
		if len(tab) == 0:
			continue
		Medians.append(median(tab))
	print len(Medians)
