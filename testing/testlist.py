
def listing1():
	myList = [["\\\\bed4\\testdata"], ["\\\\bed4\\testdata"], ["aha"]]
	return(",".join(map(str, myList)))
listing = listing1()

print listing

def split(listing):
	myList = listing
	return str(myList)[1:-1]

print split(listing)