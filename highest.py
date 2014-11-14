from utils import *
import Queue
print __name__
if __name__ == "__main__":
	Counties = getLinesCSV("data/Geography/Countiesnew.csv","rU")
	pq = Queue.PriorityQueue()
	for c in Counties:
		if c["Year"] == "-":
			pq.put(( float(int(c["ChangeNum"])+1) / (int(c["EstNum"])+1), c["County"]))

	list = []
	while not pq.empty():
		list.append(pq.get())

	print list
